# oxlorg.opnsense vs OPNsense 26.7.7

156 module classes and 374 inline calls checked, release diff against 26.1.11.
**50 errors, 41 warnings, 224 notes.**

## New since 26.1.11: errors and warnings (24)

### frr_ospf3_network.Network
- **ERROR** `ENDPOINT_MISSING` CMDS['add']: /api/quagga/ospf6settings/addNetwork: no action 'addNetworkAction' in Ospf6settingsController (controllers/OPNsense/Quagga/Api/Ospf6settingsController.php)
- **ERROR** `ENDPOINT_MISSING` CMDS['del']: /api/quagga/ospf6settings/delNetwork: no action 'delNetworkAction' in Ospf6settingsController (controllers/OPNsense/Quagga/Api/Ospf6settingsController.php)
- **ERROR** `ENDPOINT_MISSING` CMDS['set']: /api/quagga/ospf6settings/setNetwork: no action 'setNetworkAction' in Ospf6settingsController (controllers/OPNsense/Quagga/Api/Ospf6settingsController.php)
- **ERROR** `ENDPOINT_MISSING` CMDS['toggle']: /api/quagga/ospf6settings/toggleNetwork: no action 'toggleNetworkAction' in Ospf6settingsController (controllers/OPNsense/Quagga/Api/Ospf6settingsController.php)
### frr_ospf_general.General
- **ERROR** `FIELD_MISSING` field 'passive_ints' -> 'passiveinterfaces' not in OPNsense\Quagga\OSPF:<root>: reading existing entries will fail or the value is silently ignored
### nat_source.SNat
- **ERROR** `KEY_PATH` 'get' is overridden in SourceNatController and never references ['snatrules', 'rule'] from API_KEY_PATH 'filter.snatrules.rule' - the module will not find its entries in the response
### savepoint filter/cancelRollback
- **ERROR** `ENDPOINT_MISSING` inline call: /api/firewall/filter/cancelRollback: no action 'cancelRollbackAction' in FilterController (controllers/OPNsense/Firewall/Api/FilterController.php)
### savepoint filter/revert
- **ERROR** `ENDPOINT_MISSING` inline call: /api/firewall/filter/revert: no action 'revertAction' in FilterController (controllers/OPNsense/Firewall/Api/FilterController.php)
### savepoint filter/savepoint
- **ERROR** `ENDPOINT_MISSING` inline call: /api/firewall/filter/savepoint: no action 'savepointAction' in FilterController (controllers/OPNsense/Firewall/Api/FilterController.php)
### savepoint one_to_one/cancelRollback
- **ERROR** `ENDPOINT_MISSING` inline call: /api/firewall/one_to_one/cancelRollback: no action 'cancelRollbackAction' in OneToOneController (controllers/OPNsense/Firewall/Api/OneToOneController.php)
### savepoint one_to_one/revert
- **ERROR** `ENDPOINT_MISSING` inline call: /api/firewall/one_to_one/revert: no action 'revertAction' in OneToOneController (controllers/OPNsense/Firewall/Api/OneToOneController.php)
### savepoint one_to_one/savepoint
- **ERROR** `ENDPOINT_MISSING` inline call: /api/firewall/one_to_one/savepoint: no action 'savepointAction' in OneToOneController (controllers/OPNsense/Firewall/Api/OneToOneController.php)
### savepoint source_nat/cancelRollback
- **ERROR** `ENDPOINT_MISSING` inline call: /api/firewall/source_nat/cancelRollback: no action 'cancelRollbackAction' in SourceNatController (controllers/OPNsense/Firewall/Api/SourceNatController.php)
### savepoint source_nat/revert
- **ERROR** `ENDPOINT_MISSING` inline call: /api/firewall/source_nat/revert: no action 'revertAction' in SourceNatController (controllers/OPNsense/Firewall/Api/SourceNatController.php)
### savepoint source_nat/savepoint
- **ERROR** `ENDPOINT_MISSING` inline call: /api/firewall/source_nat/savepoint: no action 'savepointAction' in SourceNatController (controllers/OPNsense/Firewall/Api/SourceNatController.php)
### service iperf/reload
- **ERROR** `ENDPOINT_MISSING` inline call: /api/iperf/service/reconfigure: controller 'iperf/service' does not exist (known: Client, Instance)
### service iperf/restart
- **ERROR** `ENDPOINT_MISSING` inline call: /api/iperf/service/restart: controller 'iperf/service' does not exist (known: Client, Instance)
### service iperf/start
- **ERROR** `ENDPOINT_MISSING` inline call: /api/iperf/service/start: controller 'iperf/service' does not exist (known: Client, Instance)
### service iperf/status
- **ERROR** `ENDPOINT_MISSING` inline call: /api/iperf/service/status: controller 'iperf/service' does not exist (known: Client, Instance)
### frr_bgp_neighbor.Neighbor
- **WARN** `FIELD_MISSING` field 'multi_protocol' -> 'multiprotocol' not in OPNsense\Quagga\BGP:neighbors.neighbor: reading existing entries will fail or the value is silently ignored (class has custom get_existing(): verify)
### frr_ospf3_network.Network
- **WARN** `KEY_PATH` path OPNsense\Quagga\OSPF6:networks.network does not exist in the model (class has custom get_existing(): verify)
### frr_ospf_network.Network
- **WARN** `FIELD_MISSING` field 'area_range' -> 'arearange' not in OPNsense\Quagga\OSPF:networks.network: reading existing entries will fail or the value is silently ignored (class has custom get_existing(): verify)
- **WARN** `FIELD_MISSING` field 'prefix_list_in' -> 'linkedPrefixlistIn' not in OPNsense\Quagga\OSPF:networks.network: reading existing entries will fail or the value is silently ignored (class has custom get_existing(): verify)
- **WARN** `FIELD_MISSING` field 'prefix_list_out' -> 'linkedPrefixlistOut' not in OPNsense\Quagga\OSPF:networks.network: reading existing entries will fail or the value is silently ignored (class has custom get_existing(): verify)

## API changes 26.1.11 -> 26.7.7 in endpoints/models the collection uses (104)

### firewall/d_nat
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'cancelRollback' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'revert' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'savepoint' removed
### firewall/filter
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'cancelRollback' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'revert' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'savepoint' removed
### firewall/one_to_one
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'cancelRollback' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'revert' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'savepoint' removed
### firewall/source_nat
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'cancelRollback' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'revert' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'savepoint' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'setGeneral' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'get' now implemented in OPNsense\Firewall\Api\SourceNatController (was OPNsense\Base\ApiMutableModelControllerBase)
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'set' now implemented in OPNsense\Firewall\Api\SourceNatController (was OPNsense\Base\ApiMutableModelControllerBase)
### frr_bgp_neighbor.Neighbor
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'multiprotocol' removed (module uses it)
### frr_ospf3_interface.Interface
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'area' type 'TextField' -> 'ModelRelationField' (now expects UUIDs of linked entries: plain values sent by the module are rejected)
### frr_ospf_general.General
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'passiveinterfaces' removed (module uses it)
### frr_ospf_interface.Interface
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'area' type 'TextField' -> 'ModelRelationField' (now expects UUIDs of linked entries: plain values sent by the module are rejected)
### frr_ospf_network.Network
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'arearange' removed (module uses it)
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'linkedPrefixlistIn' removed (module uses it)
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'linkedPrefixlistOut' removed (module uses it)
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'area' type 'TextField' -> 'ModelRelationField' (now expects UUIDs of linked entries: plain values sent by the module are rejected)
### quagga/ospf6settings
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'addNetwork' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'delNetwork' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'getNetwork' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'searchNetwork' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'setNetwork' removed
- **WARN** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'toggleNetwork' removed
### acme_validation.Validation
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'dns_freemyip_token' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'dns_gcore_token' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'dns_hostinger_token' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: options of 'dns_service' +['dns_freemyip', 'dns_gcore', 'dns_hostinger']
### bind_record.Record
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: options of 'type' +['NAPTR']
### dhcp_subnet_v4.SubnetV4
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'ping_check' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'subnet_id' added
### dhcrelay_relay.DhcRelayRelay
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'circuit_id' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'remote_id' added
### dnsmasq_general.General
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'expand_hosts' added
### frr_bgp_general.General
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'networks' type 'CSVListField' -> 'NetworkField'
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'routerid' type 'TextField' -> 'NetworkField'
### frr_bgp_neighbor.Neighbor
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'family' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedPrefixlistIn' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedPrefixlistOut' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedRoutemapIn' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedRoutemapOut' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
### frr_bgp_peer_group.PeerGroup
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedPrefixlistIn' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedPrefixlistOut' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedRoutemapIn' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedRoutemapOut' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
### frr_bgp_redistribution.Redistribution
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedRoutemap' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
### frr_bgp_route_map.RouteMap
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'match' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'match2' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'match3' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
### frr_general.General
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'daemons' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'manual_config' added
### frr_ospf3_general.General
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'areas.area' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'networks.network' removed
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'routerid' type 'TextField' -> 'NetworkField'
### frr_ospf3_interface.Interface
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'interfacename' required None -> True
### frr_ospf3_redistribution.Redistribution
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedRoutemap' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
### frr_ospf3_route_map.RouteMap
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'match2' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
### frr_ospf_general.General
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'routerid' type 'TextField' -> 'NetworkField'
### frr_ospf_interface.Interface
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'passive' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'interfacename' required None -> True
### frr_ospf_network.Network
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'ipaddr' type 'TextField' -> 'NetworkField'
### frr_ospf_redistribution.Redistribution
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'linkedRoutemap' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
### frr_ospf_route_map.RouteMap
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'id' required None -> True
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'match2' type 'ModelRelationField' -> '.\\GroupedModelRelationField'
### hasync_general.General
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: options of 'pfsyncversion' +['1500']
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'pfsyncversion' default '1400' -> '1500'
### interface_gif.Gif
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'noclamp' added
### ipsec_child.Child
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'replay_window' added
### monit_alert.Alert
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'format' type 'StrictTextField' -> 'TextField'
### nat_destination.DNat
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'audit' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'created' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'created.description' removed
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'created.time' removed
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'created.username' removed
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'updated.description' removed
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'updated.time' removed
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'updated.username' removed
### nat_one_to_one.OneToOne
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'audit' added
### nat_source.SNat
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'audit' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'endpoint-independent' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'poolopts' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'poolopts_sourcehashkey' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'interface' default 'lan' -> None
### openvpn_server.Server
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'auth-gen-token-secret' type 'StrictTextField' -> 'TextField'
### openvpn_static_key.Key
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: 'key' type 'StrictTextField' -> 'TextField'
### quagga/ospf6settings
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'addArea' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'delArea' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'getArea' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'searchArea' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'setArea' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: action 'toggleArea' added
### rule.Rule
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'audit' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'max-pkt-rate-number' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'max-pkt-rate-seconds' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'received-on' added
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'received-on-not' added
### user.User
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'menu_favorites' added
### wireguard_peer.Peer
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'privkey' added
### wireguard_server.Server
- **INFO** `RELEASE_DIFF` 26.1.11 -> 26.7.7: field 'allowed_ips' added

## Already present with 26.1.11: errors and warnings (38)

### acme_validation.Validation
- **ERROR** `FIELD_MISSING` field 'dns_active24_token' -> 'dns_active24_token' not in OPNsense\AcmeClient\AcmeClient:validations.validation: reading existing entries will fail or the value is silently ignored
### haproxy_cpu.HaproxyCpu
- **ERROR** `CHOICE_INVALID` option 'thread_id' allows ['x0'] which OPNsense\HAProxy\HAProxy:cpus.cpu.thread_id rejects (valid: ['all', 'even', 'odd', 'x1', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x2', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x3', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x4', 'x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x5', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59', 'x6', 'x60', 'x61', 'x62', 'x63', 'x7', 'x8', 'x9'])
### haproxy_fcgi.HaproxyFcgi
- **ERROR** `ENDPOINT_MISSING` CMDS['toggle']: /api/haproxy/settings/toggleFcgi: no action 'toggleFcgiAction' in SettingsController (controllers/OPNsense/HAProxy/Api/SettingsController.php)
### nat_source.SNat
- **ERROR** `CHOICE_INVALID` option 'ip_protocol' allows ['inet46'] which OPNsense\Firewall\Filter:snatrules.rule.ipprotocol rejects (valid: ['inet', 'inet6'])
### openvpn_client.Client
- **ERROR** `CHOICE_INVALID` option 'mode' allows ['dco'] which OPNsense\OpenVPN\OpenVPN:Instances.Instance.dev_type rejects (valid: ['ovpn', 'tap', 'tun'])
### openvpn_server.Server
- **ERROR** `CHOICE_INVALID` option 'mode' allows ['dco'] which OPNsense\OpenVPN\OpenVPN:Instances.Instance.dev_type rejects (valid: ['ovpn', 'tap', 'tun'])
### plugins/modules/frr_diagnostic.py:57 (bgproute)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/bgproute: no action 'bgprouteAction' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### plugins/modules/frr_diagnostic.py:57 (bgproute4)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/bgproute4: no action 'bgproute4Action' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### plugins/modules/frr_diagnostic.py:57 (bgproute6)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/bgproute6: no action 'bgproute6Action' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### plugins/modules/frr_diagnostic.py:57 (generalroute)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/generalroute: no action 'generalrouteAction' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### plugins/modules/frr_diagnostic.py:57 (generalroute4)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/generalroute4: no action 'generalroute4Action' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### plugins/modules/frr_diagnostic.py:57 (generalroute6)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/generalroute6: no action 'generalroute6Action' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### plugins/modules/frr_diagnostic.py:57 (ospfneighbor)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/ospfneighbor: no action 'ospfneighborAction' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### plugins/modules/frr_diagnostic.py:57 (ospfroute)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/ospfroute: no action 'ospfrouteAction' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### plugins/modules/frr_diagnostic.py:57 (ospfv3database)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/ospfv3database: no action 'ospfv3databaseAction' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### plugins/modules/frr_diagnostic.py:57 (ospfv3neighbor)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/ospfv3neighbor: no action 'ospfv3neighborAction' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### plugins/modules/frr_diagnostic.py:57 (ospfv3route)
- **ERROR** `ENDPOINT_MISSING` inline call: /api/quagga/diagnostics/ospfv3route: no action 'ospfv3routeAction' in DiagnosticsController (controllers/OPNsense/Quagga/Api/DiagnosticsController.php)
### service fetchmail/reload
- **ERROR** `ENDPOINT_MISSING` inline call: /api/fetchmail/service/reconfigure: API module 'fetchmail' does not exist
### service fetchmail/restart
- **ERROR** `ENDPOINT_MISSING` inline call: /api/fetchmail/service/restart: API module 'fetchmail' does not exist
### service fetchmail/start
- **ERROR** `ENDPOINT_MISSING` inline call: /api/fetchmail/service/start: API module 'fetchmail' does not exist
### service fetchmail/status
- **ERROR** `ENDPOINT_MISSING` inline call: /api/fetchmail/service/status: API module 'fetchmail' does not exist
### service fetchmail/stop
- **ERROR** `ENDPOINT_MISSING` inline call: /api/fetchmail/service/stop: API module 'fetchmail' does not exist
### service ftp_proxy/reload
- **ERROR** `ENDPOINT_MISSING` inline call: /api/ftpproxy/service/reconfigure: no action 'reconfigureAction' in ServiceController (controllers/OPNsense/FtpProxy/Api/ServiceController.php)
### service ipsec_legacy/reload
- **ERROR** `ENDPOINT_MISSING` inline call: /api/legacy_subsystem/service/applyConfig: API module 'legacy_subsystem' does not exist
### service softether/reload
- **ERROR** `ENDPOINT_MISSING` inline call: /api/softether/service/reconfigure: API module 'softether' does not exist
### service softether/restart
- **ERROR** `ENDPOINT_MISSING` inline call: /api/softether/service/restart: API module 'softether' does not exist
### service softether/start
- **ERROR** `ENDPOINT_MISSING` inline call: /api/softether/service/start: API module 'softether' does not exist
### service softether/status
- **ERROR** `ENDPOINT_MISSING` inline call: /api/softether/service/status: API module 'softether' does not exist
### service softether/stop
- **ERROR** `ENDPOINT_MISSING` inline call: /api/softether/service/stop: API module 'softether' does not exist
### service tinc/status
- **ERROR** `ENDPOINT_MISSING` inline call: /api/tinc/service/status: no action 'statusAction' in ServiceController (controllers/OPNsense/Tinc/Api/ServiceController.php)
### service udp_broadcast_relay/reload
- **ERROR** `ENDPOINT_MISSING` inline call: /api/udpbroadcastrelay/service/reconfigure: no action 'reconfigureAction' in ServiceController (controllers/OPNsense/UDPBroadcastRelay/Api/ServiceController.php)
### interface_lagg.Lagg
- **WARN** `CHOICE_INVALID` option 'lacp_strict' allows ['no', 'yes'] which OPNsense\Interfaces\Lagg:lagg.lacp_strict rejects (valid: ['', '0', '1']) (class has custom update(): verify)
- **WARN** `CHOICE_INVALID` option 'use_flowid' allows ['no', 'yes'] which OPNsense\Interfaces\Lagg:lagg.use_flowid rejects (valid: ['', '0', '1']) (class has custom update(): verify)
### interface_vip.Vip
- **WARN** `CHOICE_INVALID` option 'mode' allows ['other'] which OPNsense\Interfaces\Vip:vip.mode rejects (valid: ['carp', 'ipalias', 'proxyarp']) (class has custom get_existing(): verify)
### unbound_dot.DnsOverTls
- **WARN** `ENDPOINT_MAGIC` CMDS['add']: /api/unbound/settings/addDot: no such action, only reachable through the backwards-compatibility __call() in SettingsController (likely deprecated)
- **WARN** `ENDPOINT_MAGIC` CMDS['del']: /api/unbound/settings/delDot: no such action, only reachable through the backwards-compatibility __call() in SettingsController (likely deprecated)
- **WARN** `ENDPOINT_MAGIC` CMDS['set']: /api/unbound/settings/setDot: no such action, only reachable through the backwards-compatibility __call() in SettingsController (likely deprecated)
- **WARN** `ENDPOINT_MAGIC` CMDS['toggle']: /api/unbound/settings/toggleDot: no such action, only reachable through the backwards-compatibility __call() in SettingsController (likely deprecated)

## Notes: coverage gaps and unverifiable spots (149)

### acme_account.Account
- **INFO** `FIELDS_NOT_SUPPORTED` 4 API field(s) not covered: id, key, statusCode, statusLastUpdate
### acme_action.Action
- **INFO** `CHOICE_NEW` option 'type': API also accepts ['acme_proxmoxbs', 'acme_ruckus', 'acme_truenas_ws', 'acme_zyxel_gs1900', 'configd_reload_caddy']
- **INFO** `FIELDS_NOT_SUPPORTED` 26 API field(s) not covered: acme_proxmoxbs_nodename, acme_proxmoxbs_port, acme_proxmoxbs_realm, acme_proxmoxbs_server, acme_proxmoxbs_tokenid, acme_proxmoxbs_tokenkey, acme_proxmoxbs_user, acme_ruckus_host, acme_ruckus_pass, acme_ruckus_user, acme_synology_dsm_otpcode, acme_truenas_ws_apikey, acme_truenas_ws_hostname, acme_truenas_ws_protocol, acme_truenasws_apikey, acme_truenasws_hostname, acme_truenasws_protocol, acme_zyxel_gs1900_host, acme_zyxel_gs1900_insecure, acme_zyxel_gs1900_password, acme_zyxel_gs1900_reboot, acme_zyxel_gs1900_user, configd, configd_generic_command, id, sftp_modtime
### acme_certificate.Certificate
- **INFO** `FIELDS_NOT_SUPPORTED` 6 API field(s) not covered: certRefId, id, lastUpdate, profile, statusCode, statusLastUpdate
### acme_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 6 API field(s) not covered: UpdateCron, environment, haproxyAclRef, haproxyActionRef, haproxyBackendRef, haproxyServerRef
### acme_validation.Validation
- **INFO** `CHOICE_NEW` option 'dns_service': API also accepts ['dns_freemyip', 'dns_gcore', 'dns_he_ddns', 'dns_hostinger', 'dns_mijnhost', 'dns_scaleway', 'dns_spaceship', 'dns_technitium', 'dns_timeweb', 'dns_websupport', 'dns_zoneedit']
- **INFO** `FIELDS_NOT_SUPPORTED` 37 API field(s) not covered: dns_active24_api_key, dns_active24_api_secret, dns_azuredns_managedidentity, dns_da_insecure, dns_da_key, dns_dh_key, dns_freemyip_token, dns_gcore_token, dns_he_ddns_key, dns_hostinger_token, dns_inws_password, dns_lexicon_provider, dns_lexicon_token, dns_lexicon_user, dns_linode_key, dns_mijnhost_api_key, dns_scaleway_token, dns_sl_account_id, dns_sl_apiver, dns_sl_login_name, dns_sl_password, dns_sl_project_name, dns_sl_token_lifetime, dns_spaceship_api_key, dns_spaceship_api_secret, dns_spaceship_root_domain, dns_technitium_hostname, dns_technitium_token, dns_timeweb_token, dns_transip_token_global_key, dns_websupport_api_key, dns_websupport_api_secret, dns_zoneedit_id, dns_zoneedit_token, enabled, id, tlsalpn_service
### alias.Alias
- **INFO** `CHOICE_NEW` option 'type': API also accepts ['asn', 'authgroup']
- **INFO** `FIELDS_NOT_SUPPORTED` 3 API field(s) not covered: categories, expire, proto
### bind_blocklist.Blocklist
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'block' choices are rewritten by BL_MAPPING before sending, and every translated value is valid
### bind_domain.Domain
- **INFO** `CHOICE_NEW` option 'mode': API also accepts ['forward']
- **INFO** `FIELDS_NOT_SUPPORTED` 4 API field(s) not covered: allowrndctransfer, allowrndcupdate, forwardserver, serial
### bind_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 3 API field(s) not covered: general_log_level, rndcalgo, rndcsecret
### bind_record.Record
- **INFO** `CHOICE_NEW` option 'type': API also accepts ['DNAME', 'HTTPS', 'NAPTR', 'RP', 'SSHFP', 'SVCB']
### cron.CronJob
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: origin
### dhcp_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 5 API field(s) not covered: compatibility, decline_probation_period, manual_config, service_sockets_max_retries, service_sockets_retry_wait_time
### dhcp_reservation_v4.ReservationV4
- **INFO** `FIELDS_NOT_SUPPORTED` 13 API field(s) not covered: client_id, next_server, option, option_data.boot_file_name, option_data.classless_static_route, option_data.domain_name, option_data.domain_name_servers, option_data.domain_search, option_data.ntp_servers, option_data.routers, option_data.static_routes, option_data.tftp_server_name, option_data.time_servers
### dhcp_subnet_v4.SubnetV4
- **INFO** `FIELDS_NOT_SUPPORTED` 30 API field(s) not covered: allocator, ddns_conflict_resolution_mode, ddns_dns_port, ddns_dns_server, ddns_domain_key_algorithm, ddns_domain_key_name, ddns_domain_key_secret, ddns_forward_zone, ddns_override_client_update, ddns_override_no_update, ddns_qualifying_suffix, ddns_reverse_zone, ddns_update_on_renew, match-client-id, option, option_data.boot_file_name, option_data.classless_static_route, option_data.domain_name, option_data.domain_name_servers, option_data.domain_search, option_data.ntp_servers, option_data.routers, option_data.static_routes, option_data.tftp_server_name, option_data.time_servers, option_data.v4_dnr, option_data.v6_only_preferred, ping_check, subnet_id, valid_lifetime
### dhcrelay_relay.DhcRelayRelay
- **INFO** `FIELDS_NOT_SUPPORTED` 3 API field(s) not covered: carp_depend_on, circuit_id, remote_id
### dnsmasq_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 11 API field(s) not covered: dhcp.host_ping, dhcp.log_dhcp, dhcp.log_quiet, dhcp_boot, dhcp_options, dhcp_ranges, dhcp_tags, domainoverrides, expand_hosts, hosts, strip_subnet
### frr_bfd_neighbor.Neighbor
- **INFO** `FIELDS_NOT_SUPPORTED` 6 API field(s) not covered: detect_multiplier, interfacename, localaddress, multihop, receive_interval, transmit_interval
### frr_bgp_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 11 API field(s) not covered: aspaths.aspath, bestpath, communitylists.communitylist, enforce_first_as, maximumpaths, maximumpathsibgp, neighbors.neighbor, peergroups.peergroup, prefixlists.prefixlist, redistributions.redistribution, routemaps.routemap
### frr_bgp_neighbor.Neighbor
- **INFO** `FIELDS_NOT_SUPPORTED` 9 API field(s) not covered: allowas_in, attributeunchanged, bfd_strict, capabilities, family, localas, peergroup, removeprivateas, soft_reconfiguration_inbound
### frr_bgp_peer_group.PeerGroup
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: family
### frr_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 2 API field(s) not covered: fwrules, manual_config
### frr_ospf3_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 8 API field(s) not covered: areas.area, interfaces.interface, originate, originatealways, originatemetric, prefixlists.prefixlist, redistributions.redistribution, routemaps.routemap
### frr_ospf3_interface.Interface
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: bfd
### frr_ospf_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 8 API field(s) not covered: areas.area, interfaces.interface, logadjacencychanges, neighbors.neighbor, networks.network, prefixlists.prefixlist, redistributions.redistribution, routemaps.routemap
### frr_ospf_interface.Interface
- **INFO** `CHOICE_NEW` option 'auth_type': API also accepts ['plain']
- **INFO** `FIELDS_NOT_SUPPORTED` 3 API field(s) not covered: bfd, p2mpoptions, passive
### gateway.Gw
- **INFO** `FIELDS_NOT_SUPPORTED` 3 API field(s) not covered: monitor_killstates, monitor_killstates_priority, nosync
### group.Group
- **INFO** `FIELDS_NOT_SUPPORTED` 2 API field(s) not covered: gid, scope
### haproxy_acl.HaproxyAcl
- **INFO** `CHOICE_NEW` option 'expression': API also accepts ['http_method', 'quic_enabled', 'sc0_clr_gpc0', 'sc0_clr_gpc1', 'sc0_get_gpc0', 'sc0_get_gpc1', 'sc0_get_gpt0', 'sc0_gpc0_rate', 'sc0_gpc1_rate', 'sc0_inc_gpc0', 'sc0_inc_gpc1', 'sc1_clr_gpc', 'sc1_clr_gpc0', 'sc1_clr_gpc1', 'sc1_get_gpc0', 'sc1_get_gpc1', 'sc1_get_gpt0', 'sc1_gpc0_rate', 'sc1_gpc1_rate', 'sc1_inc_gpc0', 'sc1_inc_gpc1', 'sc2_clr_gpc', 'sc2_clr_gpc0', 'sc2_clr_gpc1', 'sc2_get_gpc0', 'sc2_get_gpc1', 'sc2_get_gpt0', 'sc2_gpc0_rate', 'sc2_gpc1_rate', 'sc2_inc_gpc0', 'sc2_inc_gpc1', 'sc_bytes_in_rate', 'sc_bytes_out_rate', 'sc_clr_gpc', 'sc_clr_gpc0', 'sc_clr_gpc1', 'sc_conn_cnt', 'sc_conn_cur', 'sc_conn_rate', 'sc_get_gpc', 'sc_get_gpc0', 'sc_get_gpc1', 'sc_get_gpt', 'sc_get_gpt0', 'sc_glitch_cnt', 'sc_glitch_rate', 'sc_gpc0_rate', 'sc_gpc1_rate', 'sc_gpc_rate', 'sc_http_err_cnt', 'sc_http_err_rate', 'sc_http_fail_cnt', 'sc_http_fail_rate', 'sc_http_req_cnt', 'sc_http_req_rate', 'sc_inc_gpc', 'sc_inc_gpc0', 'sc_inc_gpc1', 'sc_sess_cnt', 'sc_sess_rate', 'src_clr_gpc', 'src_clr_gpc0', 'src_clr_gpc1', 'src_get_gpc', 'src_get_gpc0', 'src_get_gpc1', 'src_get_gpt', 'src_glitch_cnt', 'src_glitch_rate', 'src_gpc0_rate', 'src_gpc1_rate', 'src_gpc_rate', 'src_http_fail_cnt', 'src_http_fail_rate', 'src_inc_gpc', 'src_inc_gpc0', 'src_inc_gpc1', 'stopping', 'var', 'wait_end']
- **INFO** `ENDPOINT_MISSING` CMDS['toggle']: /api/haproxy/settings/toggleAcl: no action 'toggleAclAction' in SettingsController (controllers/OPNsense/HAProxy/Api/SettingsController.php)
- **INFO** `FIELDS_NOT_SUPPORTED` 162 API field(s) not covered: converter, gpc_number, gpt_number, http_method, id, mapfile, queryBackend, sc0_clr_gpc0, sc0_clr_gpc0_comparison, sc0_clr_gpc1, sc0_clr_gpc1_comparison, sc0_get_gpc0, sc0_get_gpc0_comparison, sc0_get_gpc1, sc0_get_gpc1_comparison, sc0_get_gpt0, sc0_get_gpt0_comparison, sc0_gpc0_rate, sc0_gpc0_rate_comparison, sc0_gpc1_rate, sc0_gpc1_rate_comparison, sc0_inc_gpc0, sc0_inc_gpc0_comparison, sc0_inc_gpc1, sc0_inc_gpc1_comparison, sc1_clr_gpc, sc1_clr_gpc0, sc1_clr_gpc0_comparison, sc1_clr_gpc1, sc1_clr_gpc1_comparison, sc1_clr_gpc_comparison, sc1_get_gpc0, sc1_get_gpc0_comparison, sc1_get_gpc1, sc1_get_gpc1_comparison, sc1_get_gpt0, sc1_get_gpt0_comparison, sc1_gpc0_rate, sc1_gpc0_rate_comparison, sc1_gpc1_rate, sc1_gpc1_rate_comparison, sc1_inc_gpc0, sc1_inc_gpc0_comparison, sc1_inc_gpc1, sc1_inc_gpc1_comparison, sc2_clr_gpc, sc2_clr_gpc0, sc2_clr_gpc0_comparison, sc2_clr_gpc1, sc2_clr_gpc1_comparison, sc2_clr_gpc_comparison, sc2_get_gpc0, sc2_get_gpc0_comparison, sc2_get_gpc1, sc2_get_gpc1_comparison, sc2_get_gpt0, sc2_get_gpt0_comparison, sc2_gpc0_rate, sc2_gpc0_rate_comparison, sc2_gpc1_rate, sc2_gpc1_rate_comparison, sc2_inc_gpc0, sc2_inc_gpc0_comparison, sc2_inc_gpc1, sc2_inc_gpc1_comparison, sc_bytes_in_rate, sc_bytes_in_rate_comparison, sc_bytes_out_rate, sc_bytes_out_rate_comparison, sc_clr_gpc, sc_clr_gpc0, sc_clr_gpc0_comparison, sc_clr_gpc1, sc_clr_gpc1_comparison, sc_clr_gpc_comparison, sc_conn_cnt, sc_conn_cnt_comparison, sc_conn_cur, sc_conn_cur_comparison, sc_conn_rate, sc_conn_rate_comparison, sc_get_gpc, sc_get_gpc0, sc_get_gpc0_comparison, sc_get_gpc1, sc_get_gpc1_comparison, sc_get_gpc_comparison, sc_get_gpt, sc_get_gpt0, sc_get_gpt0_comparison, sc_get_gpt_comparison, sc_glitch_cnt, sc_glitch_cnt_comparison, sc_glitch_rate, sc_glitch_rate_comparison, sc_gpc0_rate, sc_gpc0_rate_comparison, sc_gpc1_rate, sc_gpc1_rate_comparison, sc_gpc_rate, sc_gpc_rate_comparison, sc_http_err_cnt, sc_http_err_cnt_comparison, sc_http_err_rate, sc_http_err_rate_comparison, sc_http_fail_cnt, sc_http_fail_cnt_comparison, sc_http_fail_rate, sc_http_fail_rate_comparison, sc_http_req_cnt, sc_http_req_cnt_comparison, sc_http_req_rate, sc_http_req_rate_comparison, sc_inc_gpc, sc_inc_gpc0, sc_inc_gpc0_comparison, sc_inc_gpc1, sc_inc_gpc1_comparison, sc_inc_gpc_comparison, sc_number, sc_sess_cnt, sc_sess_cnt_comparison, sc_sess_rate, sc_sess_rate_comparison, src_clr_gpc0, src_clr_gpc0_comparison, src_clr_gpc1, src_clr_gpc1_comparison, src_get_gpc, src_get_gpc0, src_get_gpc0_comparison, src_get_gpc1, src_get_gpc1_comparison, src_get_gpc_comparison, src_get_gpt, src_get_gpt_comparison, src_glitch_cnt, src_glitch_cnt_comparison, src_glitch_rate, src_glitch_rate_comparison, src_gpc0_rate, src_gpc0_rate_comparison, src_gpc1_rate, src_gpc1_rate_comparison, src_gpc_rate, src_gpc_rate_comparison, src_http_fail_cnt, src_http_fail_cnt_comparison, src_http_fail_rate, src_http_fail_rate_comparison, src_inc_gpc, src_inc_gpc0, src_inc_gpc0_comparison, src_inc_gpc1, src_inc_gpc1_comparison, src_inc_gpc_comparison, table_name, urlparam, value, var, var_comparison, var_value
### haproxy_action.HaproxyAction
- **INFO** `FIELDS_NOT_SUPPORTED` 4 API field(s) not covered: custom, enabled, linkedAcls, testType
- **INFO** `FIELD_MISSING_OPTIONAL` field 'test_type' -> 'test_type' not in OPNsense\HAProxy\HAProxy:actions.action (declared optional)
- **INFO** `FIELD_MISSING_OPTIONAL` field 'linked_acls' -> 'linked_acls' not in OPNsense\HAProxy\HAProxy:actions.action (declared optional)
- **INFO** `FIELD_MISSING_OPTIONAL` field 'custom_rule' -> 'custom_rule' not in OPNsense\HAProxy\HAProxy:actions.action (declared optional)
### haproxy_backend.HaproxyBackend
- **INFO** `CHOICE_NEW` option 'forwarded_header_parameters': API also accepts ['by_port', 'for_port']
- **INFO** `FIELDS_NOT_SUPPORTED` 9 API field(s) not covered: healthCheckProxyProto, id, stickiness_dataTypes, stickiness_glitchRatePeriod, stickiness_gpcElements, stickiness_gpcRatePeriod, stickiness_gptElements, stickiness_httpFailRatePeriod, stickiness_length
### haproxy_cpu.HaproxyCpu
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: id
### haproxy_errorfile.HaproxyErrorfile
- **INFO** `ENDPOINT_MISSING` CMDS['toggle']: /api/haproxy/settings/toggleErrorfile: no action 'toggleErrorfileAction' in SettingsController (controllers/OPNsense/HAProxy/Api/SettingsController.php)
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: id
### haproxy_fcgi.HaproxyFcgi
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: id
### haproxy_frontend.HaproxyFrontend
- **INFO** `CHOICE_NEW` option 'ssl_max_version': API also accepts ['SSLv3']
- **INFO** `CHOICE_NEW` option 'ssl_min_version': API also accepts ['SSLv3']
- **INFO** `FIELDS_NOT_SUPPORTED` 6 API field(s) not covered: id, stickiness_glitchRatePeriod, stickiness_gpcElements, stickiness_gpcRatePeriod, stickiness_gptElements, stickiness_httpFailRatePeriod
- **INFO** `FIELD_MISSING_OPTIONAL` field 'forwarded_header' -> 'forwardedHeader' not in OPNsense\HAProxy\HAProxy:frontends.frontend (declared optional)
### haproxy_general_settings.HaproxyGeneralSettings
- **INFO** `FIELDS_NOT_SUPPORTED` 66 API field(s) not covered: cache.enabled, cache.maxAge, cache.maxObjectSize, cache.maxSecondaryEntries, cache.processVary, cache.totalMaxSize, defaults.customOptions, defaults.init_addr, defaults.maxConnections, defaults.maxConnectionsServers, defaults.redispatch, defaults.retries, defaults.timeoutCheck, defaults.timeoutClient, defaults.timeoutConnect, defaults.timeoutServer, logging.facility, logging.host, logging.length, logging.level, peers.enabled, peers.listen1, peers.listen2, peers.name1, peers.name2, peers.port1, peers.port2, stats.allowedGroups, stats.allowedUsers, stats.authEnabled, stats.customOptions, stats.enabled, stats.port, stats.prometheus_bind, stats.prometheus_enabled, stats.prometheus_path, stats.remoteBind, stats.remoteEnabled, stats.users, storeOcsp, tuning.bogusProxyEnabled, tuning.bufferSize, tuning.customOptions, tuning.h2_initialWindowSize, tuning.h2_initialWindowSizeIncoming, tuning.h2_initialWindowSizeOutgoing, tuning.h2_maxConcurrentStreams, tuning.h2_maxConcurrentStreamsIncoming, tuning.h2_maxConcurrentStreamsOutgoing, tuning.luaMaxMem, tuning.maxConnections, tuning.maxDHSize, tuning.nbthread, tuning.ocspUpdateEnabled, tuning.ocspUpdateMaxDelay, tuning.ocspUpdateMinDelay, tuning.resolversPrefer, tuning.root, tuning.spreadChecks, tuning.sslServerVerify, tuning.ssl_bindOptions, tuning.ssl_cipherList, tuning.ssl_cipherSuites, tuning.ssl_defaultsEnabled, tuning.ssl_maxVersion, tuning.ssl_minVersion
### haproxy_group.HaproxyGroup
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: id
### haproxy_healthcheck.HaproxyHealthcheck
- **INFO** `ENDPOINT_MISSING` CMDS['toggle']: /api/haproxy/settings/toggleHealthcheck: no action 'toggleHealthcheckAction' in SettingsController (controllers/OPNsense/HAProxy/Api/SettingsController.php)
- **INFO** `FIELDS_NOT_SUPPORTED` 4 API field(s) not covered: agentPort, dbUser, force_ssl, smtpDomain
### haproxy_lua.HaproxyLua
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: id
### haproxy_mailer.HaproxyMailer
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: id
### haproxy_maintenance.HaproxyMaintenance
- **INFO** `FIELDS_NOT_SUPPORTED` 5 API field(s) not covered: reloadServiceCron, restartServiceCron, syncCertsCron, updateOcsp, updateOcspCron
### haproxy_mapfile.HaproxyMapfile
- **INFO** `ENDPOINT_MISSING` CMDS['toggle']: /api/haproxy/settings/toggleMapfile: no action 'toggleMapfileAction' in SettingsController (controllers/OPNsense/HAProxy/Api/SettingsController.php)
- **INFO** `FIELDS_NOT_SUPPORTED` 3 API field(s) not covered: id, type, url
### haproxy_resolver.HaproxyResolver
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: id
### haproxy_server.HaproxyServer
- **INFO** `FIELDS_NOT_SUPPORTED` 2 API field(s) not covered: id, sslSNIExpr
### haproxy_user.HaproxyUser
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: id
### hasync_general.General
- **INFO** `CHOICE_NEW` option 'pfsync_version': API also accepts ['1500']
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: pfsyncdefer
### ids_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 10 API field(s) not covered: detect.Profile, detect.toclient_groups, detect.toserver_groups, eveLog.http.dumpAllHeaders, eveLog.http.enable, eveLog.http.extended, eveLog.tls.custom, eveLog.tls.enable, eveLog.tls.extended, eveLog.tls.sessionResumption
- **INFO** `HANDLED_IN_CODE` KEY_PATH: 'set' (generic setAction) expects the payload under 'ids', API_KEY_PATH implies 'general' - handled in code: build_request() builds the payload under 'ids'
- **INFO** `HANDLED_IN_CODE` FIELD_MISSING: field 'profile' -> 'profile' not in OPNsense\IDS\IDS:general - handled in code: the class fills it from other API fields when reading and builds the request itself (build_request)
- **INFO** `HANDLED_IN_CODE` FIELD_MISSING: field 'profile_toclient_groups' -> 'profile_toclient_groups' not in OPNsense\IDS\IDS:general - handled in code: the class fills it from other API fields when reading and builds the request itself (build_request)
- **INFO** `HANDLED_IN_CODE` FIELD_MISSING: field 'profile_toserver_groups' -> 'profile_toserver_groups' not in OPNsense\IDS\IDS:general - handled in code: the class fills it from other API fields when reading and builds the request itself (build_request)
### ids_policy.Policy
- **INFO** `HANDLED_IN_CODE` KEY_PATH: detail 'get_policy' returns {'policy': ...} (getBase) but API_KEY_PATH is 'policies.policy' - handled in code: get_existing, search_call() read(s) the response without API_KEY_PATH
- **INFO** `HANDLED_IN_CODE` KEY_PATH: path OPNsense\IDS\IDS:policies.policy does not exist in the model - handled in code: get_existing, search_call() read(s) the response without API_KEY_PATH
### ids_policy_rule.Rule
- **INFO** `HANDLED_IN_CODE` KEY_PATH: detail 'get_policy_rule' returns {'rule': ...} (getBase) but API_KEY_PATH is 'policies.rule' - handled in code: search_call() read(s) the response without API_KEY_PATH
- **INFO** `HANDLED_IN_CODE` KEY_PATH: path OPNsense\IDS\IDS:rules.rule does not exist in the model - handled in code: search_call() read(s) the response without API_KEY_PATH
### ids_ruleset.Ruleset
- **INFO** `HANDLED_IN_CODE` KEY_PATH: 'list_rulesets' is overridden in SettingsController and never references ['ruleset'] from API_KEY_PATH 'rulesets.ruleset' - handled in code: search_call() read(s) the response without API_KEY_PATH
- **INFO** `HANDLED_IN_CODE` KEY_PATH: path OPNsense\IDS\IDS:ruleset does not exist in the model - handled in code: search_call() read(s) the response without API_KEY_PATH
### ids_user_rule.Rule
- **INFO** `HANDLED_IN_CODE` KEY_PATH: detail 'get_user_rule' returns {'rule': ...} (getBase) but API_KEY_PATH is 'userDefinedRules.rule' - handled in code: get_existing, search_call() read(s) the response without API_KEY_PATH
- **INFO** `HANDLED_IN_CODE` KEY_PATH: path OPNsense\IDS\IDS:userDefinedRules.rule does not exist in the model - handled in code: get_existing, search_call() read(s) the response without API_KEY_PATH
### interface_bridge.Bridge
- **INFO** `ENDPOINT_MISSING` CMDS['toggle']: /api/interfaces/bridge_settings/toggleItem: no action 'toggleItemAction' in BridgeSettingsController (controllers/OPNsense/Interfaces/Api/BridgeSettingsController.php)
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: bridgeif
### interface_gif.Gif
- **INFO** `ENDPOINT_MISSING` CMDS['toggle']: /api/interfaces/gif_settings/toggleItem: no action 'toggleItemAction' in GifSettingsController (controllers/OPNsense/Interfaces/Api/GifSettingsController.php)
- **INFO** `FIELDS_NOT_SUPPORTED` 4 API field(s) not covered: gifif, if, ipaddr, noclamp
### interface_gre.Gre
- **INFO** `ENDPOINT_MISSING` CMDS['toggle']: /api/interfaces/gre_settings/toggleItem: no action 'toggleItemAction' in GreSettingsController (controllers/OPNsense/Interfaces/Api/GreSettingsController.php)
- **INFO** `FIELDS_NOT_SUPPORTED` 3 API field(s) not covered: greif, if, ipaddr
### interface_lagg.Lagg
- **INFO** `CHOICE_NEW` option 'lacp_strict': API also accepts ['0', '1']
- **INFO** `CHOICE_NEW` option 'use_flowid': API also accepts ['0', '1']
### interface_loopback.Loopback
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: deviceId
### interface_vip.Vip
- **INFO** `FIELDS_NOT_SUPPORTED` 3 API field(s) not covered: nosync, subnet, subnet_bits
### interface_vlan.Vlan
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: proto
### interface_vxlan.Vxlan
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: deviceId
### ipsec_auth.BaseAuth
- **INFO** `UNUSED` no Ansible module uses this class; skipped
### ipsec_cert.KeyPair
- **INFO** `FIELDS_NOT_SUPPORTED` 2 API field(s) not covered: keyFingerprint, keySize
### ipsec_child.Child
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: replay_window
### ipsec_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 7 API field(s) not covered: charon.plugins.attr.x_28679, charon.reqid_base, charon.syslog.daemon.chd, charon.syslog.daemon.lib, general.enabled, keyPairs.keyPair, preSharedKeys.preSharedKey
### ipsec_manual_spd.ManualSPD
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: protocol
### monit_service.Service
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: starttimeout
### nat_destination.DNat
- **INFO** `FIELDS_NOT_SUPPORTED` 4 API field(s) not covered: associated-rule-id, audit, category, nosync
### nat_one_to_one.OneToOne
- **INFO** `FIELDS_NOT_SUPPORTED` 2 API field(s) not covered: audit, categories
### nat_source.SNat
- **INFO** `FIELDS_NOT_SUPPORTED` 8 API field(s) not covered: audit, categories, endpoint-independent, nosync, poolopts, poolopts_sourcehashkey, tag, tagged
### neighbor.Neighbor
- **INFO** `ENDPOINT_MISSING` CMDS['toggle']: /api/interfaces/neighbor_settings/toggleItem: no action 'toggleItemAction' in NeighborSettingsController (controllers/OPNsense/Interfaces/Api/NeighborSettingsController.php)
### openvpn_client.Client
- **INFO** `CHOICE_NEW` option 'mode': API also accepts ['ovpn']
- **INFO** `CHOICE_NEW` option 'options': API also accepts ['block-ipv6', 'explicit-exit-notify', 'fast-io']
- **INFO** `FIELDS_NOT_SUPPORTED` 35 API field(s) not covered: auth-gen-token, auth-gen-token-renewal, auth-gen-token-secret, authmode, bridge_gateway, bridge_pool, cert_depth, compress_migrate, crl, data-ciphers, data-ciphers-fallback, dns_domain, dns_domain_search, dns_servers, ifconfig-pool-persist, local_group, maxclients, nopool, ntp_servers, port-share, provision_exclusive, push_excluded_routes, push_inactive, redirect_gateway, register_dns, route_metric, server, server_ipv6, strictusercn, topology, use_ocsp, username_as_common_name, various_push_flags, verify-x509-name, verify_client_cert
### openvpn_server.Server
- **INFO** `CHOICE_NEW` option 'data_cipher_fallback': API also accepts ['AES-128-CBC', 'AES-128-CFB', 'AES-128-CFB1', 'AES-128-CFB8', 'AES-128-OFB', 'AES-192-CBC', 'AES-192-CFB', 'AES-192-CFB1', 'AES-192-CFB8', 'AES-192-GCM', 'AES-192-OFB', 'AES-256-CBC', 'AES-256-CFB', 'AES-256-CFB1', 'AES-256-CFB8', 'AES-256-OFB']
- **INFO** `CHOICE_NEW` option 'data_ciphers': API also accepts ['AES-128-CBC', 'AES-128-CFB', 'AES-128-CFB1', 'AES-128-CFB8', 'AES-128-OFB', 'AES-192-CBC', 'AES-192-CFB', 'AES-192-CFB1', 'AES-192-CFB8', 'AES-192-GCM', 'AES-192-OFB', 'AES-256-CBC', 'AES-256-CFB', 'AES-256-CFB1', 'AES-256-CFB8', 'AES-256-OFB']
- **INFO** `CHOICE_NEW` option 'mode': API also accepts ['ovpn']
- **INFO** `CHOICE_NEW` option 'options': API also accepts ['block-ipv6', 'explicit-exit-notify', 'fast-io']
- **INFO** `CHOICE_NEW` option 'push_options': API also accepts ['block-ipv6', 'explicit-exit-notify']
- **INFO** `FIELDS_NOT_SUPPORTED` 11 API field(s) not covered: bridge_gateway, bridge_pool, carp_depend_on, compress_migrate, http-proxy, password, push_excluded_routes, push_inactive, remote, username, verify-x509-name
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'user_cn_strict' choices are rewritten by USER_CN_STRICT_MAP before sending, and every translated value is valid
### openvpn_static_key.Key
- **INFO** `CHOICE_NEW` option 'mode': API also accepts ['crypt-v2']
### package.Package
- **INFO** `UNUSED` no Ansible module uses this class; skipped
### postfix_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: tlswrappermode
### privilege.Privilege
- **INFO** `HANDLED_IN_CODE` FIELD_MISSING: field 'id' -> 'id' not in OPNsense\Auth\Priv:priv - handled in code: it is the entry key (FIELD_PK) taken from the search response and passed as URL parameter, not a model field
- **INFO** `UNVERIFIED` detail action 'get_item' is custom (no getBase); key path not verified
### rule.Rule
- **INFO** `CHOICE_NEW` option 'icmp_type': API also accepts ['althost', 'dataconv', 'inforep', 'inforeq', 'ipv6-here', 'ipv6-where', 'maskrep', 'maskreq', 'mobredir', 'mobregrep', 'mobregreq', 'skip', 'squench', 'trace']
- **INFO** `FIELDS_NOT_SUPPORTED` 13 API field(s) not covered: audit, categories, icmp6type, max-pkt-rate-number, max-pkt-rate-seconds, nopfsync, nosync, received-on, received-on-not, tcpflags_any, udp-first, udp-multiple, udp-single
### shaper_pipe.Pipe
- **INFO** `CHOICE_NEW` option 'mask': API also accepts ['dst-ip6', 'src-ip6']
- **INFO** `FIELDS_NOT_SUPPORTED` 2 API field(s) not covered: number, origin
### shaper_queue.Queue
- **INFO** `CHOICE_NEW` option 'mask': API also accepts ['dst-ip6', 'src-ip6']
- **INFO** `FIELDS_NOT_SUPPORTED` 2 API field(s) not covered: number, origin
### shaper_rule.Rule
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: origin
### unbound_domain.Domain
- **INFO** `UNUSED` no Ansible module uses this class; skipped
### unbound_dot.DnsOverTls
- **INFO** `CHOICE_NEW` option 'type': API also accepts ['forward']
- **INFO** `FIELDS_NOT_SUPPORTED` 3 API field(s) not covered: description, forward_first, forward_tcp_upstream
### unbound_forward.Forward
- **INFO** `CHOICE_NEW` option 'type': API also accepts ['dot']
- **INFO** `FIELDS_NOT_SUPPORTED` 2 API field(s) not covered: forward_first, verify
### unbound_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 2 API field(s) not covered: safesearch, stats
### unbound_host.Host
- **INFO** `CHOICE_NEW` option 'record_type': API also accepts ['TXT']
- **INFO** `FIELDS_NOT_SUPPORTED` 6 API field(s) not covered: addptr, mx, mxprio, server, ttl, txtdata
- **INFO** `HANDLED_IN_CODE` FIELD_MISSING: field 'prio' -> 'prio' not in OPNsense\Unbound\Unbound:hosts.host - handled in code: the class fills it from other API fields when reading and builds the request itself (build_request)
- **INFO** `HANDLED_IN_CODE` FIELD_MISSING: field 'value' -> 'value' not in OPNsense\Unbound\Unbound:hosts.host - handled in code: the class fills it from other API fields when reading and builds the request itself (build_request)
### user.User
- **INFO** `FIELDS_NOT_SUPPORTED` 7 API field(s) not covered: apikeys, dashboard, menu_favorites, otp_seed, pwd_changed_at, scope, uid
### wazuh_agent.WazuhAgent
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: active_response.repeated_offenders
### webproxy_acl.General
- **INFO** `FIELDS_NOT_SUPPORTED` 3 API field(s) not covered: allowWhitelistBannedHosts, remoteACLs.UpdateCron, remoteACLs.blacklists.blacklist
### webproxy_cache.Cache
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: enabled
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'memory_cache_mode' choices are rewritten by BLANK_VALUES (sent as empty value) before sending, and every translated value is valid
### webproxy_forward.General
- **INFO** `FIELDS_NOT_SUPPORTED` 31 API field(s) not covered: acl.allowWhitelistBannedHosts, acl.allowedSubnets, acl.bannedHosts, acl.blackList, acl.browser, acl.googleapps, acl.mimeType, acl.remoteACLs.UpdateCron, acl.remoteACLs.blacklists.blacklist, acl.safePorts, acl.sslPorts, acl.unrestricted, acl.whiteList, acl.youtube, authentication.authEnforceGroup, authentication.children, authentication.credentialsttl, authentication.method, authentication.realm, icap.EnablePreview, icap.EncodeUsername, icap.OptionsTTL, icap.PreviewSize, icap.RequestURL, icap.ResponseURL, icap.SendClientIP, icap.SendUsername, icap.UsernameHeader, icap.enable, icap.exclude, workers
### webproxy_general.General
- **INFO** `FIELDS_NOT_SUPPORTED` 25 API field(s) not covered: cache.local.cache_linux_packages, cache.local.cache_mem, cache.local.cache_windows_updates, cache.local.directory, cache.local.enabled, cache.local.max_swap_rate, cache.local.maximum_object_size, cache.local.maximum_object_size_in_memory, cache.local.memory_cache_mode, cache.local.size, cache.local.slot_size, cache.local.swap_timeout, parentproxy.enableauth, parentproxy.enabled, parentproxy.host, parentproxy.localdomains, parentproxy.localips, parentproxy.password, parentproxy.port, parentproxy.user, traffic.OverallBandwidthTrotteling, traffic.enabled, traffic.maxDownloadSize, traffic.maxUploadSize, traffic.perHostTrotteling
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'errors' choices are rewritten by BLANK_VALUES (sent as empty value) before sending, and every translated value is valid
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'handling_forwarded_for' choices are rewritten by BLANK_VALUES (sent as empty value) before sending, and every translated value is valid
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'log_target' choices are rewritten by BLANK_VALUES (sent as empty value) before sending, and every translated value is valid
### webproxy_pac_match.Match
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'month_from' choices are rewritten by MONTH_MAPPING before sending, and every translated value is valid
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'month_to' choices are rewritten by MONTH_MAPPING before sending, and every translated value is valid
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'weekday_from' choices are rewritten by WEEKDAY_MAPPING before sending, and every translated value is valid
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'weekday_to' choices are rewritten by WEEKDAY_MAPPING before sending, and every translated value is valid
### webproxy_pac_proxy.Proxy
- **INFO** `HANDLED_IN_CODE` CHOICE_INVALID: option 'type' choices are rewritten by .upper() before sending, and every translated value is valid
### webproxy_pac_rule.Rule
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: enabled
### webproxy_remote_acl.Acl
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: enabled
### wireguard_peer.Peer
- **INFO** `FIELDS_NOT_SUPPORTED` 1 API field(s) not covered: privkey
### wireguard_server.Server
- **INFO** `FIELDS_NOT_SUPPORTED` 5 API field(s) not covered: allowed_ips, debug, endpoint, instance, peer_dns
