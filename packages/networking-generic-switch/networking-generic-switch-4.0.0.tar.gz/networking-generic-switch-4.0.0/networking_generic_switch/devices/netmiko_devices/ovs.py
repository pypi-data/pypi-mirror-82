# Copyright 2016 Mirantis, Inc.
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

from networking_generic_switch.devices import netmiko_devices


class OvsLinux(netmiko_devices.NetmikoSwitch):

    PLUG_PORT_TO_NETWORK = (
        'ovs-vsctl set port {port} vlan_mode=access',
        'ovs-vsctl set port {port} tag={segmentation_id}',
    )

    DELETE_PORT = (
        'ovs-vsctl clear port {port} tag',
        'ovs-vsctl clear port {port} trunks',
        'ovs-vsctl clear port {port} vlan_mode'
    )
