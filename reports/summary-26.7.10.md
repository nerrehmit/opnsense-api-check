# OPNsense 26.7.10: what changed and what it means for oxlorg.opnsense

OPNsense 26.7.10 was released on 2026-11-24 (core tag `26.7.10` = 4092e30, plugins tag `26.7.10` = 6f62c20). The collection was checked at upstream `O-X-L/ansible-opnsense` `latest` (db38431, collection version 26.1.11), which is unchanged since the 26.7.9 run.

**Short version: nothing the collection calls was removed or renamed, and no module newly breaks.** The static check finds the same 43 errors and 13 warnings as on 26.7.9 (all of them already known). A few behaviour changes in core affect modules without changing the API. The one that most likely needs a collection update is Kea static reservations and local DNS registration (see below).

## The release in brief

The OPNsense team calls it "business as usual": security advisories, bug fixes and smaller features.

- **DHCP and PPP client reliability:** a series of interface fixes that were tested in public calls for testing (DHCP timeout handling, `newwanip` handling, PPP deferred until boot finishes, PPP uptime option removed).
- **Suricata** uses Vectorscan instead of Hyperscan, as a drop-in replacement. The `hs` pattern matcher key is unchanged, only the label changed.
- **Monit 6.1.0**, with fixes for its incompatibilities and deprecations (`failed link` becomes `link down`, polling interval limited to 1–3600 s, DHCP interfaces allowed in service settings).
- **API keys** can now have a description. They moved to a separate model and controller (`auth/user_api_key`). `auth/user/searchApiKey` and `delApiKey` stay for now and are marked for removal in 27.1.
- **Kea:** less prefix space wasted for IA_NA/IA_PD, and static reservations are registered in local DNS using the subnet's `ddns_qualifying_suffix`.
- **Unbound:** the deprecated blocklistproject (`bla*`, `blp*`, ...) URLs were removed from the template, and an IPv6 misinterpretation in blocklist source nets was fixed.
- **Firewall:** source NAT targets `wan`/`lan`/`optN` (without `ip`) now resolve to the interface network. `firewall_rule_lookup.php` was replaced by an API action, the GeoIP country `EU` was replaced by `XK` (Kosovo), and there are several fixes in GIF, GRE, bridge, LAGG, alias and group validation.
- **Security:** 2 OPNsense advisories (PPP array field validation GHSA-f35q-c34m-pfw3, and stricter firmware subscription/flavour handling GHSA-89wp-xvvm-9pp4), about 25 FreeBSD SAs/ENs, PHP 8.5.13, OpenSSL 3.5.9, NSS 3.133/ca_root_nss 3.134, Kea 3.0.5.
- **Plugins:** os-caddy 2.2.4, os-ddclient 1.34 (adds IONOS), os-firewall-legacy 1.2, os-zabbix-agent 1.20, os-zabbix-proxy 1.18, and os-intrusion-detection-content-et-open 1.0.3 (Suricata 8.0 ruleset, new ET categories).

Full notes: [opnsense/changelog community/26.7/26.7.10](https://github.com/opnsense/changelog/blob/master/community/26.7/26.7.10).

## Static check result

[report-26.7.10.md](report-26.7.10.md): **43 errors, 13 warnings, 158 notes**. Apart from the release diff, the findings are exactly the same as in the 26.7.9 report. Warnings dropped from 15 to 13 only because the 26.7.9 report counted two release-diff warnings (the ACME Selfhost change), and those are no longer new.

Only one change touches an endpoint or model field the collection uses:

| Module | Change | Impact |
|---|---|---|
| `ids_general` | label of `MPMAlgo` option `hs`: `Hyperscan` → `Vectorscan` (INFO) | None. The module sends the key `hs`. Only the `pattern_matcher` description still says "Hyperscan". |

The whole API grew by one controller (`auth/UserApiKey`: `search`, `get`, `set`, `del`) and one model (`OPNsense\Auth\ApiKey`). The collection uses neither.

A run against `stable/26.7` (core = the 26.7.10 tag; plugins f4ad386, 2026-11-24) finds nothing new, so nothing for 26.7.11 has landed yet.

## Behaviour changes the static check can't see

I read these from the core and plugin diffs (26.7.9 → 26.7.10). I haven't tested them on a firewall.

| Module | What changed | What to do |
|---|---|---|
| `dhcp_subnet`, `dhcp_reservation` (Kea DHCPv4) | When local DNS registers DHCP static mappings (Unbound "Register DHCP Static Mappings", or Dnsmasq), a reservation's domain now comes **only** from the subnet's `ddns_qualifying_suffix`. The `domain_name` option no longer counts: that is the subnet's `domain` argument in the collection, or the reservation option. If the suffix is empty, Unbound falls back to the system domain. Reservations in a subnet with a DDNS server (`ddns_dns_server`) are no longer registered locally at all. So a reservation in a subnet with `domain: lab.example` was `host.lab.example` on 26.7.9 and becomes `host.<system domain>` on 26.7.10. | **Collection update needed.** `ddns_qualifying_suffix` is in `dhcp_subnet`'s `FIELDS_NOT_SUPPORTED`, so this can't be fixed from a playbook today. Until then, set the suffix in the GUI. |
| `monit_test` | A migration (Monit model 1.0.15) rewrites `failed link …` conditions to `link down …`, and moves `Custom` tests with a link condition to type `NetworkInterface`. `link up` / `link down` are now recognised conditions, and combining both on one network service is rejected. | A task with `condition: 'failed link'` reports one change after the upgrade and writes the deprecated form back. Use `link down` in playbooks. No code change needed. |
| `interface_lagg` | A variable-shadowing bug meant the check "Members … are already used in other laggs" never fired. It works now. | Tasks that put the same port into two LAGGs now fail, which is correct. No code change. |
| `interface_bridge` | Reversed `str_starts_with()` arguments are fixed, so `gre*` and `lo*` devices are no longer accepted as bridge members. | Tasks that bridge a GRE or loopback interface now get a validation error. |
| `rule_interface_group` | The group name collision check now compares with interface keys (`lan`, `wan`, `optN`) instead of top-level config sections. | A group named like an interface key is now rejected, and names like `system` are now allowed. |
| `alias` (type `geoip`) | Country `EU` (MaxMind "unclassified") was removed and `XK` (Kosovo) was added. | Aliases that list `EU` now fail validation. |
| `ids_policy` | `prio` got `MinimumValue 0`. | A negative `priority` is now rejected by the API. The module has no client-side check, but this is an edge case. |
| `ipsec_psk` | The uniqueness check on local + remote identifier now also runs when only the remote identifier changes (the constraint reference was malformed before). | Only affects real duplicates. |
| `nat_source` | A target of `wan` / `lan` / `optN` without the `ip` suffix now becomes the interface network (`(if:network:0)`). Before, it wasn't resolved. | This is a fix. No change needed. |
| `wireguard_peer`, `wireguard_server` | `toggleClient` / `toggleServer` accept an optional `enabled` argument. | None. The collection only toggles when the state differs. |
| `user` | API keys gained descriptions and their own controller. | None today. A future API-key module should use `auth/user_api_key`, because the `auth/user/*ApiKey` actions go away in 27.1. |

These changes don't touch any collection module: the Monit general polling interval is now 1–3600 s (the collection has no Monit general module), the captive portal zone ID must be unique, os-ddclient added IONOS, os-freeradius added `fallbackvlan_any_service`, the PPP uptime option was removed, and gateway latency/loss threshold constraints were dropped (they never ran). Service stop and similar configd actions are now limited to `wheel,wwwonly`. The API runs as `wwwonly`, so API calls aren't affected.

## Gaps in the checker that this release showed

The snapshot doesn't record `MinimumValue`/`MaximumValue`, masks or constraints. So the `ids_policy` priority minimum and the Monit interval range didn't show up in the release diff. Comparing them with the collection's `INT_VALIDATIONS` and argument defaults would be a small, useful extension.
