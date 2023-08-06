import ipaddress
import os
import re

from cloudshell.devices.autoload.autoload_builder import AutoloadDetailsBuilder

from cloudshell.f5.autoload.snmp_if_table import SnmpIfTable


class AbstractF5GenericSNMPAutoload(object):
    VENDOR = "F5"
    SNMP_ERRORS = [r"No\s+Such\s+Object\s+currently\s+exists"]

    @property
    def root_model_class(self):
        raise NotImplementedError(
            "Class {} must implement property 'root_model_class'".format(type(self))
        )

    @property
    def chassis_model_class(self):
        raise NotImplementedError(
            "Class {} must implement property 'chassis_model_class'".format(type(self))
        )

    @property
    def port_model_class(self):
        raise NotImplementedError(
            "Class {} must implement property 'port_model_class'".format(type(self))
        )

    @property
    def power_port_model_class(self):
        raise NotImplementedError(
            "Class {} must implement property 'power_port_model_class'".format(
                type(self)
            )
        )

    def __init__(self, snmp_handler, shell_name, shell_type, resource_name, logger):
        """Init command.

        :param snmp_handler:
        :param logger:
        :return:
        """
        self.snmp_handler = snmp_handler
        self.shell_name = shell_name
        self.shell_type = shell_type
        self.resource_name = resource_name
        self.logger = logger
        self.elements = {}
        self.snmp_handler.set_snmp_errors(self.SNMP_ERRORS)
        self.resource = self.root_model_class(
            shell_name=shell_name,
            shell_type=shell_type,
            name=resource_name,
            unique_id=resource_name,
        )

    def discover(self, supported_os):
        """General entry point for autoload.

        Reads device structure and attributes: chassis, modules, submodules,
        ports, port-channels and power supplies
        :return: AutoLoadDetails object
        """
        if not self._is_valid_device_os(supported_os):
            raise Exception(self.__class__.__name__, "Unsupported device OS")

        self.logger.info("*" * 70)
        self.logger.info("Start SNMP discovery process .....")

        self._load_f5_mib()
        self._build_resources()

        autoload_details = AutoloadDetailsBuilder(self.resource).autoload_details()
        self._log_autoload_details(autoload_details)
        return autoload_details

    def _build_resources(self):
        """Discover and create all needed resources.

        :return:
        """
        self._get_device_details()
        self._get_chassis_attributes()
        self._get_power_ports()
        self._get_ports()

    def _load_f5_mib(self):
        """Loads f5 specific mibs inside snmp handler."""
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mibs"))
        self.snmp_handler.update_mib_sources(path)
        self.snmp_handler.load_mib(["F5-BIGIP-SYSTEM-MIB"])

    def _log_autoload_details(self, autoload_details):
        """Logging autoload details.

        :param autoload_details:
        :return:
        """
        self.logger.debug("-------------------- <RESOURCES> ----------------------")
        for resource in autoload_details.resources:
            self.logger.debug(
                "{0:15}, {1:20}, {2}".format(
                    resource.relative_address, resource.name, resource.unique_identifier
                )
            )
        self.logger.debug("-------------------- </RESOURCES> ----------------------")

        self.logger.debug("-------------------- <ATTRIBUTES> ---------------------")
        for attribute in autoload_details.attributes:
            self.logger.debug(
                "-- {0:15}, {1:60}, {2}".format(
                    attribute.relative_address,
                    attribute.attribute_name,
                    attribute.attribute_value,
                )
            )
        self.logger.debug("-------------------- </ATTRIBUTES> ---------------------")

    def _is_valid_device_os(self, supported_os):
        """Validate device OS using snmp.

        :return: True or False
        """
        system_description = self.snmp_handler.get_property(
            "SNMPv2-MIB", "sysDescr", "0"
        )
        self.logger.debug(
            "Detected system description: '{0}'".format(system_description)
        )
        result = re.search(
            r"({0})".format("|".join(supported_os)),
            system_description,
            flags=re.DOTALL | re.IGNORECASE,
        )

        if result:
            return True
        else:
            error_message = (
                "Incompatible driver! Please use this driver for '{0}' "
                "operation system(s)".format(str(tuple(supported_os)))
            )
            self.logger.error(error_message)
            return False

    def _get_device_model(self):
        """Get device model from the SNMPv2 mib.

        :return: device model
        :rtype: str
        """
        return self.snmp_handler.get_property("SNMPv2-MIB", "sysObjectID", "0")

    def _get_device_model_name(self):
        """Get device model name from the CSV file map.

        :return: device model model
        :rtype: str
        """
        return self.snmp_handler.get_property(
            "F5-BIGIP-SYSTEM-MIB", "sysPlatformInfoMarketingName", "0"
        )

    def _get_device_os_version(self):
        """Get device OS Version form snmp SNMPv2 mib.

        :return: device model
        :rtype: str
        """
        os_table = self.snmp_handler.get_table(
            "F5-BIGIP-SYSTEM-MIB", "sysSwStatusActive"
        )
        active_os_index = [
            k
            for k, v in os_table.iteritems()
            if "true" in v.get("sysSwStatusActive", "")
        ][-1]
        if active_os_index:
            # For some reason pysnmp cannot convert "F5-BIGIP-SYSTEM-MIB",
            # "sysSwStatusVersion" , active_os_index
            return self.snmp_handler.get_table_field(
                ("1.3.6.1.4.1.3375.2.1.9.4.2.1.4." + active_os_index)
            ).get("sysSwStatusVersion")

    def _get_device_details(self):
        """Get root element attributes."""
        self.logger.info("Building Root")

        self.resource.contact_name = self.snmp_handler.get_property(
            "SNMPv2-MIB", "sysContact", "0"
        )
        self.resource.system_name = self.snmp_handler.get_property(
            "SNMPv2-MIB", "sysName", "0"
        )
        self.resource.location = self.snmp_handler.get_property(
            "SNMPv2-MIB", "sysLocation", "0"
        )
        self.resource.os_version = self._get_device_os_version()
        self.resource.model = self._get_device_model()
        self.resource.model_name = self._get_device_model_name()
        self.resource.vendor = self.VENDOR

    def _add_element(self, relative_path, resource, parent_id=""):
        """Add object data to resources and attributes lists.

        :param resource: object which contains all required data for certain resource
        """
        rel_seq = relative_path.split("/")

        if len(rel_seq) == 1:  # Chassis connected directly to root
            self.resource.add_sub_resource(relative_path, resource)
        else:
            if parent_id:
                parent_object = self.elements.get(parent_id, self.resource)
            else:
                parent_object = self.elements.get("/".join(rel_seq[:-1]), self.resource)

            rel_path = re.search(r"\d+", rel_seq[-1]).group()
            parent_object.add_sub_resource(rel_path, resource)

        self.elements.update({relative_path: resource})

    def _get_chassis_attributes(self):
        """Get Chassis element attributes."""
        self.logger.info("Building Chassis")

        chassis_table = self.snmp_handler.get_table(
            "F5-BIGIP-SYSTEM-MIB", "sysChassisSlotTable"
        )
        if not chassis_table:
            chassis_table["0"] = {}

        for chassis in chassis_table:
            chassis_object = self.chassis_model_class(
                shell_name=self.shell_name,
                name="Chassis {}".format(chassis),
                unique_id="{}.{}.{}".format(self.resource_name, "chassis", chassis),
            )

            chassis_object.model = self.snmp_handler.get_property(
                "F5-BIGIP-SYSTEM-MIB", "sysGeneralHwName", 0
            )
            chassis_object.serial_number = chassis_table[chassis].get(
                "sysChassisSlotSerialNumber"
            ) or self.snmp_handler.get_property(
                "F5-BIGIP-SYSTEM-MIB", "sysGeneralChassisSerialNum", 0
            )

            relative_address = "{0}".format(chassis)

            self._add_element(relative_path=relative_address, resource=chassis_object)

            self.logger.info("Added Chassis {}".format(chassis))
        self.logger.info("Building Chassis completed")

    def _get_power_ports(self):
        """Get attributes for power ports provided in self.power_supply_list.

        :return:
        """
        self.logger.info("Building PowerPorts")
        power_port_dict = self.snmp_handler.get_table(
            "F5-BIGIP-SYSTEM-MIB", "sysChassisPowerSupplyIndex"
        )
        for power_port in power_port_dict.keys():
            power_port_id = power_port_dict[power_port].get(
                "sysChassisPowerSupplyIndex"
            )
            if power_port_id:
                chassis_id = "0"
                relative_address = "{0}/PP{1}".format(chassis_id, power_port_id)

                power_port = self.power_port_model_class(
                    shell_name=self.shell_name,
                    name="PP{0}".format(power_port_id),
                    unique_id="{0}.{1}.{2}".format(
                        self.resource_name, "power_port", power_port_id
                    ),
                )

                self._add_element(
                    relative_path=relative_address,
                    resource=power_port,
                    parent_id=chassis_id,
                )

                self.logger.info("Added Power Port {}".format(power_port_id))

        self.logger.info("Building Power Ports completed")

    def _get_ports(self):
        """Get resource details and attributes for every port in self.port_list.

        :return:
        """
        self.logger.info("Load Ports:")
        duplex_table = self.snmp_handler.get_table(
            "F5-BIGIP-SYSTEM-MIB", "sysInterfaceMediaMaxDuplex"
        )
        lldp_table = self.snmp_handler.get_table(
            "F5-BIGIP-SYSTEM-MIB", "sysLldpNeighborsTableLocalInterface"
        )
        if_table = SnmpIfTable(snmp_handler=self.snmp_handler, logger=self.logger)
        port_dict = self.snmp_handler.get_table(
            "F5-BIGIP-SYSTEM-MIB", "sysInterfaceName"
        )
        for port in port_dict:
            if not port:
                continue
            port_name = port_dict[port].get("sysInterfaceName")
            port_if_entity = if_table.get_if_index_from_port_name(port_name, ["mgmt"])
            if not port_if_entity:
                continue
            port_object = self.port_model_class(
                shell_name=self.shell_name,
                name="Port {}".format(port_name),
                unique_id="{0}.{1}.{2}".format(self.resource_name, "port", port),
            )
            port_object.mac_address = port_if_entity.if_mac
            port_object.l2_protocol_type = port_if_entity.if_type
            port_object.ipv4_address = port_if_entity.ipv4_address
            port_object.ipv6_address = port_if_entity.ipv6_address
            port_object.port_description = port_if_entity.if_port_description
            port_object.bandwidth = port_if_entity.if_speed
            port_object.mtu = port_if_entity.if_mtu
            port_object.duplex = (
                duplex_table.get(port)
                .get("sysInterfaceMediaMaxDuplex", "Half")
                .strip("'")
                .replace("none", "Half")
                .capitalize()
            )
            port_object.auto_negotiation = port_if_entity.auto_negotiation
            if lldp_table:
                lldp_table_key = [
                    k
                    for k, v in lldp_table
                    if v["sysLldpNeighborsTableLocalInterface"] == port
                ][-1]
                if lldp_table_key:
                    port_object.adjacent = "{remote_host} through {remote_port}".format(
                        remote_host=self.snmp_handler.get_property(
                            "F5-BIGIP-SYSTEM-MIB",
                            "sysLldpNeighborsTableSysName",
                            index=lldp_table_key,
                        ),
                        remote_port=self.snmp_handler.get_property(
                            "F5-BIGIP-SYSTEM-MIB",
                            "sysLldpNeighborsTablePortDesc",
                            index=lldp_table_key,
                        ),
                    )

            self._add_element(relative_path="0/0", resource=port_object)
            self.logger.info("Added Port" + port_name)

        self.logger.info("Building Ports completed")

    def _get_ip_address(self, string, stype):
        result = ""
        if stype is None:
            stype = ""
        try:
            if "6" in stype:
                result = ipaddress.IPv6Network(string, strict=False)
            else:
                result = ipaddress.IPv4Network(string, strict=False)
        except ipaddress.AddressValueError:
            self.logger.debug("Failed to load ip address", exc_info=1)
            if "6" in stype:
                result = ipaddress.IPv6Network(string, strict=False)
            else:
                result = ipaddress.IPv4Network(string[:4], strict=False)
        finally:
            return str(result).replace("/32", "")
