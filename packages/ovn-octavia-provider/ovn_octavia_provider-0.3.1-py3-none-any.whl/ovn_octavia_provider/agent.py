#    Copyright 2020 Red Hat, Inc. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log as logging

from ovn_octavia_provider.common import config as ovn_conf
from ovn_octavia_provider import event as ovn_event
from ovn_octavia_provider import helper as ovn_helper
from ovn_octavia_provider.ovsdb import impl_idl_ovn

ovn_conf.register_opts()

LOG = logging.getLogger(__name__)

OVN_EVENT_LOCK_NAME = "neutron_ovn_octavia_event_lock"


def OvnProviderAgent(exit_event):

    helper = ovn_helper.OvnProviderHelper()
    events = [ovn_event.LogicalRouterPortEvent(helper),
              ovn_event.LogicalSwitchPortUpdateEvent(helper)]

    # NOTE(mjozefcz): This API is only for handling OVSDB events!
    ovn_nb_idl_for_events = impl_idl_ovn.OvnNbIdlForLb(
        event_lock_name=OVN_EVENT_LOCK_NAME)
    ovn_nb_idl_for_events.notify_handler.watch_events(events)
    ovn_nb_idl_for_events.start()

    LOG.info('OVN provider agent has started.')
    exit_event.wait()
    LOG.info('OVN provider agent is exiting.')
    ovn_nb_idl_for_events.notify_handler.unwatch_events(events)
    ovn_nb_idl_for_events.stop()
