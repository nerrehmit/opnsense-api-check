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

These need a quick look at the module code before fixing.

- `frr_diagnostic`: every target (`bgproute4`, `ospfroute`, ...) was renamed to `search*` in the FRR plugin, e.g. `searchBgproute4`.
- `service`: `fetchmail`, `softether` and `legacy_subsystem` (ipsec_legacy) no longer exist. `ftp_proxy`/`udp_broadcast_relay` have no `reconfigure`, and `tinc` has no `status`.
- `haproxy_fcgi`: `toggleFcgi` doesn't exist, but the class uses `enabled`.
- `unbound_dot`: `add/set/del/toggleDot` are only served through a backwards-compatibility `__call()` that forwards to `*Forward`, so it's deprecated and will likely disappear.
- Argument choices the API rejects: `nat_source.ip_protocol=inet46`; `openvpn_*.mode=dco` (the API calls it `ovpn`); `haproxy_cpu.thread_id=x0`; `interface_lagg` yes/no vs 1/0; `interface_vip.mode=other`.
- `acme_validation`: field `dns_active24_token` no longer exists.
- `alias_purge`: the module is deliberately retired (it calls `fail_json` pointing to the `*_multi` modules), but it imports `PURGE_MOD_ARGS` and `INFO_MOD_ARG`, which no longer exist. So users get a misleading "install httpx" error instead of the deprecation message.

### Coverage gaps (not breakages)

26.7 added 30 fields to models the collection already manages, for example new ACME DNS providers, `ping_check` on DHCP subnets and new rule/NAT fields. They are listed under "API changes" (INFO) in the report. Separately, every module lists the API fields it doesn't expose (`FIELDS_NOT_SUPPORTED`).

### Validation against the two known issues

- **#446** is reported as a *new* error against 26.7.7: `nat_source.SNat KEY_PATH 'get' is overridden in SourceNatController and never references ['snatrules', 'rule']`. The release diff also shows `firewall/source_nat: action 'get' now implemented in SourceNatController (was ApiMutableModelControllerBase)`.
- **#466** is a point-release problem. `staticnatport` first appears in core **26.1.5**, not 26.7: 26.1–26.1.4 lack it and 26.1.5–26.1.11 have it. Against 26.1.11 there is nothing to report. Against **26.1.4** the checker reports `nat_source.SNat FIELD_MISSING field 'static_port' -> 'staticnatport'` ([reports/report-26.1.4.md](reports/report-26.1.4.md)). So to cover a whole series, run the check against the first and the latest point release, or against every one of them.

## What the 26.7.8 run found

Inputs: the collection at `nerrehmit/collection_opnsense` HEAD (7b06551), checked against OPNsense **26.7.8** and diffed against **26.7.7**. The full report is in [reports/report-26.7.8.md](reports/report-26.7.8.md). Nothing was removed or renamed in the endpoints the collection calls. Two changes matter:

| Module | What changed in 26.7.8 |
|---|---|
| `ipsec_connection` | The labels of `version` gained "(deprecated)" notes (`IKEv1+IKEv2 (allows deprecated IKEv1)`, `IKEv1 (deprecated)`). The class maps the old labels back (`FIELDS_VALUE_MAPPING_RCV`), so a connection with `version: ikev1+2` (the module default) or `ikev1` is reported as changed on every run. The model default also moved from `0` (IKEv1+IKEv2) to `2` (IKEv2), which doesn't matter here because the module always sends `version`. |
| `unbound_dnsbl` | The provider `atf` (Abuse.ch ThreatFox IOC) was removed. `providers` has no `choices`, so a playbook that still lists `atf` now gets a validation error from the API. |

The other release changes are additions (`charon.retry_initiate_interval` in IPsec general settings, CSV export/import of Unbound host overrides) and label tweaks.

## What the 26.7.9 run found

Inputs: the collection at upstream `O-X-L/ansible-opnsense` `latest` (db38431). Its code is the same as 7b06551, the three newer commits only change docs. It was checked against OPNsense **26.7.9** (released 2026-11-11, core 228ab68, plugins a01a2e8) and diffed against **26.7.8**. The full report is in [reports/report-26.7.9.md](reports/report-26.7.9.md): 43 errors and 15 warnings (26.7.8: 41 and 15). Every 26.7.8 finding is still there, including the `ipsec_connection` `LABEL_MISMATCH`. One change breaks a module:

| Module | What changed in 26.7.9 |
|---|---|
| `acme_validation` | os-acme-client 4.18 switched the Selfhost DNS API to an API key ("BREAKING CHANGE" in its changelog). `dns_selfhost_user` and `dns_selfhost_password` were removed and `dns_selfhost_apikey` was added. OPNsense ignores keys that aren't in the model and the class only compares `description` and `method`, so tasks still run, but the old Selfhost options are silently dropped and there is no option for the new key. Other DNS providers aren't affected. |

The other 37 release-diff entries are additions (INFO): 7 ACME DNS providers and a TOTP secret for 1984Hosting, 2 ACME deploy hooks (JetKVM, TrueNAS websocat), Kea DHCPv4 shared networks (`interface`, `match_code`, `match_data`, `match_encoding` on subnets), BGP neighbor `localasoptions` (os-frr 2.1), radvd `nat64prefixLifetime` and syslog destination `suppress`. Two ACME deploy-hook labels changed.

Changes the static check can't see, read from the core diff and not tested on a firewall:

- `trust_ca`: the 26.7.8 regression that rejected a CA without a private key ("Only a single private key is allowed (found 0 sections)", core #11130) is fixed (874c32d).
- `gateway`: interface-bound dynamic gateways are listed once per address family again, as on 26.7.7 (revert ac08367).
- `interface_assignment`: on 26.7.6 to 26.7.8, saving one assignment marked every interface without a stored `dhcp6-ia-pd-len` as pending, so the module's `reconfigure` reapplied all of them. 26.7.9 fixes the comparison (25c8736) and adds a unit test that exactly one interface is pending after one change (b214361).

A run against `stable/26.7` (core 8dfb0b7, plugins 2340793, both 2026-11-19) with 26.7.9 as the baseline finds no change in anything the collection uses.

## What the 26.7.10 run found

Inputs: the collection at upstream `O-X-L/ansible-opnsense` `latest` (db38431, unchanged since the 26.7.9 run), checked against OPNsense **26.7.10** (released 2026-11-24, core 4092e30, plugins 6f62c20) and diffed against **26.7.9**. The full report is in [reports/report-26.7.10.md](reports/report-26.7.10.md), and the release summary with the module impact is in [reports/summary-26.7.10.md](reports/summary-26.7.10.md). There are 43 errors and 13 warnings. Apart from the release diff, the findings are exactly the same as on 26.7.9. The two fewer warnings are the 26.7.9 release-diff warnings, which are no longer new. Nothing the collection calls was removed or renamed.

The only release-diff entry is an INFO: the `ids_general` pattern matcher `hs` is now labelled "Vectorscan" instead of "Hyperscan". The key is unchanged.

Changes the static check can't see, read from the core diff and not tested on a firewall:

| Module | What changed in 26.7.10 |
|---|---|
| `dhcp_subnet`, `dhcp_reservation` | Kea static reservations registered in Unbound/Dnsmasq now get their domain only from the subnet's `ddns_qualifying_suffix`, no longer from the `domain_name` option (the module's `domain`). Without a suffix they fall back to the system domain. The collection doesn't support `ddns_qualifying_suffix` yet, so it needs an update. |
| `monit_test` | A migration rewrites `failed link` to `link down`. A task that still says `failed link` reports one change after the upgrade. |
| `interface_lagg`, `interface_bridge`, `rule_interface_group`, `alias` (geoip) | Validation fixes. A port in two LAGGs, a GRE/loopback bridge member, a group named like an interface key (`lan`, `optN`) and the GeoIP country `EU` are now rejected. |
| `ids_policy` | A negative `priority` is now rejected (`MinimumValue 0`). |

`stable/26.7` (core = the 26.7.10 tag, plugins f4ad386) has nothing new on top of 26.7.10.

## How it works

1. `tool/opn_snapshot.py` reads the OPNsense sources and writes a JSON snapshot:
   - every API controller (`/api/<module>/<controller>/<action>`), with inherited actions resolved through the class chain, its bound model (`$internalModelClass` / `$internalModelName`), the `getBase/addBase/setBase/...` calls in each action, and whether it has a `__call()` fallback
   - every model XML as a field tree: container / ArrayField / field, type, required, default, and static `OptionValues` with their display labels (option groups included, also the `<optN value="Group label">` form the Unbound blocklist providers use).
2. `tool/oxl_extract.py` imports the collection, which needs `ansible-core` and `httpx`. For each `module_utils/main` class it records `API_MOD/API_CONT/CMDS/API_KEY_PATH*/FIELDS_*`. It also captures each Ansible module's argument spec (choices included) and the inline `{'module', 'controller', 'command'}` calls, expanding choice- or mapping-driven commands and the `service`/`savepoint` tables.
3. `tool/oxl_check.py` matches them up the way the OPNsense router does (`snake_case` → `CamelCase`, controller file names are case-sensitive, actions aren't). It reports:
   - `ENDPOINT_MISSING`: a module/controller/action that doesn't exist
   - `KEY_PATH`: the response or request wrapper key doesn't match what `get`/`getBase`/`addBase`/`setBase` use, or the path isn't in the model
   - `FIELD_MISSING`: a field the module reads or writes that isn't in the model
   - `CHOICE_INVALID`: an argument choice that isn't in the field's `OptionValues`
   - `REQUIRED_NOT_SET`: a required API field without a default that the module never sends
   - `LABEL_MISMATCH`: a `FIELDS_VALUE_MAPPING_RCV` value that is neither an option key nor an option label of the field. For option lists keyed `0..n` the API returns a JSON list and the collection reads the selected entry's display label, so a renamed label means existing entries aren't mapped back and the module reports a change on every run (`ipsec_connection.version` on 26.7.8)
   - `HANDLED_IN_CODE` (a note, not an error or warning): one of the findings above that the collection's own code takes care of, with the reason (see below)
   - `EXTRACT_ERROR`: a part of the collection that `oxl_extract.py` couldn't read, so it wasn't checked. It is an ERROR when a class file or a whole call table (the `service` mapping, the savepoint calls) is missing, and a WARN when only one Ansible module couldn't be loaded (currently the retired `alias_purge`). These are listed first in the report, so a run can't pass while part of the collection was skipped.
   - With `--baseline`: what changed between the two releases in the endpoints and models the collection uses, and whether each finding is new.
     A used field that switches between a plain field and a `ModelRelationField` (in either direction) is a WARN, because the module then sends the wrong kind of value (plain value vs. UUID of the linked entry). Other type, required and default changes stay INFO.
     Removed option values of a used field are a WARN. Changed option labels of a used field are INFO, and a WARN when the class maps that old label in `FIELDS_VALUE_MAPPING_RCV`.

Severity is lowered to WARN wherever the class overrides `search_call`, `get_existing`, `simplify_existing`, `build_request` and so on, because the static view may be wrong there. Those lines end in "verify".

Some of that custom code is recognised, and its findings become `HANDLED_IN_CODE` notes instead:

- Values the Ansible module rewrites before the class sees them: a module-level mapping applied as `MAP[...]` whose keys are the option's choices (`MONTH_MAPPING`, `BL_MAPPING`, `USER_CN_STRICT_MAP`), a mapping of option to the choice that gets blanked with `module.params[..] = ''` (`BLANK_VALUES`, valid when the API field isn't required), and `module.params['x'].upper()`/`.lower()`. The translated values are checked against the API, so a wrong mapping still shows up as `CHOICE_INVALID`.
- Read-side `KEY_PATH` findings when the class lists its entries in its own `search_call()`/`get_existing()` without touching `API_KEY_PATH` (e.g. the IDS classes read `rows` from `search*`).
- Write-side `KEY_PATH` findings when `build_request()` builds the payload under the key the API expects.
- `FIELD_MISSING` for a field the class's own read method fills from other API fields (`simple['value'] = host['mx']`) and that `build_request()` handles, and for the entry key `FIELD_PK` (e.g. a privilege `id`).

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
- Value translations the collection does in code in some other way than the patterns above can still make a `CHOICE_INVALID` a false alarm. Check before fixing.
- Plugins are compared at the same tag as core (`opnsense/plugins` uses matching tags). A box with an older plugin build may differ.
- Field limits aren't part of the snapshot: `MinimumValue`/`MaximumValue`, masks, constraints and model PHP validation. Changes there (on 26.7.10, the `ids_policy` priority minimum and the Monit polling interval range) don't show up in the release diff. The same goes for backend behaviour outside the API, such as how Kea reservations are registered in DNS.
