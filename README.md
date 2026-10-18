# OPNsense API vs oxlorg.opnsense: static compatibility check

A static check that compares the API OPNsense defines in its source (opnsense/core and opnsense/plugins) with the API the oxlorg.opnsense collection calls. You don't need a firewall, a VM or any Ansible runs. One run takes about 20 seconds per release once the sources are cloned.

## What the 26.7 run found

Inputs: the collection at `nerrehmit/collection_opnsense` HEAD (5cec92e, collection version 26.1.11), checked against OPNsense **26.7.7** and diffed against **26.1.11**. The full report is in [reports/report-26.7.7.md](reports/report-26.7.7.md).

### New breakages in 26.7 (these worked on 26.1.11)

| Module | What broke in 26.7 |
|---|---|
| `nat_source` | `firewall/source_nat/get` now returns only `filter.general`, so the rules are no longer in the response. This is issue **#446**. |
| `savepoint` | `savepoint`, `revert` and `cancelRollback` were removed from every firewall controller (filter, source_nat, one_to_one, d_nat), and core has no replacement anywhere. Only `apply` is left. |
| `frr_ospf3_network` | `quagga/ospf6settings/*Network` endpoints and the `networks.network` model node are gone (the FRR plugin uses areas/interfaces now). |
| `frr_ospf_general` | field `passiveinterfaces` removed |
| `frr_ospf_network` | fields `arearange`, `linkedPrefixlistIn`, `linkedPrefixlistOut` removed |
| `frr_bgp_neighbor` | field `multiprotocol` removed |
| `service` (name `iperf`) | `iperf/service/*` no longer exists. The plugin now has only `client` and `instance` controllers. |

### Problems that already existed on 26.1.11 (worth fixing while at it)

These need a quick look at the module code, because the checker can't see value translations done by hand.

- `frr_diagnostic`: every target (`bgproute4`, `ospfroute`, ...) was renamed to `search*` in the FRR plugin, e.g. `searchBgproute4`.
- `service`: `fetchmail`, `softether` and `legacy_subsystem` (ipsec_legacy) no longer exist. `ftp_proxy`/`udp_broadcast_relay` have no `reconfigure`, and `tinc` has no `status`.
- `haproxy_fcgi`: `toggleFcgi` doesn't exist, but the class uses `enabled`.
- `unbound_dot`: `add/set/del/toggleDot` are only served through a backwards-compatibility `__call()` that forwards to `*Forward`, so it's deprecated and will likely disappear.
- Argument choices the API rejects: `nat_source.ip_protocol=inet46`; `openvpn_*.mode=dco`; `openvpn_server.user_cn_strict`; `haproxy_cpu.thread_id=x0`; several `webproxy_*` options (`default`/`squid`/`file`, numeric months/weekdays vs `JAN`/`MON`, lowercase vs uppercase PAC proxy types); `bind_blocklist.block` labels; `interface_lagg` yes/no vs 1/0.
- `acme_validation`: field `dns_active24_token` no longer exists.
- `alias_purge`: the module is deliberately retired (it calls `fail_json` pointing to the `*_multi` modules), but it imports `PURGE_MOD_ARGS` and `INFO_MOD_ARG`, which no longer exist. So users get a misleading "install httpx" error instead of the deprecation message.

### Coverage gaps (not breakages)

26.7 added 30 fields to models the collection already manages, for example new ACME DNS providers, `ping_check` on DHCP subnets and new rule/NAT fields. They are listed under "API changes" (INFO) in the report. Separately, every module lists the API fields it doesn't expose (`FIELDS_NOT_SUPPORTED`).

### Validation against the two known issues

- **#446** is reported as a *new* error against 26.7.7: `nat_source.SNat KEY_PATH 'get' is overridden in SourceNatController and never references ['snatrules', 'rule']`. The release diff also shows `firewall/source_nat: action 'get' now implemented in SourceNatController (was ApiMutableModelControllerBase)`.
- **#466** is a point-release problem. `staticnatport` first appears in core **26.1.5**, not 26.7: 26.1–26.1.4 lack it and 26.1.5–26.1.11 have it. Against 26.1.11 there is nothing to report. Against **26.1.4** the checker reports `nat_source.SNat FIELD_MISSING field 'static_port' -> 'staticnatport'` ([reports/report-26.1.4.md](reports/report-26.1.4.md)). So to cover a whole series, run the check against the first and the latest point release, or against every one of them.

## How it works

1. `tool/opn_snapshot.py` reads the OPNsense sources and writes a JSON snapshot:
   - every API controller (`/api/<module>/<controller>/<action>`), with inherited actions resolved through the class chain, its bound model (`$internalModelClass` / `$internalModelName`), the `getBase/addBase/setBase/...` calls in each action, and whether it has a `__call()` fallback
   - every model XML as a field tree: container / ArrayField / field, type, required, default, and static `OptionValues` (option groups included).
2. `tool/oxl_extract.py` imports the collection, which needs `ansible-core` and `httpx`. For each `module_utils/main` class it records `API_MOD/API_CONT/CMDS/API_KEY_PATH*/FIELDS_*`. It also captures each Ansible module's argument spec (choices included) and the inline `{'module', 'controller', 'command'}` calls, expanding choice- or mapping-driven commands and the `service`/`savepoint` tables.
3. `tool/oxl_check.py` matches them up the way the OPNsense router does (`snake_case` → `CamelCase`, controller file names are case-sensitive, actions aren't). It reports:
   - `ENDPOINT_MISSING`: a module/controller/action that doesn't exist
   - `KEY_PATH`: the response or request wrapper key doesn't match what `get`/`getBase`/`addBase`/`setBase` use, or the path isn't in the model
   - `FIELD_MISSING`: a field the module reads or writes that isn't in the model
   - `CHOICE_INVALID`: an argument choice that isn't in the field's `OptionValues`
   - `REQUIRED_NOT_SET`: a required API field without a default that the module never sends
   - With `--baseline`: what changed between the two releases in the endpoints and models the collection uses, and whether each finding is new.
     A used field that switches between a plain field and a `ModelRelationField` (in either direction) is a WARN, because the module then sends the wrong kind of value (plain value vs. UUID of the linked entry). Other type, required and default changes stay INFO.

Severity is lowered to WARN wherever the class overrides `search_call`, `get_existing`, `simplify_existing`, `build_request` and so on, because the static view may be wrong there. Those lines end in "verify".

## Rerun / keep up with releases

```sh
pip install ansible-core httpx
# target release, optional baseline (the release the collection last supported)
OUT=reports bash tool/run.sh /path/to/collection_opnsense 26.7.7 26.1.11
# exits 1 on errors; FAIL_ON=WARN or FAIL_ON=never to change that
```

To follow new releases, run it for each new `26.7.x` tag with the previous tag as baseline. The "New since …" and "API changes …" sections are then exactly the delta to look at. That fits a scheduled GitHub Actions job on the collection repo that watches `opnsense/core` tags. I haven't added that to the repo yet.

## Limitations

- It's static. Behaviour inside custom PHP actions is only checked heuristically (for a custom `get`, the keys must at least appear in its body). Dynamic option lists (interfaces, aliases, certificates) aren't compared.
- Value translations the collection does in code, outside `FIELDS_VALUE_MAPPING`, can make a `CHOICE_INVALID` a false alarm. Check before fixing.
- Plugins are compared at the same tag as core (`opnsense/plugins` uses matching tags). A box with an older plugin build may differ.
