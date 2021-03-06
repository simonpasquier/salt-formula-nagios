# -*- coding: utf-8 -*-

from netaddr import IPNetwork, IPAddress


def alarm_to_service(host, alarm_id, alarm, check_command, threshold, default=None):
    """
    Return a dictinnary representing a Nagios service from an alarm definition.
    The service properties are enforced to activate passive check and turn on the
    freshness pattern.
    """
    if default is None:
        default = {}

    notifications_enabled = 0
    alerting = alarm.get('alerting', 'enabled')
    if alerting == 'enabled_with_notification':
        notifications_enabled = 1

    service = {
        'service_description': alarm_id,
        'host_name': host,
        'notifications_enabled': notifications_enabled,
        'freshness_threshold': threshold,
        'check_command': check_command,
        'passive_checks_enabled': 1,
        'active_checks_enabled': 0,
        'check_freshness': 1,
    }
    service.update(default)
    return {host + alarm_id: service }


def alarm_cluster_to_service(host, alarm_id, alarm, check_command, threshold, default=None):
    """
    Return a dictinnary representing a Nagios service from an alarm_custer
    definition.
    The service properties are enforced to activate passive check and turn on the
    freshness pattern.
    """
    if default is None:
        default = {}

    notifications_enabled = 1
    alerting = alarm.get('alerting', 'enabled_with_notification')
    if alerting != 'enabled_with_notification':
        notifications_enabled = 0

    service = {
        'service_description': alarm_id,
        'host_name': host,
        'notifications_enabled': notifications_enabled,
        'freshness_threshold': threshold,
        'check_command': check_command,
        'passive_checks_enabled': 1,
        'active_checks_enabled': 0,
        'check_freshness': 1,
    }
    service.update(default)
    return {host + alarm_id: service }


def threshold(alarm, triggers, delay=10):
    """
    Return the freshness_threshold for a Nagios service based on the maximum
    window used by triggers.
    An additional delay is applied to prevent flapping when collectors
    are (re)started.
    """

    window = 10
    for trigger in alarm.get('triggers', []):
        if trigger in triggers:
            for rule in triggers[trigger].get('rules', []):
                if rule.get('window', 0) > window:
                    window = int(rule.get('window'))

    return window + delay


def alarm_cluster_hostname(dimension_key, alarm, default_hostname, suffix=None):
    """
    Return the associated Nagios host_name of an alarm_cluster.
    """

    suffix = '.' + suffix if suffix else ''

    for key, value in alarm.get('dimension', {}).items():
        if key == dimension_key:
            return value + suffix

    return default_hostname + suffix


def host_address(networks, addresses):
    """
    Return the IP address which belongs to a network
    """

    if isinstance(networks, basestring):
        networks = [networks]

    for net in networks:
        for addr in addresses:
            try:
                if IPAddress(addr) in IPNetwork(net):
                    return addr
            except: pass
    return

