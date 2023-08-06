import oci

import os
import subprocess
from time import sleep
from sys import platform
import ctypes

from cloudmesh.abstract.ComputeNodeABC import ComputeNodeABC
from cloudmesh.common.Printer import Printer
from cloudmesh.common.console import Console
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.util import banner
from cloudmesh.common.util import path_expand
from cloudmesh.common.variables import Variables
from cloudmesh.common.DictList import DictList
from cloudmesh.configuration.Config import Config
from cloudmesh.provider import ComputeProviderPlugin
from cloudmesh.secgroup.Secgroup import Secgroup, SecgroupRule
from cloudmesh.common.DateTime import DateTime
from cloudmesh.image.Image import Image
import textwrap


class Provider(ComputeNodeABC, ComputeProviderPlugin):
    kind = "oracle"

    sample = textwrap.dedent("""
    cloudmesh:
      cloud:
        {name}:
          cm:
            active: true
            heading: {name}
            host: TBD
            label: {name}
            kind: oracle
            version: TBD
            service: compute
          default:
            image: ami-0f65671a86f061fcd
            size: t2.micro
          credentials:
            user: {user}
            fingerprint: {fingerprint}
            key_file: ~/.oci/oci_api_key.pem
            pass_phrase: {pass_phrase}
            tenancy: {tenancy}
            compartment_id: {compartment_id}
            region: us-ashburn-1
    """)

    vm_state = [
        'STARTING',
        'RUNNING',
        'STOPPING',
        'STOPPED',
        'UNKNOWN'
    ]

    output = {
        "status": {
            "sort_keys": ["cm.name"],
            "order": ["cm.name",
                      "cm.cloud",
                      "vm_state",
                      "status",
                      "task_state"],
            "header": ["Name",
                       "Cloud",
                       "State",
                       "Status",
                       "Task"]
        },
        "vm": {
            "sort_keys": ["cm.name"],
            "order": ["cm.name",
                      "cm.cloud",
                      "_lifecycle_state",
                      "_lifecycle_state",
                      "task_state",
                      "_image",
                      "_shape",
                      "ip_public",
                      "ip_private",
                      "project_id",
                      "cm.created",
                      "cm.kind"],
            "header": ["Name",
                       "Cloud",
                       "State",
                       "Status",
                       "Task",
                       "Image",
                       "Flavor",
                       "Public IPs",
                       "Private IPs",
                       "Project ID",
                       "Started at",
                       "Kind"],
            "humanize": ["launched_at"]
        },
        "image": {
            "sort_keys": ["cm.name"],
            "order": ["cm.name",
                      "_size_in_mbs",
                      "_lifecycle_state",
                      "cm.driver"],
            "header": ["Name",
                       "Size (MB)",
                       "Status",
                       "Driver"]
        },
        "flavor": {
            "sort_keys": ["cm.name",
                          "vcpus",
                          "disk"],
            "order": ["cm.name",
                      "vcpus",
                      "ram",
                      "disk"],
            "header": ["Name",
                       "VCPUS",
                       "RAM",
                       "Disk"]
        },
        "key": {
            "sort_keys": ["name"],
            "order": ["name",
                      "type",
                      "format",
                      "fingerprint",
                      "comment"],
            "header": ["Name",
                       "Type",
                       "Format",
                       "Fingerprint",
                       "Comment"]
        },
        "secrule": {
            "sort_keys": ["name"],
            "order": ["name",
                      "tags",
                      "direction",
                      "ethertype",
                      "port_range_max",
                      "port_range_min",
                      "protocol",
                      "remote_ip_prefix",
                      "remote_group_id"
                      ],
            "header": ["Name",
                       "Tags",
                       "Direction",
                       "Ethertype",
                       "Port range max",
                       "Port range min",
                       "Protocol",
                       "Range",
                       "Remote group id"]
        },
        "secgroup": {
            "sort_keys": ["name"],
            "order": ["name",
                      "tags",
                      "description",
                      "rules"
                      ],
            "header": ["Name",
                       "Tags",
                       "Description",
                       "Rules"]
        },
        "ip": {
            "order": ["name", 'floating_ip_address', 'fixed_ip_address'],
            "header": ["Name", 'Floating', 'Fixed']
        },
    }

    # noinspection PyPep8Naming
    def Print(self, data, output=None, kind=None):

        if output == "table":
            if kind == "secrule":
                # this is just a temporary fix, both in sec.py and here the
                # secgruops and secrules should be separated
                result = []
                for group in data:
                    # for rule in group['security_group_rules']:
                    #     rule['name'] = group['name']
                    result.append(group)
                data = result

            order = self.output[kind]['order']  # not pretty
            header = self.output[kind]['header']  # not pretty
            # humanize = self.output[kind]['humanize']  # not pretty

            print(Printer.flatwrite(data,
                                    sort_keys=["name"],
                                    order=order,
                                    header=header,
                                    output=output,
                                    # humanize=humanize
                                    )
                  )
        else:
            print(Printer.write(data, output=output))

    @staticmethod
    def _get_credentials(config):
        """
        Internal function to create a dict for the oraclesdk credentials.

        :param config: The credentials from the cloudmesh yaml file
        :return: the dict for the oraclesdk
        """

        d = {'version': '1',
             'user': config['user'],
             'fingerprint': config['fingerprint'],
             'key_file': config['key_file'],
             'pass_phrase': config['pass_phrase'],
             'tenancy': config['tenancy'],
             'compartment_id': config['compartment_id'],
             'region': config['region']}
        return d

    def __init__(self, name=None):
        """
        Initializes the provider. The default parameters are read from the
        configuration file that is defined in yaml format.

        :param name: The name of the provider as defined in the yaml file
        :param configuration: The location of the yaml configuration file
        """

        self.config = Config()
        conf = self.config["cloudmesh"]
        super().__init__(name)

        self.user = self.config["cloudmesh.profile.user"]
        self.spec = conf["cloud"][name]
        self.cloud = name

        self.default = self.spec["default"]
        self.cloudtype = self.spec["cm"]["kind"]

        self.cred = self.config[f"cloudmesh.cloud.{name}.credentials"]

        fields = ["user",
                  "fingerprint",
                  "key_file",
                  "pass_phrase",
                  "tenancy",
                  "compartment_id",
                  "region"]

        for field in fields:
            if self.cred[field] == 'TBD':
                Console.error(
                    f"The credential for Oracle cloud is incomplete. {field} "
                    "must not be TBD")
        self.credential = self._get_credentials(self.cred)

        self.compute = oci.core.ComputeClient(self.credential)
        self.virtual_network = oci.core.VirtualNetworkClient(self.credential)
        self.identity_client = oci.identity.IdentityClient(self.credential)
        self.compartment_id = self.credential["compartment_id"]

        try:
            self.public_key_path = conf["profile"]["publickey"]
            self.key_path = path_expand(
                Config()["cloudmesh"]["profile"]["publickey"])
            f = open(self.key_path, 'r')
            self.key_val = f.read()
        except:
            raise ValueError("the public key location is not set in the "
                             "profile of the yaml file.")

    def update_dict(self, elements, kind=None):
        """
        This function adds a cloudmesh cm dict to each dict in the list
        elements.
        Libcloud
        returns an object or list of objects With the dict method
        this object is converted to a dict. Typically this method is used
        internally.

        :param elements: the list of original dicts. If elements is a single
                         dict a list with a single element is returned.
        :param kind: for some kinds special attributes are added. This includes
                     key, vm, image, flavor.
        :return: The list with the modified dicts
        """

        if elements is None:
            return None
        elif type(elements) == list:
            _elements = elements
        else:
            _elements = [elements]
        d = []
        for entry in _elements:
            if "cm" not in entry:
                entry['cm'] = {}

            if kind == 'ip':
                entry['name'] = entry['_ip_address']

            entry["cm"].update({
                "kind": kind,
                "driver": self.cloudtype,
                "cloud": self.cloud,
                "updated": str(DateTime.now())
            })

            if kind == 'key':
                try:
                    entry['comment'] = entry['public_key'].split(" ", 2)[2]
                except:
                    entry['comment'] = ""
                entry['format'] = \
                    entry['public_key'].split(" ", 1)[0].replace("ssh-", "")

            elif kind == 'vm':
                entry['name'] = entry["cm"]["name"] = entry["_display_name"]
                entry['_image'] = self.compute.get_image(
                    entry['_image_id']).data.display_name

                private = self.get_private_ipobj(entry['_id'])
                if private:
                    details = oci.core.models.GetPublicIpByPrivateIpIdDetails(
                        private_ip_id=private.id)
                    public = self.virtual_network.get_public_ip_by_private_ip_id(
                        details).data
                    if public:
                        entry['ip_public'] = public.ip_address
                    entry['ip_private'] = private.ip_address

                entry["cm"]["created"] = str(entry["_time_created"])
                entry["status"] = entry["cm"]["status"] = str(
                    entry["_lifecycle_state"])

                entry['_launch_options'] = entry['_launch_options'].__dict__
                entry['_source_details'] = entry['_source_details'].__dict__
                entry['_agent_config'] = entry['_agent_config'].__dict__

            elif kind == 'flavor':
                entry['name'] = entry["cm"]["name"] = entry["_shape"]
                entry["cm"]["created"] = str(DateTime.now())

            elif kind == 'image':
                entry['name'] = entry["cm"]["name"] = entry["_display_name"]
                entry["cm"]["created"] = str(DateTime.now())
                entry['_launch_options'] = entry['_launch_options'].__dict__

            elif kind == 'secgroup':
                entry['name'] = entry["cm"]["name"] = entry["_display_name"]

            key_id = "_id"
            if key_id in entry.keys():
                entry["oracle_id"] = entry[key_id]
                entry.pop(key_id)
            d.append(entry)
        return d

    def find(self, elements, name=None):
        """
        Finds an element in elements with the specified name.

        :param elements: The elements
        :param name: The name to be found
        :return:
        """

        for element in elements:
            if element["name"] == name or element["cm"]["name"] == name:
                return element
        return None

    def get_instance(self, name):
        vm_instance = self.compute.list_instances(self.compartment_id,
                                                  display_name=name).data
        if vm_instance:
            return vm_instance[0]
        else:
            return None

    def keys(self):
        """
        Lists the keys on the cloud

        :return: dict
        """
        print("Not supported in oracle cloud")

    def key_upload(self, key=None):
        """
        uploads the key specified in the yaml configuration to the cloud
        :param key:
        :return:
        """
        print("Not supported in oracle cloud")

    def key_delete(self, name=None):
        """
        deletes the key with the given name
        :param name: The name of the key
        :return:
        """
        print("Not supported in oracle cloud")

    def list_secgroups(self, name=None):
        """
        List the named security group

        :param name: The name of the group, if None all will be returned
        :return:
        """
        groups = self.virtual_network.list_network_security_groups(
            self.compartment_id, display_name=name).data

        return self.get_list(
            groups,
            kind="secgroup")

    def list_secgroup_rules(self, name='default'):
        """
        List the named security group

        :param name: The name of the group, if None all will be returned
        :return:
        """
        return self.list_secgroups(name=name)

    def add_secgroup(self, name=None, description=None, vcn_id=None):
        """
        Adds the
        :param name: Name of the group
        :param description: The description
        :return:
        """

        if description is None:
            description = name
        try:
            details = oci.core.models.CreateNetworkSecurityGroupDetails(
                compartment_id=self.compartment_id, display_name=name,
                vcn_id=vcn_id)
            secgroup = self.virtual_network.create_network_security_group(
                details)
            return secgroup.data
        except:
            Console.warning(f"secgroup {name} already exists in cloud. "
                            f"skipping.")

    def add_secgroup_rule(self,
                          name=None,  # group name
                          port=None,
                          protocol=None,
                          ip_range=None):
        """
        Adds the
        :param name: Name of the group
        :param description: The description
        :return:
        """

        try:
            portmin, portmax = port.split(":")
        except:
            portmin = None
            portmax = None
        sec_group = self.list_secgroups(name)
        if sec_group:
            rule_details = oci.core.models.AddSecurityRuleDetails(
                direction='INGRESS', protocol=protocol)
            details = oci.core.models.AddNetworkSecurityGroupSecurityRulesDetails(
                security_rules=[rule_details])
            self.virtual_network.add_network_security_group_security_rules(
                sec_group[0].id, details)
        else:
            print("Security group not found")

    def remove_secgroup(self, name=None):
        """
        Delete the names security group

        :param name: The name
        :return:
        """
        sec_group = self.list_secgroups(name)
        if sec_group:
            self.virtual_network.delete_network_security_group(sec_group[0].id)
            sec_group = self.list_secgroups(name)
        else:
            print("Security group with this name not found")
        return len(sec_group) == 0

    def upload_secgroup(self, name=None):

        cgroups = self.list_secgroups(name)
        group_exists = False
        if len(cgroups) > 0:
            print("Warning group already exists")
            group_exists = True

        groups = Secgroup().list()
        rules = SecgroupRule().list()

        data = {}
        for rule in rules:
            data[rule['name']] = rule

        for group in groups:
            if group['name'] == name:
                break
        print("upload group:", name)

        if not group_exists:
            self.add_secgroup(name=name, description=group['description'])

            for r in group['rules']:
                if r != 'nothing':
                    found = data[r]
                    print("    ", "rule:", found['name'])
                    self.add_secgroup_rule(
                        name=name,
                        port=found["ports"],
                        protocol=found["protocol"],
                        ip_range=found["ip_range"])

        else:

            for r in group['rules']:
                if r != 'nothing':
                    found = data[r]
                    print("    ", "rule:", found['name'])
                    self.add_rules_to_secgroup(
                        name=name,
                        rules=[found['name']])

    def add_rules_to_secgroup(self, name=None, rules=None):

        if name is None and rules is None:
            raise ValueError("name or rules are None")

        cgroups = self.list_secgroups(name)
        if len(cgroups) == 0:
            raise ValueError("group does not exist")

        groups = DictList(Secgroup().list())
        rules_details = DictList(SecgroupRule().list())

        try:
            group = groups[name]
        except:
            raise ValueError("group does not exist")

        for rule in rules:
            try:
                found = rules_details[rule]
                self.add_secgroup_rule(name=name,
                                       port=found["ports"],
                                       protocol=found["protocol"],
                                       ip_range=found["ip_range"])
            except:
                ValueError("rule can not be found")

    def remove_rules_from_secgroup(self, name=None, rules=None):

        if name is None and rules is None:
            raise ValueError("name or rules are None")

        cgroups = self.list_secgroups(name)
        if len(cgroups) == 0:
            raise ValueError("group does not exist")

        groups = DictList(Secgroup().list())
        rules_details = DictList(SecgroupRule().list())

        try:
            group = groups[name]
        except:
            raise ValueError("group does not exist")

        for rule in rules:
            try:
                found = rules_details[rule]
                try:
                    pmin, pmax = rules['ports'].split(":")
                except:
                    pmin = None
                    pmax = None
            except:
                ValueError("rule can not be found")

            for r in cgroups['security_group_rules']:

                test = \
                    r["port_range_max"] == pmin and \
                    r["port_range_min"] == pmax and \
                    r["protocol"] == found["protocol"] and \
                    r["remote_ip_prefix"] == found["ports"]
                # r["direction"] == "egress" \
                # r["ethertype"] == "IPv6" \
                # r["id"] == "1234e4e3-ba72-4e33-9844-..." \
                # r["remote_group_id"]] == null \
                # r["tenant_id"]] == "CH-12345"

                if test:
                    id = r["security_group_id"]
                    list_test = [test]
                    self.virtual_network.remove_network_security_group_security_rules(
                        id,
                        oci.core.models.RemoveNetworkSecurityGroupSecurityRulesDetails(
                            list_test
                        ))

    def get_list(self, d, kind=None, debug=False, **kwargs):
        """
        Lists the dict d on the cloud
        :return: dict or libcloud object
        """

        if self.compute:
            entries = []
            for entry in d:
                entries.append(entry.__dict__)
            return self.update_dict(entries, kind=kind)
        return None

    def images(self, **kwargs):
        """
        Lists the images on the cloud
        :return: dict object
        """
        d = self.compute.list_images(self.compartment_id).data
        return self.get_list(d, kind="image")

    def image(self, name=None):
        """
        Gets the image with a given name
        :param name: The name of the image
        :return: the dict of the image
        """

        img = self.compute.list_images(self.compartment_id, display_name=name)
        return img.data[0]

    def flavors(self):
        """
        Lists the flavors on the cloud

        :return: dict of flavors
        """
        flavor_list = self.compute.list_shapes(self.compartment_id).data
        print(flavor_list)
        return self.get_list(flavor_list, kind="flavor")

    def flavor(self, name=None):
        """
        Gets the flavor with a given name
        :param name: The name of the flavor
        :return: The dict of the flavor
        """

        return self.find(self.flavors(), name=name)

    def start(self, name=None):
        """
        Start a server with the given name

        :param name: A list of node name
        :return:  A list of dict representing the nodes
        """

        vm_instance = self.get_instance(name)

        if vm_instance:
            if self.compute.get_instance(
                vm_instance.id).data.lifecycle_state in 'STOPPED':
                self.compute.instance_action(vm_instance.id, 'START')
        else:
            print("VM instance not found")

    def stop(self, name=None):
        """
        Stop a list of nodes with the given name

        :param name: A list of node name
        :return:  A list of dict representing the nodes
        """

        vm_instance = self.get_instance(name)

        if vm_instance:
            if self.compute.get_instance(
                vm_instance.id).data.lifecycle_state in 'RUNNING':
                self.compute.instance_action(vm_instance.id, 'SOFTSTOP')
        else:
            print("VM instance not found")

    def pause(self, name=None):
        """
        Start a server with the given name

        :param name: A list of node name
        :return:  A list of dict representing the nodes
        """
        print("Pause is not supported in Oracle")

    def unpause(self, name=None):
        """
        Stop a list of nodes with the given name

        :param name: A list of node name
        :return:  A list of dict representing the nodes
        """
        print("Un-Pause is not supported in Oracle")

    def info(self, name=None):
        """
        Gets the information of a node with a given name

        :param name: The name of the virtual machine
        :return: The dict representing the node including updated status
        """
        data = self.get_instance(name)

        if data is None:
            print("VM not found {name}")
            return None

        r = self.update_dict(data.__dict__, kind="vm")
        return r

    def status(self, name=None):

        vm_instance = self.get_instance(name)
        r = self.compute.get_instance(vm_instance.id).data
        return r.lifecycle_state

    def suspend(self, name=None):
        """
        NOT YET IMPLEMENTED.

        suspends the node with the given name.

        :param name: the name of the node
        :return: The dict representing the node
        """
        # same as stopping server instance
        self.stop(name)

    def resume(self, name=None):
        """
        resume a stopped node.

        :param name: the name of the node
        :return: the dict of the node
        """
        vm_instance = self.get_instance(name)
        res = self.compute.instance_action(vm_instance.id, 'START')
        return res

    def list(self):
        """
        Lists the vms on the cloud

        :return: dict of vms
        """
        vm_list = self.compute.list_instances(self.compartment_id).data
        return self.get_list(vm_list, kind="vm")

    def destroy(self, name=None):
        """
        Destroys the node
        :param name: the name of the node
        :return: the dict of the node
        """
        vm_instance = self.get_instance(name)
        servers = None
        if vm_instance and vm_instance.lifecycle_state != 'TERMINATED':
            vnic = self.compute.list_vnic_attachments(
                self.compartment_id, instance_id=vm_instance.id).data[0]

            # Get associated vcn and subnet
            if vnic.lifecycle_state != "DETACHED":
                subnet_id = vnic.subnet_id
                vcn_id = self.virtual_network.get_subnet(
                    vnic.subnet_id).data.vcn_id

            print("Terminating instance...")
            self.compute.terminate_instance(vm_instance.id)

            ins = oci.wait_until(
                self.compute,
                self.compute.get_instance(vm_instance.id),
                'lifecycle_state',
                'TERMINATED',
                max_wait_seconds=300
            ).data

            servers = self.update_dict(ins.__dict__, kind='vm')
            print("Instance terminated.")
            print("Deleting associated resources...")

            if subnet_id:
                self.virtual_network.delete_subnet(subnet_id)

            if vcn_id:
                vcn = self.virtual_network.get_vcn(
                    vcn_id).data

                # Update route table
                self.virtual_network.update_route_table(
                    vcn.default_route_table_id,
                    oci.core.models.UpdateRouteTableDetails(route_rules=[]))

                # Delete gateway
                gateway_id = self.virtual_network.list_internet_gateways(
                    self.compartment_id, vcn_id).data[0].id
                self.virtual_network.delete_internet_gateway(gateway_id)

                # Delete security group
                nsg_id = self.virtual_network.list_network_security_groups(
                    self.compartment_id, vcn_id=vcn.id).data[0].id
                self.virtual_network.delete_network_security_group(nsg_id)
                oci.wait_until(
                    self.virtual_network,
                    self.virtual_network.get_network_security_group(nsg_id),
                    'lifecycle_state',
                    'TERMINATED',
                    succeed_on_not_found=True,
                    max_wait_seconds=300
                )

                # Delete VCN
                self.virtual_network.delete_vcn(vcn_id)
                print("Associated resources deleted")
        else:
            print("VM instance not found")
        return servers

    def reboot(self, name=None):
        """
        Reboot a list of nodes with the given name

        :param name: A list of node name
        :return:  A list of dict representing the nodes
        """

        vm_instance = self.get_instance(name)
        res = self.compute.instance_action(vm_instance.id, 'SOFTRESET')
        return res

    def set_server_metadata(self, name, cm):
        """
        Sets the server metadata from the cm dict

        :param name: The name of the vm
        :param cm: The cm dict
        :return:
        """

        data = {'cm': str(cm)}
        vm_instance = self.get_instance(name)
        self.compute.get_instance(vm_instance.id).data.metadata = data

    def get_server_metadata(self, name):
        vm_instance = self.get_instance(name)
        return vm_instance.metadata

    def delete_server_metadata(self, name, key):
        vm_instance = self.get_instance(name)
        vm_instance.metadata = {}
        return vm_instance.metadata

    def get_availability_domain(self):
        availability_domain = \
            self.identity_client.list_availability_domains(
                self.compartment_id).data[0]
        return availability_domain

    def create_vcn_and_subnet(self, name, availability_domain):
        try:
            # Create a VCN
            vcn_name = 'vcn_' + name
            cidr_block = "11.0.0.0/16"
            vcn_details = oci.core.models.CreateVcnDetails(
                cidr_block=cidr_block, display_name=vcn_name,
                compartment_id=self.compartment_id)
            result = self.virtual_network.create_vcn(vcn_details).data

            vcn = oci.wait_until(
                self.virtual_network,
                self.virtual_network.get_vcn(result.id),
                'lifecycle_state',
                'AVAILABLE',
                max_wait_seconds=300
            ).data
            print('Created VCN')

            # Create a subnet
            subnet_name = 'subnet_' + name
            subnet_cidr_block1 = "11.0.0.0/25"
            result_subnet = self.virtual_network.create_subnet(
                oci.core.models.CreateSubnetDetails(
                    compartment_id=self.compartment_id,
                    availability_domain=availability_domain,
                    display_name=subnet_name,
                    vcn_id=vcn.id,
                    cidr_block=subnet_cidr_block1
                )
            ).data

            subnet = oci.wait_until(
                self.virtual_network,
                self.virtual_network.get_subnet(result_subnet.id),
                'lifecycle_state',
                'AVAILABLE',
                max_wait_seconds=300
            ).data
            print('Created subnet')

            # Create an internet gateway
            result_gateway = self.virtual_network.create_internet_gateway(
                oci.core.models.CreateInternetGatewayDetails(
                    compartment_id=self.compartment_id,
                    display_name='test_gateway',
                    is_enabled=True,
                    vcn_id=vcn.id
                )
            ).data

            gateway = oci.wait_until(
                self.virtual_network,
                self.virtual_network.get_internet_gateway(result_gateway.id),
                'lifecycle_state',
                'AVAILABLE',
                max_wait_seconds=300
            ).data
            print('Created gateway')

            route_rules = [oci.core.models.RouteRule(
                destination='0.0.0.0/0', network_entity_id=result_gateway.id)]

            new_vcn = self.virtual_network.get_vcn(vcn.id).data
            route_table_id = new_vcn.default_route_table_id
            route_table = self.virtual_network.get_route_table(
                route_table_id).data
            self.virtual_network.update_route_table(
                route_table.id,
                                                    oci.core.models.UpdateRouteTableDetails(
                                                        route_rules=route_rules
                                                    ))

            return {'vcn': vcn, 'subnet': subnet}

        except:
            if subnet is not None:
                self.virtual_network.delete_subnet(subnet.id)
            if gateway is not None:
                self.virtual_network.delete_internet_gateway(gateway.id)
            if vcn is not None:
                self.virtual_network.delete_vcn(vcn.id)

    def create(self,
               name=None,
               image=None,
               size=None,
               location=None,
               timeout=360,
               key=None,
               secgroup=None,
               ip=None,
               user=None,
               public=True,
               group=None,
               metadata=None,
               cloud=None,
               **kwargs):
        """
        creates a named node


        :param group: the list of groups the vm belongs to
        :param name: the name of the node
        :param image: the image used
        :param size: the size of the image
        :param timeout: a timeout in seconds that is invoked in case the image
                        does not boot. The default is set to 3 minutes.
        :param kwargs: additional arguments HEADING(c=".")ed along at time of
                       boot
        :return:
        """

        # user is 'opc' for oracle linux and windows based systems and
        # otherwise ubuntu
        if user is None:
            user = Image.guess_username(image)

        '''
        # get IP - no way to assign while creating instance in oracle
        if ip is not None:
            entry = self.list_public_ips(ip=ip, available=True)
            if len(entry) == 0:
                print("ip not available")
                raise ValueError(f"The ip can not be assigned {ip}")
        '''

        if type(group) == str:
            groups = Parameter.expand(group)
        else:
            groups = None

        banner("Create Server")
        print("    Name:    ", name)
        print("    User:    ", user)
        print("    IP:      ", ip)
        print("    Image:   ", image)
        print("    Size:    ", size)
        print("    Public:  ", public)
        print("    Key:     ", key)
        print("    location:", location)
        print("    timeout: ", timeout)
        print("    secgroup:", secgroup)
        print("    group:   ", group)
        print("    groups:  ", groups)
        print()

        try:
            create_instance_details = oci.core.models.LaunchInstanceDetails()
            create_instance_details.compartment_id = self.compartment_id
            availability_domain = self.get_availability_domain()

            vcn_and_subnet = self.create_vcn_and_subnet(
                name,
                                                        availability_domain.name)

            if secgroup is not None:
                # s = self.list_secgroups(secgroup)
                # if (len(s) == 0):
                s = self.add_secgroup(secgroup, secgroup,
                                      vcn_and_subnet['vcn'].id)
                s_id = s.id
            # else:
            # s_id = s[0]['_id']

            create_instance_details.availability_domain = availability_domain.name
            create_instance_details.display_name = name

            if secgroup is not None:
                nsgs = [s_id]
            else:
                nsgs = None

            subnet = vcn_and_subnet['subnet']
            create_instance_details.create_vnic_details = \
                oci.core.models.CreateVnicDetails(
                nsg_ids=nsgs,
                subnet_id=subnet.id,
                assign_public_ip=public
            )

            create_instance_details.image_id = self.image(image).id
            create_instance_details.shape = size

            if os.path.isfile(key):
                key_file = open(key, "r")
                create_instance_details.metadata = {
                    "ssh_authorized_keys": key_file.read()}
            else:
                create_instance_details.metadata = {
                    "ssh_authorized_keys":
                        self.key_val}

            result = self.compute.launch_instance(create_instance_details)
            instance_ocid = result.data.id

            get_instance_response = oci.wait_until(
                self.compute,
                self.compute.get_instance(instance_ocid),
                'lifecycle_state',
                'RUNNING',
                max_wait_seconds=600
            )
            print('Launched instance')

            variables = Variables()
            variables['vm'] = name

        except Exception as e:
            Console.error("Problem starting vm", traceflag=True)
            print(e)
            raise RuntimeError

        vm_instance = self.compute.get_instance(instance_ocid).data.__dict__
        return self.update_dict(vm_instance, kind="vm")[0]

    # ok
    def list_public_ips(self,
                        ip=None,
                        available=False):

        ips = self.virtual_network.list_public_ips("REGION",
                                                   self.compartment_id).data
        if ip is not None:
            for ip_names in ips:
                if ip_names.display_name == ip:
                    ips = [ip_names]
                    break

        if available:
            available_lists = []
            for ip_names in ips:
                if ip_names.lifecycle_state == 'AVAILABLE':
                    available_lists.append(ip_names)
            ips = available_lists

        return self.get_list(ips, kind="ip")

    # ok
    def delete_public_ip(self, ip=None):
        try:
            ips = self.list_public_ips(ip)

            for _ip in ips:
                r = self.virtual_network.delete_public_ip(ip['id'])
        except:
            pass

    # ok
    def create_public_ip(self):
        details = oci.core.models.CreatePublicIpDetails(
            compartment_id=self.compartment_id, display_name="test_ip",
            lifetime="RESERVED")
        return self.virtual_network.create_public_ip(details)

    # ok
    def find_available_public_ip(self):
        ips = self.virtual_network.list_public_ips("REGION",
                                                   self.compartment_id).data
        available = None
        for ip_names in ips:
            if ip_names.lifecycle_state == 'AVAILABLE':
                available = ip_names.ip_address
                break

        return available

    def attach_public_ip(self, name=None, ip=None):
        server = self.get_instance(name)
        private = self.get_private_ipobj(server.id)

        # Delete the already assigned public ip from the instance
        self.detach_public_ip(name, ip)

        # Create new public ip and assign it to the instance
        details = oci.core.models.CreatePublicIpDetails(
            compartment_id=self.compartment_id, lifetime="RESERVED",
            private_ip_id=private.id)
        self.virtual_network.create_public_ip(details)

        return self.get_instance(name)

    def detach_public_ip(self, name=None, ip=None):
        server = self.get_instance(name)
        private = self.get_private_ipobj(server.id)

        # Delete the already assigned public ip from the instance
        if private:
            details = oci.core.models.GetPublicIpByPrivateIpIdDetails(
                private_ip_id=private.id)
            public = self.virtual_network.get_public_ip_by_private_ip_id(
                details).data
            if public:
                # EPHEMERAL public ips are deleted on detaching from server
                if public.lifetime == "EPHEMERAL":
                    self.virtual_network.delete_public_ip(public.id)
                else:
                    # RESERVED public ips can be detached and used later
                    self.virtual_network.update_public_ip(
                        public.id, oci.core.models.UpdatePublicIpDetails(
                            private_ip_id=None
                        ))

    def get_public_ip(self,
                      server=None,
                      name=None):
        ip_public = None
        private = self.get_private_ip(server, name)
        if private:
            details = oci.core.models.GetPublicIpByPrivateIpIdDetails(
                private_ip_id=private)
            public = self.virtual_network.get_public_ip_by_private_ip_id(
                details).data
            if public:
                ip_public = public.ip_address
        return ip_public

    def get_private_ipobj(self, id):
        vnic = self.compute.list_vnic_attachments(
            self.compartment_id, instance_id=id).data[0]
        private = None
        if vnic.lifecycle_state != "DETACHED":
            private = self.virtual_network.list_private_ips(
                subnet_id=vnic.subnet_id).data[0]
        return private

    def get_private_ip(self,
                       server=None,
                       name=None):
        if server is None:
            server = self.get_instance(name)

        if server is None:
            print("Server instance not found")

        private = self.get_private_ipobj(server.id)
        if private:
            private = private.ip_address
        return private

    def console(self, vm=None):
        return self.log(server=vm)

    def log(self, vm=None):
        instance = self.get_instance(vm)
        details = oci.core.models.CaptureConsoleHistoryDetails(
            instance_id=instance.id)
        captured_history = self.compute.capture_console_history(details).data
        oci.wait_until(
            self.compute,
            self.compute.get_console_history(captured_history.id),
            'lifecycle_state',
            'SUCCEEDED',
            max_wait_seconds=600
        )
        return self.compute.get_console_history_content(
            captured_history.id).data

    def rename(self, name=None, destination=None):
        """
        rename a node. NOT YET IMPLEMENTED.

        :param destination
        :param name: the current name
        :return: the dict with the new name
        """
        details = oci.core.models.UpdateInstanceDetails()
        details.display_name = name
        vm_instance = self.get_instance(name)
        self.compute.update_instance(vm_instance.id, details)

    def ssh(self, vm=None, command=None):
        ip = vm['ip_public']
        image = vm['_image']
        key = self.key_path.rpartition('.pub')[0]
        user = Image.guess_username(image)

        if len(ip) == 0:
            Console.error("Public IP address not found")
        if len(key) == 0:
            Console.error("Key not found")

        if command is None:
            command = ""

        if user is None:
            location = ip
        else:
            location = user + '@' + ip
        cmd = "ssh " \
              "-o StrictHostKeyChecking=no " \
              "-o UserKnownHostsFile=/dev/null " \
              f"-i {key} {location} {command}"
        cmd = cmd.strip()
        # VERBOSE(cmd)
        if command == "":
            if platform.lower() == 'win32':
                class disable_file_system_redirection:
                    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
                    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

                    def __enter__(self):
                        self.old_value = ctypes.c_long()
                        self.success = self._disable(
                            ctypes.byref(self.old_value))

                    def __exit__(self, type, value, traceback):
                        if self.success:
                            self._revert(self.old_value)

                with disable_file_system_redirection():
                    os.system(cmd)
            else:
                os.system(cmd)
        else:
            if platform.lower() == 'win32':
                class disable_file_system_redirection:
                    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
                    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

                    def __enter__(self):
                        self.old_value = ctypes.c_long()
                        self.success = self._disable(
                            ctypes.byref(self.old_value))

                    def __exit__(self, type, value, traceback):
                        if self.success:
                            self._revert(self.old_value)

                with disable_file_system_redirection():
                    ssh = subprocess.Popen(cmd,
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            else:
                ssh = subprocess.Popen(cmd,
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            result = ssh.stdout.read().decode("utf-8")
            if not result:
                error = ssh.stderr.readlines()
                print("ERROR: %s" % error)
            else:
                return result

    def wait(self,
             vm=None,
             interval=None,
             timeout=None):
        name = vm['name']
        if interval is None:
            # if interval is too low, OS will block your ip (I think)
            interval = 120
        if timeout is None:
            timeout = 360
        Console.info(
            f"waiting for instance {name} to be reachable: Interval: "
            "{interval}, Timeout: {timeout}")
        timer = 0
        while timer < timeout:
            sleep(interval)
            timer += interval
            try:
                r = self.list()
                r = self.ssh(vm=vm, command='echo IAmReady').strip()
                if 'IAmReady' in r:
                    return True
            except:
                pass

        return False
