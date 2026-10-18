#!/usr/bin/env python3
"""
Build a static snapshot of the OPNsense MVC API from source checkouts of
opnsense/core and (optionally) opnsense/plugins.

The snapshot contains:
  * every API controller, keyed by URL module + controller class name, with
    its public *Action methods (inherited ones included), the model it is bound
    to and the get/add/set/del/toggle/search *Base() calls each action makes
  * every MVC model (XML) as a field tree: containers, array fields and leaf
    fields with their type, required flag and static option values

Usage: opn_snapshot.py --core <core-checkout> [--plugins <plugins-checkout>] \
           --label 26.7.7 --out snapshot.json
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

MVC = os.path.join('src', 'opnsense', 'mvc', 'app')
BASE_CALLS = ('getBase', 'addBase', 'setBase', 'delBase', 'toggleBase', 'searchBase')


# --------------------------------------------------------------------------- PHP

def strip_php_comments(src: str) -> str:
    """Remove comments while leaving string literals intact."""
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c in ('"', "'"):
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == '\\' else 1
            out.append(src[i:j + 1])
            i = j + 1
        elif src.startswith('/*', i):
            j = src.find('*/', i + 2)
            j = n if j == -1 else j + 2
            out.append('\n' * src.count('\n', i, j))
            i = j
        elif src.startswith('//', i) or (c == '#' and not src.startswith('#[', i)):
            j = src.find('\n', i)
            i = n if j == -1 else j
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def match_brace(src: str, start: int) -> int:
    """Return index after the brace block starting at src[start] == '{'."""
    depth = 0
    i, n = start, len(src)
    while i < n:
        c = src[i]
        if c in ('"', "'"):
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == '\\' else 1
            i = j + 1
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


def split_args(s: str) -> list:
    args, depth, cur, quote = [], 0, [], None
    i = 0
    while i < len(s):
        c = s[i]
        if quote:
            cur.append(c)
            if c == '\\' and i + 1 < len(s):
                cur.append(s[i + 1])
                i += 1
            elif c == quote:
                quote = None
        elif c in ('"', "'"):
            quote = c
            cur.append(c)
        elif c in '([{':
            depth += 1
            cur.append(c)
        elif c in ')]}':
            depth -= 1
            cur.append(c)
        elif c == ',' and depth == 0:
            args.append(''.join(cur).strip())
            cur = []
        else:
            cur.append(c)
        i += 1
    if ''.join(cur).strip():
        args.append(''.join(cur).strip())
    return args


def literal(arg: str, statics: dict):
    arg = arg.strip()
    m = re.fullmatch(r"""(['"])(.*)\1""", arg, re.S)
    if m:
        return m.group(2).replace('\\\\', '\\')
    m = re.fullmatch(r'(?:static|self)::\$(\w+)', arg)
    if m and m.group(1) in statics:
        return statics[m.group(1)]
    return None


def call_args(body: str, pos: int) -> str:
    """Return the raw argument string of the call whose '(' is at pos."""
    depth, i = 0, pos
    quote = None
    while i < len(body):
        c = body[i]
        if quote:
            if c == '\\':
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in ('"', "'"):
            quote = c
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return body[pos + 1:i]
        i += 1
    return body[pos + 1:]


def parse_php_class(path: str) -> dict:
    with open(path, encoding='utf-8', errors='replace') as f:
        src = strip_php_comments(f.read())

    ns = re.search(r'^\s*namespace\s+([\w\\]+)\s*;', src, re.M)
    ns = ns.group(1) if ns else ''
    uses = {}
    for m in re.finditer(r'^\s*use\s+\\?([\w\\]+)(?:\s+as\s+(\w+))?\s*;', src, re.M):
        alias = m.group(2) or m.group(1).rsplit('\\', 1)[-1]
        uses[alias] = m.group(1)

    cm = re.search(r'^\s*(?:abstract\s+|final\s+)*class\s+(\w+)(?:\s+extends\s+([\w\\]+))?', src, re.M)
    if not cm:
        return None
    name, parent = cm.group(1), cm.group(2)
    if parent:
        if parent.startswith('\\'):
            parent = parent[1:]
        else:
            head = parent.split('\\', 1)[0]
            if head in uses:
                parent = uses[head] + parent[len(head):]
            else:
                parent = f'{ns}\\{parent}' if ns else parent

    statics = {}
    for m in re.finditer(
            r'(?:public|protected|private)\s+static\s+(?:\??\w+\s+)?\$(\w+)\s*=\s*(["\'])(.*?)\2\s*;', src):
        statics[m.group(1)] = m.group(3).replace('\\\\', '\\').lstrip('\\')

    methods = {}
    for m in re.finditer(r'((?:public|protected|private|static|final|abstract|\s)*)function\s+(\w+)\s*\(', src):
        mods, mname = m.group(1), m.group(2)
        brace = src.find('{', m.end())
        semi = src.find(';', m.end())
        if brace == -1 or (semi != -1 and semi < brace):
            continue  # abstract / interface
        end = match_brace(src, brace)
        body = src[brace:end]
        params = call_args(src, m.end() - 1)
        calls = []
        for cmatch in re.finditer(r'->(' + '|'.join(BASE_CALLS) + r')\s*\(', body):
            args = split_args(call_args(body, cmatch.end() - 1))
            calls.append({
                'call': cmatch.group(1),
                'raw_args': args[:2],
            })
        methods[mname] = {
            'public': 'private' not in mods and 'protected' not in mods,
            'params': [p.strip() for p in split_args(params)],
            'base_calls': calls,
            # identifiers/strings referenced, used for heuristic checks of custom actions
            'tokens': sorted(set(re.findall(r"[A-Za-z_][\w\-]*", body))),
            'lines': body.count('\n') + 1,
        }

    return {
        'fqn': f'{ns}\\{name}' if ns else name,
        'name': name,
        'parent': parent,
        'statics': statics,
        'methods': methods,
    }


# --------------------------------------------------------------------------- models

def _has_typed_descendant(el) -> bool:
    for d in el.iter():
        if d is not el and d.get('type') is not None:
            return True
    return False


def parse_model_node(el) -> dict:
    typ = el.get('type')
    if typ is None or _has_typed_descendant(el):
        kind = 'container' if typ is None else 'array'
        children = {}
        for c in el:
            if c.tag[:1].isupper() and c.get('type') is None and not _has_typed_descendant(c):
                continue  # field settings like <Required> on custom container types
            children[c.tag] = parse_model_node(c)
        node = {'kind': kind, 'children': children}
        if typ:
            node['type'] = typ
        return node

    node = {'kind': 'field', 'type': typ}
    req = el.find('Required')
    if req is not None and (req.text or '').strip().upper() == 'Y':
        node['required'] = True
    if el.find('Default') is not None:
        node['default'] = (el.findtext('Default') or '').strip()
    if el.get('volatile') == 'true':
        node['volatile'] = True
    if el.find('Multiple') is not None and (el.find('Multiple').text or '').strip().upper() == 'Y':
        node['multiple'] = True
    ov = el.find('OptionValues')
    if ov is not None:
        opts = []
        for o in ov:
            if o.get('value') is None and len(o):
                # <optgroup><value>..</value></optgroup>
                opts.extend(g.get('value') if g.get('value') is not None else g.tag for g in o)
            else:
                opts.append(o.get('value') if o.get('value') is not None else o.tag)
        node['options'] = opts
    return node


def parse_model(path: str):
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return None
    if root.tag != 'model':
        return None
    items = root.find('items')
    return {
        'mount': (root.findtext('mount') or '').strip(),
        'version': (root.findtext('version') or '').strip(),
        'items': parse_model_node(items) if items is not None else {'kind': 'container', 'children': {}},
    }


# --------------------------------------------------------------------------- tree walk

def app_roots(core: str, plugins: str = None):
    yield 'core', os.path.join(core, MVC)
    if plugins:
        for cat in sorted(os.listdir(plugins)):
            cdir = os.path.join(plugins, cat)
            if not os.path.isdir(cdir) or cat.startswith('.'):
                continue
            for plug in sorted(os.listdir(cdir)):
                app = os.path.join(cdir, plug, MVC)
                if os.path.isdir(app):
                    yield f'{cat}/{plug}', app


def build(core: str, plugins: str = None, label: str = '') -> dict:
    classes, models, controllers = {}, {}, {}

    for origin, app in app_roots(core, plugins):
        cdir = os.path.join(app, 'controllers')
        for dp, _, files in os.walk(cdir):
            for f in files:
                if not f.endswith('.php'):
                    continue
                p = os.path.join(dp, f)
                info = parse_php_class(p)
                if info is None:
                    continue
                info['origin'] = origin
                info['file'] = os.path.relpath(p, app)
                classes[info['fqn']] = info

                rel = os.path.relpath(p, cdir).split(os.sep)
                # <Vendor>/<Namespace>/Api/<Name>Controller.php
                if len(rel) == 4 and rel[2] == 'Api' and f.endswith('Controller.php') \
                        and not f.endswith('BaseController.php') and f != 'ControllerBase.php':
                    controllers.setdefault(f'{rel[1].lower()}/{f[:-len("Controller.php")]}', []).append({
                        'vendor': rel[0], 'namespace': rel[1], 'fqn': info['fqn'],
                    })

        mdir = os.path.join(app, 'models')
        for dp, _, files in os.walk(mdir):
            for f in files:
                if not f.endswith('.xml'):
                    continue
                p = os.path.join(dp, f)
                mdl = parse_model(p)
                if mdl is None:
                    continue
                cls = os.path.relpath(p, mdir)[:-4].replace(os.sep, '\\')
                mdl['origin'] = origin
                models[cls] = mdl

    out_ctrl = {}
    for key, cands in sorted(controllers.items()):
        # the router prefers the OPNsense vendor directory
        cands.sort(key=lambda c: (c['vendor'] != 'OPNsense', c['vendor']))
        cand = cands[0]
        chain, cur, seen = [], cand['fqn'], set()
        while cur and cur in classes and cur not in seen:
            seen.add(cur)
            chain.append(classes[cur])
            cur = classes[cur]['parent']
        unresolved_parent = cur if cur and cur not in classes else None

        statics, actions = {}, {}
        for cls in reversed(chain):
            statics.update(cls['statics'])
        for cls in reversed(chain):
            for mname, meth in cls['methods'].items():
                if mname.endswith('Action') and meth['public'] and mname != 'Action':
                    actions[mname[:-6].lower()] = {
                        'name': mname[:-6],
                        'defined_in': cls['fqn'],
                        'params': meth['params'],
                        # re-resolve static::$x references against the final class
                        'base_calls': [dict(c) for c in meth['base_calls']],
                        'tokens': meth['tokens'],
                    }

        top = chain[0] if chain else {}
        out_ctrl[key] = {
            'module': cand['namespace'].lower(),
            'namespace': cand['namespace'],
            'vendor': cand['vendor'],
            'controller': key.split('/', 1)[1],
            'origin': top.get('origin'),
            'file': top.get('file'),
            'parents': [c['fqn'] for c in chain[1:]] + ([unresolved_parent] if unresolved_parent else []),
            'model_class': statics.get('internalModelClass'),
            'model_name': statics.get('internalModelName'),
            'statics': statics,
            'actions': actions,
            'magic_call': next((c['fqn'] for c in chain if '__call' in c['methods']), None),
            # identifiers used anywhere in the non-Base part of the chain (hooks fill in fields etc.)
            'tokens': sorted({t for c in chain if not c['fqn'].startswith('OPNsense\\Base\\')
                              for m in c['methods'].values() for t in m['tokens']}),
        }

    # second pass: static::$x args can only be resolved on the final class
    for key, ctrl in out_ctrl.items():
        for act in ctrl['actions'].values():
            for call in act['base_calls']:
                call['args'] = [literal(a, ctrl['statics']) for a in call.pop('raw_args')]

    return {
        'label': label,
        'controllers': out_ctrl,
        'models': models,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--core', required=True)
    ap.add_argument('--plugins')
    ap.add_argument('--label', default='')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    snap = build(a.core, a.plugins, a.label)
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(snap, f, indent=1, sort_keys=True)
    print(f"{a.label}: {len(snap['controllers'])} controllers, {len(snap['models'])} models -> {a.out}",
          file=sys.stderr)


if __name__ == '__main__':
    main()
