#!/usr/bin/env python3
"""
Extract what the oxlorg.opnsense collection expects from the OPNsense API.

For every class in plugins/module_utils/main/ that declares API_MOD it records
the URL parts (module, controller, commands), the key paths it reads and
writes, the API field names it uses and the Ansible modules built on it with
their argument choices.

The collection is imported for real (so FIELDS_ALL.extend() and friends are
resolved), which needs ansible-core and httpx installed.

Usage: oxl_extract.py --collection <checkout> --out collection.json
"""

import argparse
import ast
import importlib
import inspect
import json
import os
import re
import sys
import tempfile
import textwrap

sys.dont_write_bytecode = True  # do not litter the checkout with __pycache__

PKG = 'ansible_collections.oxlorg.opnsense'
ATTRS = [
    'API_MOD', 'API_CONT', 'API_MOD_GET', 'API_CONT_GET', 'API_CONT_REL', 'API_CMD_REL',
    'API_KEY_PATH', 'API_KEY_PATH_REQ', 'API_KEY_PATH_GET', 'CMDS', 'FIELD_ID', 'FIELD_PK',
    'FIELDS_ALL', 'FIELDS_CHANGE', 'FIELDS_TRANSLATE', 'FIELDS_OPTIONAL', 'FIELDS_TYPING',
    'FIELDS_VALUE_MAPPING', 'FIELDS_VALUE_MAPPING_RCV', 'FIELDS_BOOL_INVERT', 'SEARCH_ADDITIONAL',
]


class _Captured(Exception):
    def __init__(self, kwargs):
        super().__init__('captured')
        self.kwargs = kwargs


class _FakeModule:
    def __init__(self, *args, **kwargs):
        if args:
            kwargs['argument_spec'] = args[0]
        raise _Captured(kwargs)


def _jsonable(v):
    if isinstance(v, dict):
        return {str(k): _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, set)):
        return [_jsonable(x) for x in v]
    if isinstance(v, tuple):
        return {'__tuple__': [_jsonable(x) for x in v]}
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    return repr(v)


def _setup_path(collection: str) -> str:
    tmp = tempfile.mkdtemp(prefix='oxl-')
    os.makedirs(os.path.join(tmp, 'ansible_collections', 'oxlorg'))
    os.symlink(os.path.abspath(collection), os.path.join(tmp, 'ansible_collections', 'oxlorg', 'opnsense'))
    sys.path.insert(0, tmp)
    return tmp


def _defines(cls, name: str) -> bool:
    for c in cls.__mro__:
        if c.__module__.startswith(f'{PKG}.plugins.module_utils.base'):
            return False
        if name in c.__dict__:
            return True
    return False


def _const(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return ''.join(v.value if isinstance(v, ast.Constant) else '{}' for v in node.values)
    return None


def inline_calls(collection: str) -> list:
    """API calls built as {'module': .., 'controller': .., 'command': ..} dict literals."""
    calls = []
    root = os.path.join(collection, 'plugins')
    for dp, _, files in os.walk(root):
        for f in sorted(files):
            if not f.endswith('.py') or f.endswith('_pytest.py'):
                continue
            p = os.path.join(dp, f)
            with open(p, encoding='utf-8') as fh:
                tree = ast.parse(fh.read())
            for node in ast.walk(tree):
                if not isinstance(node, ast.Dict):
                    continue
                keys = {_const(k): v for k, v in zip(node.keys, node.values) if k is not None}
                if 'module' not in keys or 'controller' not in keys:
                    continue
                entry = {
                    'file': os.path.relpath(p, collection),
                    'line': node.lineno,
                    'module': _const(keys['module']),
                    'controller': _const(keys['controller']),
                    'command': _const(keys['command']) if 'command' in keys else None,
                }
                cmd = keys.get('command')
                # module.params['x'] / MAPPING[module.params['x']]
                if isinstance(cmd, ast.Subscript):
                    if isinstance(cmd.value, ast.Name) and isinstance(cmd.slice, ast.Subscript):
                        entry['command_map'] = cmd.value.id
                    elif isinstance(cmd.value, ast.Attribute) and cmd.value.attr == 'params':
                        entry['command_param'] = _const(cmd.slice)
                calls.append(entry)
    return calls


def expand_dynamic(calls: list, modules: dict) -> list:
    """Resolve commands taken from a module parameter (its choices) or a module-level mapping."""
    out = []
    for call in calls:
        name = os.path.basename(call['file'])[:-3]
        values = None
        if call['file'].startswith('plugins/modules/') and call.get('command_param'):
            values = (modules.get(name, {}).get('options', {}).get(call['command_param']) or {}).get('choices')
        elif call['file'].startswith('plugins/modules/') and call.get('command_map'):
            try:
                mapping = getattr(importlib.import_module(f'{PKG}.plugins.modules.{name}'), call['command_map'])
                values = sorted(set(v for v in mapping.values() if isinstance(v, str)))
            except Exception:  # pylint: disable=W0718
                values = None
        if values:
            for v in values:
                out.append({**call, 'command': v, 'origin': f"{call['file']}:{call['line']} ({v})"})
        else:
            out.append(call)
    return out


def savepoint_calls(collection: str, modules: dict) -> list:
    p = os.path.join(collection, 'plugins', 'module_utils', 'main', 'savepoint.py')
    with open(p, encoding='utf-8') as fh:
        cmds = sorted(set(re.findall(r"'command':\s*'(\w+)'", fh.read())))
    opts = modules.get('savepoint', {}).get('options', {})
    calls = []
    for mod in (opts.get('api_module') or {}).get('choices') or ['firewall']:
        for cont in (opts.get('controller') or {}).get('choices') or []:
            for cmd in cmds:
                calls.append({'file': 'plugins/module_utils/main/savepoint.py', 'line': 0,
                              'origin': f'savepoint {cont}/{cmd}', 'module': mod, 'controller': cont, 'command': cmd})
    return calls


def service_calls() -> list:
    mod = importlib.import_module(f'{PKG}.plugins.modules.service')
    calls = []
    default_actions = ['reload', 'restart', 'start', 'status', 'stop']
    for name, svc in mod.SERVICES.items():
        for action in svc.get('a', default_actions):
            cmd = svc.get('m', {}).get(action, mod.ACTION_MAPPING.get(action, action))
            calls.append({
                'file': 'plugins/modules/service.py', 'line': 0, 'origin': f'service {name}/{action}',
                'module': svc.get('c', name), 'controller': mod.API_CONTROLLER, 'command': cmd,
            })
    return calls


def value_translations(mod, src: str, opts: dict) -> None:
    """
    Record in opts[<option>]['sent_map'] how a module rewrites an argument's choices before sending them:
    - a module-level mapping applied as MAP[...] whose keys are the option's choices
      (e.g. MONTH_MAPPING = {1: 'JAN', ...})
    - a mapping of option -> choice that the module blanks with module.params[..] = ''
      (e.g. BLANK_VALUES = {'errors': 'squid'} for fields whose empty value is the API default)
    - module.params['x'] = module.params['x'].upper() / .lower()
    """
    maps = {}
    for name, obj in vars(mod).items():
        if isinstance(obj, dict) and obj and name.isupper() and re.search(rf'^{name}\s*=', src, re.M) \
                and len(re.findall(rf'\b{name}\b', src)) > 1:  # defined here and used
            maps[name] = obj
    blanking = re.search(r"module\.params\[[^\]]+\]\s*=\s*''", src) is not None

    for opt, spec in opts.items():
        choices = [str(c) for c in spec.get('choices') or [] if c not in ('', None)]
        if not choices:
            continue
        # value mappings: prefer the map whose keys are exactly the choices
        cands = [(n, m) for n, m in maps.items() if set(choices) <= {str(k) for k in m}]
        exact = [(n, m) for n, m in cands if {str(k) for k in m} == set(choices)]
        pick = exact if len(exact) == 1 else (cands if len(cands) == 1 else [])
        if pick and all(isinstance(v, (str, int, bool)) for v in pick[0][1].values()):
            n, m = pick[0]
            spec['sent_map'] = {str(k): str(v) for k, v in m.items() if str(k) in choices}
            spec['translated_by'] = n
            continue
        if blanking:
            for n, m in maps.items():
                if isinstance(m.get(opt), str) and m[opt] in choices:
                    spec['sent_map'] = {m[opt]: ''}
                    spec['translated_by'] = f"{n} (sent as empty value)"
                    break
            if 'sent_map' in spec:
                continue
        case = re.search(rf"module\.params\[(['\"]){opt}\1\]\s*=\s*module\.params\[\1{opt}\1\]\.(upper|lower)\(\)", src)
        if case:
            fn = str.upper if case.group(2) == 'upper' else str.lower
            spec['sent_map'] = {c: fn(c) for c in choices}
            spec['translated_by'] = f'.{case.group(2)}()'


READ_METHODS = ('search', 'search_call', 'get_existing', 'simplify_existing')


def code_info(cls, overrides: list) -> dict:
    """
    What the class's own (overridden) methods do with API keys and fields, so the checker can tell
    "reads the response in its own way" from "uses API_KEY_PATH / FIELDS_TRANSLATE like the base class".
    """
    def method_tree(name):
        for c in cls.__mro__:
            if name in c.__dict__:
                try:
                    return ast.parse(textwrap.dedent(inspect.getsource(c.__dict__[name])))
                except (OSError, TypeError, SyntaxError):
                    return None
        return None

    def strings(tree):
        out = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                out.add(n.value)
            elif isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == 'self' \
                    and isinstance(getattr(cls, n.attr, None), str):
                out.add(getattr(cls, n.attr))
        return out

    def reads_same_key(expr, key):
        return any(isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name)
                   and isinstance(n.slice, ast.Constant) and n.slice.value == key for n in ast.walk(expr))

    info = {'read_uses_key_path': True, 'replaced_fields': [], 'build_refs': []}
    read_src, replaced = '', set()
    for name in overrides:
        tree = method_tree(name)
        if tree is None:
            continue
        if name in READ_METHODS:
            read_src += ast.unparse(tree)
            for n in ast.walk(tree):
                # x['field'] = <value not derived from x['field']>: the class fills the field itself
                if isinstance(n, ast.Assign):
                    for t in n.targets:
                        if isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Constant) \
                                and isinstance(t.slice.value, str) and not reads_same_key(n.value, t.slice.value):
                            replaced.add(t.slice.value)
        if name == 'build_request':
            info['build_refs'] = sorted(strings(tree))
    if set(overrides) & {'search', 'search_call', 'get_existing'} and not any(
            k in read_src for k in ('API_KEY_PATH', '_base_get_existing', 'self.search(', 'super(')):
        info['read_uses_key_path'] = False
    info['replaced_fields'] = sorted(replaced)
    return info


def extract(collection: str) -> dict:
    _setup_path(collection)
    main_dir = os.path.join(collection, 'plugins', 'module_utils', 'main')
    classes, errors = {}, []

    for f in sorted(os.listdir(main_dir)):
        if not f.endswith('.py') or f.endswith('_pytest.py') or f == '__init__.py':
            continue
        try:
            mod = importlib.import_module(f'{PKG}.plugins.module_utils.main.{f[:-3]}')
        except Exception as e:  # pylint: disable=W0718
            errors.append(f'{f}: {e!r}')
            continue
        for name, cls in inspect.getmembers(mod, inspect.isclass):
            if cls.__module__ != mod.__name__ or not hasattr(cls, 'API_MOD'):
                continue
            entry = {'file': f'plugins/module_utils/main/{f}', 'class': name}
            for a in ATTRS:
                if hasattr(cls, a):
                    entry[a] = _jsonable(getattr(cls, a))
            entry['overrides'] = sorted(
                m for m in ('reload', 'search', 'search_call', 'get_existing', 'create', 'update', 'delete',
                            'process', 'check', 'simplify_existing', 'build_request', 'enable', 'disable')
                if _defines(cls, m)
            )
            entry['code'] = code_info(cls, entry['overrides'])
            classes[f'{f[:-3]}.{name}'] = entry

    modules = {}
    mod_dir = os.path.join(collection, 'plugins', 'modules')
    for f in sorted(os.listdir(mod_dir)):
        if not f.endswith('.py') or f == '__init__.py':
            continue
        try:
            mod = importlib.import_module(f'{PKG}.plugins.modules.{f[:-3]}')
        except Exception as e:  # pylint: disable=W0718
            errors.append(f'modules/{f}: {e!r}')
            continue
        used = []
        for _, obj in vars(mod).items():
            if inspect.isclass(obj) and obj.__module__.startswith(f'{PKG}.plugins.module_utils.main.') \
                    and hasattr(obj, 'API_MOD'):
                used.append(f"{obj.__module__.rsplit('.', 1)[1]}.{obj.__name__}")
        spec = None
        runner = getattr(mod, 'run_module', None) or getattr(mod, 'main', None)
        if runner is not None and hasattr(mod, 'AnsibleModule'):
            orig = mod.AnsibleModule
            mod.AnsibleModule = _FakeModule
            try:
                runner()
            except _Captured as c:
                spec = c.kwargs.get('argument_spec')
            except Exception as e:  # pylint: disable=W0718
                errors.append(f'modules/{f}: argspec {e!r}')
            finally:
                mod.AnsibleModule = orig
        opts = {}
        for opt, d in (spec or {}).items():
            if not isinstance(d, dict):
                continue
            opts[opt] = {k: _jsonable(d[k]) for k in ('type', 'choices', 'aliases', 'default', 'required', 'elements')
                         if k in d}
        with open(os.path.join(mod_dir, f), encoding='utf-8') as fh:
            value_translations(mod, fh.read(), opts)
        modules[f[:-3]] = {'classes': sorted(set(used)), 'options': opts}

    calls = expand_dynamic(inline_calls(collection), modules)
    try:
        calls.extend(savepoint_calls(collection, modules))
        calls.extend(service_calls())
    except Exception as e:  # pylint: disable=W0718
        errors.append(f'service mapping: {e!r}')

    return {'classes': classes, 'modules': modules, 'inline_calls': calls, 'errors': errors}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--collection', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    data = extract(a.collection)
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1, sort_keys=True)
    print(f"{len(data['classes'])} classes, {len(data['modules'])} modules, {len(data['errors'])} errors",
          file=sys.stderr)
    for e in data['errors']:
        print('  ' + e, file=sys.stderr)


if __name__ == '__main__':
    main()
