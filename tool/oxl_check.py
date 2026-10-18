#!/usr/bin/env python3
"""
Compare what the oxlorg.opnsense collection expects (oxl_extract.py output)
with the API an OPNsense release defines (opn_snapshot.py output).

Optionally pass --baseline with the snapshot of the release the collection was
last known to work with: the report then also lists what changed between the
two releases in the parts of the API the collection uses.

Usage: oxl_check.py --collection coll.json --snapshot snap-26.7.7.json \
           [--baseline snap-26.1.11.json] --md report.md --json findings.json
"""

import argparse
import json
import sys
from collections import defaultdict

BASE_MODEL_CTRL = 'OPNsense\\Base\\ApiMutableModelControllerBase'
SEV_ORDER = {'ERROR': 0, 'WARN': 1, 'INFO': 2}


def camelize(s: str) -> str:
    # mirrors OPNsense\Mvc\Router: str_replace('_', '', ucwords($element, '_'))
    return ''.join(w[:1].upper() + w[1:] for w in s.split('_'))


class Api:
    def __init__(self, snap: dict):
        self.snap = snap
        self.label = snap.get('label', '?')
        self.ctrl = snap['controllers']
        self.models = snap['models']
        self.by_module = defaultdict(dict)
        for key, c in self.ctrl.items():
            self.by_module[c['module']][c['controller']] = key

    def controller(self, module: str, controller: str):
        """-> (controller dict | None, problem str | None)"""
        mod = module.replace('_', '').lower()
        name = camelize(controller)
        conts = self.by_module.get(mod)
        if not conts:
            return None, f"API module '{module}' does not exist"
        if name in conts:
            return self.ctrl[conts[name]], None
        for cname, key in conts.items():
            if cname.lower() == name.lower():
                return None, (f"controller '{controller}' resolves to {name}Controller but the file is "
                              f"{cname}Controller (case-sensitive filesystem: use '{_snake(cname)}')")
        return None, f"controller '{module}/{controller}' does not exist (known: {', '.join(sorted(conts))})"

    @staticmethod
    def action(ctrl: dict, command: str):
        return ctrl['actions'].get(camelize(command).lower())

    def model_items(self, ctrl: dict):
        cls = (ctrl or {}).get('model_class')
        if not cls:
            return None
        mdl = self.models.get(cls.lstrip('\\'))
        return mdl['items'] if mdl else None


def _snake(name: str) -> str:
    out = ''
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            out += '_'
        out += ch.lower()
    return out


def resolve(node, path):
    if node is None:
        return None
    for seg in [p for p in path if p]:
        if node.get('kind') == 'field':
            return None
        node = node.get('children', {}).get(seg)
        if node is None:
            return None
    return node


def leaf_fields(node, prefix=()):
    """All leaf fields below a container/array node as {path_tuple: field}; nested arrays not descended."""
    out = {}
    for name, child in (node or {}).get('children', {}).items():
        if child['kind'] == 'field':
            out[prefix + (name,)] = child
        elif child['kind'] == 'container':
            out.update(leaf_fields(child, prefix + (name,)))
        else:
            out[prefix + (name,)] = child  # nested array, treated as one field
    return out


def api_names(field: str, translate: dict):
    """-> list of alternative API paths (tuples) for a collection field"""
    t = translate.get(field, field)
    if isinstance(t, dict) and '__tuple__' in t:
        return [tuple(t['__tuple__'])]
    if isinstance(t, list):
        return [(x,) for x in t if isinstance(x, str)]
    return [(t,)]


def is_relation(field_type) -> bool:
    """ModelRelationField and its subclasses (e.g. GroupedModelRelationField) store UUIDs of other entries"""
    return isinstance(field_type, str) and field_type.endswith('ModelRelationField')


class Checker:
    def __init__(self, coll: dict, api: Api, baseline: Api = None):
        self.coll = coll
        self.api = api
        self.base = baseline
        self.findings = []
        self.mod_by_class = defaultdict(list)
        for mname, m in coll['modules'].items():
            for c in m['classes']:
                self.mod_by_class[c].append(mname)

    def add(self, sev, where, code, msg, **extra):
        self.findings.append({'severity': sev, 'where': where, 'code': code, 'message': msg, **extra})

    # ------------------------------------------------------------------ endpoints
    def endpoint(self, where, module, controller, command, role, sev='ERROR'):
        ctrl, problem = self.api.controller(module, controller)
        url = f'{module}/{controller}/{command}'
        if ctrl is None:
            self.add(sev, where, 'ENDPOINT_MISSING', f'{role}: /api/{url}: {problem}', url=url)
            return None, None
        if command is None:
            return ctrl, None
        act = Api.action(ctrl, command)
        if act is None and ctrl.get('magic_call'):
            self.add('WARN', where, 'ENDPOINT_MAGIC',
                     f"{role}: /api/{url}: no such action, only reachable through the backwards-compatibility "
                     f"__call() in {ctrl['magic_call'].rsplit(chr(92), 1)[-1]} (likely deprecated)", url=url)
        elif act is None:
            self.add(sev, where, 'ENDPOINT_MISSING',
                     f"{role}: /api/{url}: no action '{camelize(command)[:1].lower()}{camelize(command)[1:]}Action' "
                     f"in {ctrl['controller']}Controller ({ctrl['file']})", url=url)
        return ctrl, act

    # ------------------------------------------------------------------ per class
    def check_class(self, key: str, c: dict):
        where = key
        mods = self.mod_by_class.get(key, [])
        if not mods:
            self.add('INFO', where, 'UNUSED', 'no Ansible module uses this class; skipped')
            return
        ov = set(c.get('overrides', []))
        custom_read = sorted(ov & {'search', 'search_call', 'get_existing', 'simplify_existing'})
        custom_write = sorted(ov & {'build_request', 'create', 'update'})
        read_sev = 'WARN' if custom_read else 'ERROR'
        write_sev = 'WARN' if custom_write else 'ERROR'
        read_note = f" (class has custom {', '.join(custom_read)}(): verify)" if custom_read else ''
        write_note = f" (class has custom {', '.join(custom_write)}(): verify)" if custom_write else ''
        cmds = c.get('CMDS') or {}
        mod, cont = c['API_MOD'], c['API_CONT']
        mod_get, cont_get = c.get('API_MOD_GET', mod), c.get('API_CONT_GET', cont)

        acts = {}
        ctrls = {}
        for role, cmd in sorted(cmds.items()):
            if not isinstance(cmd, str):
                continue
            m, ct = (mod_get, cont_get) if role in ('search', 'detail') else (mod, cont)
            sev = 'ERROR'
            if role == 'toggle' and 'enabled' not in (c.get('FIELDS_ALL') or []) \
                    and not ov & {'enable', 'disable'}:
                sev = 'INFO'  # only used when the entry has an 'enabled' field
            ctrl, act = self.endpoint(where, m, ct, cmd, f"CMDS['{role}']", sev)
            acts[role], ctrls[role] = act, ctrl

        has_reload = any('reload' in self.coll['modules'][m]['options'] for m in mods)
        if has_reload and 'reload' not in c.get('overrides', []):
            self.endpoint(where, mod, c.get('API_CONT_REL', cont), c.get('API_CMD_REL', 'reconfigure'), 'reload')

        # ---- where the module reads its entries from
        read_key = c.get('API_KEY_PATH_GET') or c.get('API_KEY_PATH') or ''
        read_segs = read_key.split('.') if read_key else []
        node, node_desc = None, None
        get_ctrl = ctrls.get('search') or ctrls.get('detail')
        items = self.api.model_items(get_ctrl)
        search = cmds.get('search')
        custom_search = bool(custom_read)

        if isinstance(search, str) and search.startswith('search'):
            act = acts.get('detail')
            gb = [b for b in (act or {}).get('base_calls', []) if b['call'] == 'getBase']
            if act is not None and gb and all(gb[0]['args']):
                k, path = gb[0]['args']
                if read_segs[:1] != [k]:
                    self.add(read_sev, where, 'KEY_PATH',
                             f"detail '{cmds.get('detail')}' returns {{'{k}': ...}} (getBase) but API_KEY_PATH"
                             f"{'_GET' if c.get('API_KEY_PATH_GET') else ''} is '{read_key}'{read_note}")
                node = resolve(items, path.split('.') + read_segs[1:])
                node_desc = f"{get_ctrl['model_class']}:{path}"
            elif act is not None:
                self.add('INFO', where, 'UNVERIFIED',
                         f"detail action '{cmds.get('detail')}' is custom (no getBase); key path not verified")
        elif isinstance(search, str) and get_ctrl is not None and acts.get('search') is not None:
            act = acts['search']
            calls_parent = 'parent' in act['tokens'] and f"{act['name']}Action" in act['tokens']
            if act['defined_in'] == BASE_MODEL_CTRL or calls_parent:
                root = get_ctrl.get('model_name')
                if read_segs[:1] != [root]:
                    self.add(read_sev, where, 'KEY_PATH',
                             f"'{search}' returns {{'{root}': ...}} but API_KEY_PATH is '{read_key}'{read_note}")
                node = resolve(items, read_segs[1:])
                node_desc = f"{get_ctrl['model_class']}:{'.'.join(read_segs[1:]) or '<root>'}"
            else:
                # custom get(): the keys it returns must at least be mentioned in its body
                missing = [s for s in read_segs[1:] if s not in act['tokens']]
                if missing:
                    self.add(read_sev, where, 'KEY_PATH',
                             f"'{search}' is overridden in {act['defined_in'].rsplit(chr(92), 1)[-1]} and never "
                             f"references {missing} from API_KEY_PATH '{read_key}' - the module will not find "
                             f"its entries in the response{read_note}")
                node = resolve(items, read_segs[1:])
                node_desc = f"{(get_ctrl or {}).get('model_class')}:{'.'.join(read_segs[1:])}"

        guessed = False
        if node is None and items is not None and node_desc is None and read_segs and not custom_search:
            node = resolve(items, read_segs[1:]) or resolve(items, read_segs)
            node_desc = f"{get_ctrl['model_class']}:{read_key}"
            guessed = True
        if node_desc and node is None:
            self.add('WARN' if guessed else read_sev, where, 'KEY_PATH',
                     f"path {node_desc} does not exist in the model{read_note}")

        # ---- where it writes to
        wrap = (c.get('API_KEY_PATH_REQ') or '').split('.')[0] if c.get('API_KEY_PATH_REQ') \
            else (c.get('API_KEY_PATH') or '').rsplit('.', 1)[-1]
        for role in ('add', 'set'):
            act = acts.get(role)
            if act is None:
                continue
            calls = [b for b in act['base_calls'] if b['call'] in ('addBase', 'setBase')]
            if calls and calls[0]['args'][0]:
                if wrap != calls[0]['args'][0]:
                    self.add(write_sev, where, 'KEY_PATH',
                             f"'{cmds[role]}' expects the payload under '{calls[0]['args'][0]}' "
                             f"but the module sends it under '{wrap}'{write_note}")
            elif act['defined_in'] == BASE_MODEL_CTRL and ctrls[role] is not None:
                root = ctrls[role].get('model_name')
                if wrap != root:
                    self.add(write_sev, where, 'KEY_PATH',
                             f"'{cmds[role]}' (generic setAction) expects the payload under '{root}' "
                             f"but the module sends it under '{wrap}'{write_note}")

        if node is None:
            return
        if node['kind'] == 'field':
            self.add('ERROR', where, 'KEY_PATH', f'{node_desc} is a single field, not a container')
            return

        self.ctrl_tokens = set((get_ctrl or {}).get('tokens', [])) | set((ctrls.get('add') or {}).get('tokens', []))
        self.check_fields(where, c, mods, node, node_desc,
                          'WARN' if (custom_read or custom_write or guessed) else 'ERROR',
                          read_note or write_note or (' (key path guessed)' if guessed else ''))
        if self.base:
            self.diff_node(where, c, get_ctrl, node_desc)

    def check_fields(self, where, c, mods, node, node_desc, sev, note):
        translate = c.get('FIELDS_TRANSLATE') or {}
        optional = set(c.get('FIELDS_OPTIONAL') or [])
        fields = leaf_fields(node)
        used = set()
        for f in c.get('FIELDS_ALL') or []:
            alts = api_names(f, translate)
            hit = [a for a in alts if a in fields]
            if hit:
                used.add(hit[0])
                continue
            names = ' / '.join('.'.join(a) for a in alts)
            if f in optional:
                self.add('INFO', where, 'FIELD_MISSING_OPTIONAL',
                         f"field '{f}' -> '{names}' not in {node_desc} (declared optional)", field=f)
            else:
                self.add(sev, where, 'FIELD_MISSING',
                         f"field '{f}' -> '{names}' not in {node_desc}: reading existing entries will fail "
                         f"or the value is silently ignored{note}", field=f)

        for path, fld in sorted(fields.items()):
            if path in used:
                continue
            if fld.get('kind') == 'field' and fld.get('required') and 'default' not in fld \
                    and not fld.get('volatile') and fld.get('type') not in ('UniqueIdField', 'AutoNumberField') \
                    and path[-1] not in self.ctrl_tokens:
                self.add('WARN', where, 'REQUIRED_NOT_SET',
                         f"API field '{'.'.join(path)}' is required (no default) but the module never sends it")
        unsupported = sorted('.'.join(p) for p in fields if p not in used and not fields[p].get('volatile'))
        if unsupported:
            self.add('INFO', where, 'FIELDS_NOT_SUPPORTED',
                     f"{len(unsupported)} API field(s) not covered: {', '.join(unsupported)}", fields=unsupported)

        # ---- choices vs OptionValues
        vmap = c.get('FIELDS_VALUE_MAPPING') or {}
        seen = set()
        for m in mods:
            for opt, spec in self.coll['modules'][m]['options'].items():
                choices = spec.get('choices')
                if not choices or opt in seen or opt not in (c.get('FIELDS_ALL') or []):
                    continue
                seen.add(opt)
                alts = api_names(opt, translate)
                fld = next((fields[a] for a in alts if a in fields), None)
                if not fld or 'options' not in fld:
                    continue
                api_vals = set(fld['options'])
                sent = {str(vmap.get(opt, {}).get(ch, ch)) for ch in choices if ch not in ('', None)}
                bad = sorted(sent - api_vals)
                new = sorted(api_vals - sent - {''})
                if bad:
                    self.add(sev, where, 'CHOICE_INVALID',
                             f"option '{opt}' allows {bad} which {node_desc}.{'.'.join(alts[0])} rejects "
                             f"(valid: {sorted(api_vals)}){note}", field=opt)
                if new:
                    self.add('INFO', where, 'CHOICE_NEW',
                             f"option '{opt}': API also accepts {new}", field=opt)

    # ------------------------------------------------------------------ release diff
    def diff_node(self, where, c, get_ctrl, node_desc):
        if not get_ctrl or ':' not in (node_desc or ''):
            return
        cls, path = node_desc.split(' ')[0].split(':', 1)
        old_m, new_m = self.base.models.get(cls), self.api.models.get(cls)
        if not old_m or not new_m:
            return
        segs = [] if path == '<root>' else path.split('.')
        old_n, new_n = resolve(old_m['items'], segs), resolve(new_m['items'], segs)
        if old_n is None or new_n is None:
            if old_n is None and new_n is not None:
                self.add('INFO', where, 'RELEASE_DIFF', f'{node_desc} is new since {self.base.label}')
            return
        of, nf = leaf_fields(old_n), leaf_fields(new_n)
        translate = c.get('FIELDS_TRANSLATE') or {}
        used = {a for f in (c.get('FIELDS_ALL') or []) for a in api_names(f, translate)}
        for p in sorted(set(nf) - set(of)):
            self.add('INFO', where, 'RELEASE_DIFF',
                     f"{self.base.label} -> {self.api.label}: field '{'.'.join(p)}' added"
                     + (' (module already uses it: fails on older releases)' if p in used else ''))
        for p in sorted(set(of) - set(nf)):
            self.add('WARN' if p in used else 'INFO', where, 'RELEASE_DIFF',
                     f"{self.base.label} -> {self.api.label}: field '{'.'.join(p)}' removed"
                     + (' (module uses it)' if p in used else ''))
        for p in sorted(set(of) & set(nf)):
            o, n = of[p], nf[p]
            if o.get('options') != n.get('options') and (o.get('options') or n.get('options')):
                added = sorted(set(n.get('options') or []) - set(o.get('options') or []))
                removed = sorted(set(o.get('options') or []) - set(n.get('options') or []))
                self.add('WARN' if removed and p in used else 'INFO', where, 'RELEASE_DIFF',
                         f"{self.base.label} -> {self.api.label}: options of '{'.'.join(p)}'"
                         + (f' +{added}' if added else '') + (f' -{removed}' if removed else ''))
            for attr in ('type', 'required', 'default'):
                if o.get(attr) != n.get(attr) and p in used:
                    sev, note = 'INFO', ''
                    if attr == 'type' and is_relation(o.get(attr)) != is_relation(n.get(attr)):
                        # the field changed between holding a plain value and holding UUIDs of linked entries
                        sev = 'WARN'
                        note = (' (now expects UUIDs of linked entries: plain values sent by the module are rejected)'
                                if is_relation(n.get(attr)) else
                                ' (no longer a link: the module must send the plain value instead of a UUID)')
                    self.add(sev, where, 'RELEASE_DIFF',
                             f"{self.base.label} -> {self.api.label}: '{'.'.join(p)}' {attr} "
                             f"{o.get(attr)!r} -> {n.get(attr)!r}{note}")

    def diff_endpoints(self):
        """Actions of used controllers that changed between baseline and snapshot."""
        if not self.base:
            return
        used = set()
        for c in self.coll['classes'].values():
            for m, ct in ((c['API_MOD'], c['API_CONT']), (c.get('API_MOD_GET', c['API_MOD']),
                                                            c.get('API_CONT_GET', c['API_CONT']))):
                used.add((m, ct))
        for m, ct in sorted(used):
            n, _ = self.api.controller(m, ct)
            o, _ = self.base.controller(m, ct)
            if not n or not o:
                continue
            for a in sorted(set(o['actions']) - set(n['actions'])):
                self.add('WARN', f'{m}/{ct}', 'RELEASE_DIFF',
                         f"{self.base.label} -> {self.api.label}: action '{o['actions'][a]['name']}' removed")
            for a in sorted(set(n['actions']) - set(o['actions'])):
                self.add('INFO', f'{m}/{ct}', 'RELEASE_DIFF',
                         f"{self.base.label} -> {self.api.label}: action '{n['actions'][a]['name']}' added")
            for a in sorted(set(n['actions']) & set(o['actions'])):
                if n['actions'][a]['defined_in'] != o['actions'][a]['defined_in']:
                    self.add('WARN', f'{m}/{ct}', 'RELEASE_DIFF',
                             f"{self.base.label} -> {self.api.label}: action '{n['actions'][a]['name']}' now "
                             f"implemented in {n['actions'][a]['defined_in']} (was {o['actions'][a]['defined_in']})")

    # ------------------------------------------------------------------ inline calls
    def check_inline(self):
        for call in self.coll.get('inline_calls', []):
            if not call['module'] or not call['controller'] or '{' in call['module'] + call['controller']:
                continue
            where = call.get('origin') or f"{call['file']}:{call['line']}"
            cmd = call['command']
            if cmd is not None and '{' in cmd:
                cmd = None
            self.endpoint(where, call['module'], call['controller'], cmd, 'inline call')

    def run(self):
        for key, c in sorted(self.coll['classes'].items()):
            self.check_class(key, c)
        self.check_inline()
        self.diff_endpoints()
        self.findings.sort(key=lambda f: (SEV_ORDER[f['severity']], f['where'], f['code']))
        return self.findings


def to_markdown(findings, coll, api, base) -> str:
    counts = defaultdict(int)
    for f in findings:
        counts[f['severity']] += 1
    lines = [
        f"# oxlorg.opnsense vs OPNsense {api.label}",
        '',
        f"{len(coll['classes'])} module classes and {len(coll.get('inline_calls', []))} inline calls checked"
        + (f", release diff against {base.label}" if base else '') + '.',
        f"**{counts['ERROR']} errors, {counts['WARN']} warnings, {counts['INFO']} notes.**",
        '',
    ]
    groups = []
    if base:
        groups.append((f'New since {base.label}: errors and warnings',
                       [f for f in findings if f.get('new') and f['severity'] != 'INFO']))
        groups.append((f'API changes {base.label} -> {api.label} in endpoints/models the collection uses',
                       [f for f in findings if f['code'] == 'RELEASE_DIFF']))
        groups.append((f'Already present with {base.label}: errors and warnings',
                       [f for f in findings if f.get('new') is False and f['severity'] != 'INFO']))
    else:
        groups += [(sev, [f for f in findings if f['severity'] == sev]) for sev in ('ERROR', 'WARN')]
    groups.append(('Notes: coverage gaps and unverifiable spots',
                   [f for f in findings if f['severity'] == 'INFO' and f['code'] != 'RELEASE_DIFF']))
    for title, sel in groups:
        if not sel:
            continue
        lines += [f'## {title} ({len(sel)})', '']
        cur = None
        for f in sel:
            if f['where'] != cur:
                cur = f['where']
                lines.append(f'### {cur}')
            lines.append(f"- **{f['severity']}** `{f['code']}` {f['message']}")
        lines.append('')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--collection', required=True)
    ap.add_argument('--snapshot', required=True)
    ap.add_argument('--baseline')
    ap.add_argument('--md')
    ap.add_argument('--json')
    ap.add_argument('--fail-on', choices=['ERROR', 'WARN', 'never'], default='ERROR')
    a = ap.parse_args()
    with open(a.collection, encoding='utf-8') as f:
        coll = json.load(f)
    with open(a.snapshot, encoding='utf-8') as f:
        api = Api(json.load(f))
    base = None
    if a.baseline:
        with open(a.baseline, encoding='utf-8') as f:
            base = Api(json.load(f))
    findings = Checker(coll, api, base).run()
    if base:
        before = {(f['where'], f['code'], f['message']) for f in Checker(coll, base).run()}
        for f in findings:
            if f['code'] != 'RELEASE_DIFF':
                f['new'] = (f['where'], f['code'], f['message']) not in before
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            json.dump(findings, f, indent=1)
    md = to_markdown(findings, coll, api, base)
    if a.md:
        with open(a.md, 'w', encoding='utf-8') as f:
            f.write(md)
    else:
        print(md)
    sev = {f['severity'] for f in findings}
    if a.fail_on != 'never' and any(SEV_ORDER[s] <= SEV_ORDER[a.fail_on] for s in sev):
        sys.exit(1)


if __name__ == '__main__':
    main()
