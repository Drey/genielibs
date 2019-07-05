'''Implementation for Interface unconfigconfig triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig
from genie.libs.sdk.triggers.unconfigconfig.interface.unconfigconfig import \
    TriggerUnconfigConfigEthernetInterface as UncfgCfgInterface

# import ats
from ats.utils.objects import Not, NotExists

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'bandwidth', 'load_interval',
                     'port_speed', 'in_crc_errors', 'in_errors',
                     'in_discards', '(Tunnel.*)', 'accounting']



class TriggerUnconfigConfigPhysicalTrunkInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned physical trunk interface(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned physical trunk interface(s).

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                interface: `str`
                port_channel_int: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Interface Ops object and store the "up" physical trunk interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned physical trunk interface(s) from step 1
           with Interface Conf object
        4. Verify the learned physical trunk interface(s) are "down"
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>\w+Ethernet[\d\/\.]+)',
                                                        'switchport_mode', 'trunk'],
                                                       ['info', '(?P<interface>\w+Ethernet[\d\/\.]+)',
                                                        'port_channel', 'port_channel_int', '(?P<port_channel_int>.*)']],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'port_channel',
                                                        'port_channel_member', False],
                                                       ['info', '(?P<interface>.*)', 'mac_address', '([\w\.]+)'],
                                                       ['info', '(?P<interface>.*)', '(.*)'],
                                                       ['info', '(?P<port_channel_int>.*)', 'port_channel', 'port_channel_member_intfs', '(.*)'],
                                                       ['info', '(Port-channel.*)', 'mac_address', '(.*)'],
                                                       ['info', '(Port-channel.*)', 'phys_address', '(.*)']],
                                       'exclude': interface_exclude}},
                      num_values={'interface':1})



class TriggerUnconfigConfigEthernetInterface(UncfgCfgInterface):
    """Unconfigure and reapply the whole configurations of dynamically learned ethernet interface(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned ethernet interface(s).

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                interface: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Interface Ops object and store the "up" ethernet interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned ethernet interface(s) from step 1
           with Interface Conf object
        4. Verify the learned ethernet interface(s) are "down"
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<interface>\w+Ethernet[0-9\/]+$)', 'enabled', True],
                                                        ['info', '(?P<interface>.*)', 'port_channel', 'port_channel_member', False],
                                                        ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                        'exclude': interface_exclude,
                                        'include_management_interface': False}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<interface>.*)', NotExists('access_vlan')],
                                                        ['info', '(?P<interface>.*)', 'switchport_enable', False],
                                                        ['info', '(?P<interface>.*)', NotExists('switchport_mode')],
                                                        ['info', '(?P<interface>.*)', NotExists('trunk_vlans')],
                                                        ['info', '(?P<interface>.*)', NotExists('vrf')],
                                                        ['info', '(?P<interface>.*)', 'enabled', False],
                                                        ['info', '(?P<interface>.*)', NotExists('duplex_mode')],
                                                        ['info', '(?P<interface>.*)', NotExists('mac_address')],
                                                        ['info', '(?P<interface>.*)', 'oper_status', '(.*down.*)']],
                                        'exclude': interface_exclude +\
                                                   [UncfgCfgInterface.remove_related_subinterface]}},
                      num_values={'interface': 1})


class TriggerUnconfigConfigEthernetInterfaceSub(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned
        Giga/giga/Ethernet/ethernet interface(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned
                        Giga/giga/Ethernet/ethernet interface(s).

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                interface: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Interface Ops object and store the "up" GigabitEthernet|gigabitEthernet|Ethernet|ethernet interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned GigabitEthernet|gigabitEthernet|Ethernet|ethernet interface(s) from step 1
           with Interface Conf object
        4. Verify the learned those interface(s) are "down"
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<interface>(GigabitEthernet|gigabitEthernet|Ethernet|ethernet)[0-9\/]+\.[0-9]+)',
                                                         'enabled', True],
                                                        ['info', '(?P<interface>(GigabitEthernet|gigabitEthernet|Ethernet|ethernet)[0-9\/]+\.[0-9]+)',
                                                         'oper_status', 'up']],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<interface>.*)','enabled', False]],
                                        'exclude': interface_exclude}},
                      num_values={'interface': 1})


class TriggerUnconfigConfigVirtualTrunkInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned virtual trunk interface(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned virtual trunk interface(s).

        trigger_datafile:
            Mandatory:
                timeout:
                    max_time (`int`): Maximum wait time for the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15
                    method (`str`): Method to recover the device configuration,
                                  Support methods:
                                    'checkpoint': Rollback the configuration by
                                                  checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config file on disk (iosxr)
            Optional:
                tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                     restored to the reference rate,
                                     in second. Default: 60
                tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                   in second. Default: 10
                timeout_recovery:
                    Buffer recovery timeout make sure devices are recovered at the end
                    of the trigger execution. Used when previous timeouts have been exhausted.

                    max_time (`int`): Maximum wait time for the last step of the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15
                static:
                    The keys below are dynamically learnt by default.
                    However, they can also be set to a custom value when provided in the trigger datafile.

                    interface: `str`

                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                          OR
                          interface: 'Ethernet1/1/1' (Specific value)
        steps:
            1. Learn Interface Ops object and store the "up" port-channel interface(s)
               if has any, otherwise, SKIP the trigger
            2. Save the current device configurations through "method" which user uses
            3. Unconfigure the learned port-channel interface(s) from step 1
               with Interface Conf object
            4. Verify the learned port-channel interface(s) no longer exists
            5. Recover the device configurations to the one in step 2
            6. Learn Interface Ops again and verify it is the same as the Ops in step 1

        """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>[p|P]ort-channel[\d\.]+)',
                                                        'switchport_mode', 'trunk'],
                                                       ['info', '(?P<interface>[p|P]ort-channel[\d\.]+)',
                                                        'port_channel', 'port_channel_member', False]],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<interface>.*)')]],
                                       'exclude': interface_exclude}},
                      num_values={'interface':1})
