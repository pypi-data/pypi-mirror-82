

class Device(object):
    """Generated from OpenAPI schema object #/components/schemas/Device

    A container for emulated protocol devices  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - container_name (str): The unique name of a Port or Lag object that will contain the emulated interfaces and/or devices
    - device_count (int): The number of emulated protocol devices or interfaces per port
     Example: If the device_count is 10 and the choice property value is ethernet then an implementation MUST create 10 ethernet interfaces
     The ethernet property is a container for src, dst and eth_type properties with each on of those properties being a pattern container for 10 possible values
     If an implementation is unable to support the maximum device_count it MUST indicate what the maximum device_count is using the /results/capabilities API
     The device_count is also used by the individual child properties that are a container for a /components/schemas/Device
     Pattern
    - choice (Union[Ethernet, Ipv4, Ipv6, Bgpv4]): The type of emulated protocol interface or device
    """
    _CHOICE_MAP = {
        'Ethernet': 'ethernet',
        'Ipv4': 'ipv4',
        'Ipv6': 'ipv6',
        'Bgpv4': 'bgpv4',
    }
    def __init__(self, name=None, container_name=None, device_count=1, choice=None):
        from abstract_open_traffic_generator.device import Ethernet
        from abstract_open_traffic_generator.device import Ipv4
        from abstract_open_traffic_generator.device import Ipv6
        from abstract_open_traffic_generator.device import Bgpv4
        if isinstance(choice, (Ethernet, Ipv4, Ipv6, Bgpv4)) is False:
            raise TypeError('choice must be of type: Ethernet, Ipv4, Ipv6, Bgpv4')
        self.__setattr__('choice', Device._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Device._CHOICE_MAP[type(choice).__name__], choice)
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(container_name, (str)) is True:
            self.container_name = container_name
        else:
            raise TypeError('container_name must be an instance of (str)')
        if isinstance(device_count, (float, int, type(None))) is True:
            self.device_count = device_count
        else:
            raise TypeError('device_count must be an instance of (float, int, type(None))')


class Ethernet(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Ethernet

    Emulated ethernet protocol  
    A top level in the emulated device stack  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - mac (Pattern): A container for emulated device property patterns
     Media access control address (MAC) is a 48bit identifier for use as a network address
     The value can be an int or a hex string with or without spaces or colons separating each byte
     The min value is 0 or '00:00:00:00:00:00'
     The max value is 281474976710655 or 'FF:FF:FF:FF:FF:FF'
    - mtu (Pattern): A container for emulated device property patterns
    - vlans (list[Vlan]): List of vlans
    """
    def __init__(self, name=None, mac=None, mtu=None, vlans=[]):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(mac, (Pattern, type(None))) is True:
            self.mac = mac
        else:
            raise TypeError('mac must be an instance of (Pattern, type(None))')
        if isinstance(mtu, (Pattern, type(None))) is True:
            self.mtu = mtu
        else:
            raise TypeError('mtu must be an instance of (Pattern, type(None))')
        if isinstance(vlans, (list, type(None))) is True:
            self.vlans = [] if vlans is None else list(vlans)
        else:
            raise TypeError('vlans must be an instance of (list, type(None))')


class Pattern(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Pattern

    A container for emulated device property patterns  

    Args
    ----
    - choice (Union[str, list, Counter, Random]): TBD
    """
    _CHOICE_MAP = {
        'str': 'fixed',
        'list': 'list',
        'Counter': 'counter',
        'Random': 'random',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.device import Counter
        from abstract_open_traffic_generator.device import Random
        if isinstance(choice, (str, list, Counter, Random)) is False:
            raise TypeError('choice must be of type: str, list, Counter, Random')
        self.__setattr__('choice', Pattern._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Pattern._CHOICE_MAP[type(choice).__name__], choice)


class Counter(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Counter

    An incrementing pattern  

    Args
    ----
    - start (str): TBD
    - step (str): TBD
    - up (Union[True, False]): TBD
    """
    def __init__(self, start=None, step=None, up=True):
        if isinstance(start, (str, type(None))) is True:
            self.start = start
        else:
            raise TypeError('start must be an instance of (str, type(None))')
        if isinstance(step, (str, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (str, type(None))')
        if isinstance(up, (bool, type(None))) is True:
            self.up = up
        else:
            raise TypeError('up must be an instance of (bool, type(None))')


class Decrement(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Decrement

    A decrementing pattern  

    Args
    ----
    - start (str): TBD
    - step (str): TBD
    """
    def __init__(self, start=None, step=None):
        if isinstance(start, (str, type(None))) is True:
            self.start = start
        else:
            raise TypeError('start must be an instance of (str, type(None))')
        if isinstance(step, (str, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (str, type(None))')


class Random(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Random

    A repeatable random range pattern  

    Args
    ----
    - min (str): TBD
    - max (str): TBD
    - step (Union[float, int]): TBD
    - seed (str): TBD
    """
    def __init__(self, min=None, max=None, step=None, seed=None):
        if isinstance(min, (str, type(None))) is True:
            self.min = min
        else:
            raise TypeError('min must be an instance of (str, type(None))')
        if isinstance(max, (str, type(None))) is True:
            self.max = max
        else:
            raise TypeError('max must be an instance of (str, type(None))')
        if isinstance(step, (float, int, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (float, int, type(None))')
        if isinstance(seed, (str, type(None))) is True:
            self.seed = seed
        else:
            raise TypeError('seed must be an instance of (str, type(None))')


class Vlan(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Vlan

    Emulated vlan protocol  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - tpid (Pattern): A container for emulated device property patterns
     Vlan tag protocol identifier
    - priority (Pattern): A container for emulated device property patterns
     Vlan priority
    - id (Pattern): A container for emulated device property patterns
     Vlan id
    """
    
    TPID_8100 = '8100'
    TPID_88A8 = '88a8'
    TPID_9100 = '9100'
    TPID_9200 = '9200'
    TPID_9300 = '9300'
    
    def __init__(self, name=None, tpid=None, priority=None, id=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(tpid, (Pattern, type(None))) is True:
            self.tpid = tpid
        else:
            raise TypeError('tpid must be an instance of (Pattern, type(None))')
        if isinstance(priority, (Pattern, type(None))) is True:
            self.priority = priority
        else:
            raise TypeError('priority must be an instance of (Pattern, type(None))')
        if isinstance(id, (Pattern, type(None))) is True:
            self.id = id
        else:
            raise TypeError('id must be an instance of (Pattern, type(None))')


class Ipv4(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Ipv4

    Emulated ipv4 protocol  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - address (Pattern): A container for emulated device property patterns
     The ipv4 address
    - gateway (Pattern): A container for emulated device property patterns
     The ipv4 address of the gateway
    - prefix (Pattern): A container for emulated device property patterns
     The prefix of the ipv4 address
    - ethernet (Ethernet): Emulated ethernet protocol
     A top level in the emulated device stack
    """
    def __init__(self, name=None, address=None, gateway=None, prefix=None, ethernet=None):
        from abstract_open_traffic_generator.device import Pattern
        from abstract_open_traffic_generator.device import Ethernet
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(gateway, (Pattern, type(None))) is True:
            self.gateway = gateway
        else:
            raise TypeError('gateway must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')
        if isinstance(ethernet, (Ethernet, type(None))) is True:
            self.ethernet = ethernet
        else:
            raise TypeError('ethernet must be an instance of (Ethernet, type(None))')


class Ipv6(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Ipv6

    Emulated ipv6 protocol  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - address (Pattern): A container for emulated device property patterns
    - gateway (Pattern): A container for emulated device property patterns
    - prefix (Pattern): A container for emulated device property patterns
    - ethernet (Ethernet): Emulated ethernet protocol
     A top level in the emulated device stack
    """
    def __init__(self, name=None, address=None, gateway=None, prefix=None, ethernet=None):
        from abstract_open_traffic_generator.device import Pattern
        from abstract_open_traffic_generator.device import Ethernet
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(gateway, (Pattern, type(None))) is True:
            self.gateway = gateway
        else:
            raise TypeError('gateway must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')
        if isinstance(ethernet, (Ethernet, type(None))) is True:
            self.ethernet = ethernet
        else:
            raise TypeError('ethernet must be an instance of (Ethernet, type(None))')


class Bgpv4(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Bgpv4

    Emulated bgpv4 protocol  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - as_number_2_byte (Pattern): A container for emulated device property patterns
    - dut_as_number_2_byte (Pattern): A container for emulated device property patterns
    - as_number_4_byte (Pattern): A container for emulated device property patterns
    - as_number_set_mode (Pattern): A container for emulated device property patterns
    - as_type (Union[IBGP, EBGP]): The type of BGP autonomous system
     External BGP (EBGP) is used for BGP links between two or more autonomous systems
     Internal BGP (IBGP) is used within a single autonomous system
    - hold_time_interval (Pattern): A container for emulated device property patterns
    - keep_alive_interval (Pattern): A container for emulated device property patterns
    - graceful_restart (Pattern): A container for emulated device property patterns
    - authentication (Pattern): A container for emulated device property patterns
    - ttl (Pattern): A container for emulated device property patterns
    - dut_ipv4_address (Pattern): A container for emulated device property patterns
    - ipv4 (Ipv4): Emulated ipv4 protocol
    """
    def __init__(self, name=None, as_number_2_byte=None, dut_as_number_2_byte=None, as_number_4_byte=None, as_number_set_mode=None, as_type=None, hold_time_interval=None, keep_alive_interval=None, graceful_restart=None, authentication=None, ttl=None, dut_ipv4_address=None, ipv4=None):
        from abstract_open_traffic_generator.device import Pattern
        from abstract_open_traffic_generator.device import Ipv4
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(as_number_2_byte, (Pattern, type(None))) is True:
            self.as_number_2_byte = as_number_2_byte
        else:
            raise TypeError('as_number_2_byte must be an instance of (Pattern, type(None))')
        if isinstance(dut_as_number_2_byte, (Pattern, type(None))) is True:
            self.dut_as_number_2_byte = dut_as_number_2_byte
        else:
            raise TypeError('dut_as_number_2_byte must be an instance of (Pattern, type(None))')
        if isinstance(as_number_4_byte, (Pattern, type(None))) is True:
            self.as_number_4_byte = as_number_4_byte
        else:
            raise TypeError('as_number_4_byte must be an instance of (Pattern, type(None))')
        if isinstance(as_number_set_mode, (Pattern, type(None))) is True:
            self.as_number_set_mode = as_number_set_mode
        else:
            raise TypeError('as_number_set_mode must be an instance of (Pattern, type(None))')
        if isinstance(as_type, (str, type(None))) is True:
            self.as_type = as_type
        else:
            raise TypeError('as_type must be an instance of (str, type(None))')
        if isinstance(hold_time_interval, (Pattern, type(None))) is True:
            self.hold_time_interval = hold_time_interval
        else:
            raise TypeError('hold_time_interval must be an instance of (Pattern, type(None))')
        if isinstance(keep_alive_interval, (Pattern, type(None))) is True:
            self.keep_alive_interval = keep_alive_interval
        else:
            raise TypeError('keep_alive_interval must be an instance of (Pattern, type(None))')
        if isinstance(graceful_restart, (Pattern, type(None))) is True:
            self.graceful_restart = graceful_restart
        else:
            raise TypeError('graceful_restart must be an instance of (Pattern, type(None))')
        if isinstance(authentication, (Pattern, type(None))) is True:
            self.authentication = authentication
        else:
            raise TypeError('authentication must be an instance of (Pattern, type(None))')
        if isinstance(ttl, (Pattern, type(None))) is True:
            self.ttl = ttl
        else:
            raise TypeError('ttl must be an instance of (Pattern, type(None))')
        if isinstance(dut_ipv4_address, (Pattern, type(None))) is True:
            self.dut_ipv4_address = dut_ipv4_address
        else:
            raise TypeError('dut_ipv4_address must be an instance of (Pattern, type(None))')
        if isinstance(ipv4, (Ipv4, type(None))) is True:
            self.ipv4 = ipv4
        else:
            raise TypeError('ipv4 must be an instance of (Ipv4, type(None))')


class Bgpv4RouteRange(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Bgpv4RouteRange

    Emulated bgpv4 route range  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - address (Pattern): A container for emulated device property patterns
    - prefix (Pattern): A container for emulated device property patterns
    - as_path (Pattern): A container for emulated device property patterns
    - next_hop_address (Pattern): A container for emulated device property patterns
    - aigp_metric (Pattern): A container for emulated device property patterns
    - atomic_aggregate (Pattern): A container for emulated device property patterns
    """
    def __init__(self, name=None, address=None, prefix=None, as_path=None, next_hop_address=None, aigp_metric=None, atomic_aggregate=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')
        if isinstance(as_path, (Pattern, type(None))) is True:
            self.as_path = as_path
        else:
            raise TypeError('as_path must be an instance of (Pattern, type(None))')
        if isinstance(next_hop_address, (Pattern, type(None))) is True:
            self.next_hop_address = next_hop_address
        else:
            raise TypeError('next_hop_address must be an instance of (Pattern, type(None))')
        if isinstance(aigp_metric, (Pattern, type(None))) is True:
            self.aigp_metric = aigp_metric
        else:
            raise TypeError('aigp_metric must be an instance of (Pattern, type(None))')
        if isinstance(atomic_aggregate, (Pattern, type(None))) is True:
            self.atomic_aggregate = atomic_aggregate
        else:
            raise TypeError('atomic_aggregate must be an instance of (Pattern, type(None))')
