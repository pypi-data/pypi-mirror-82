#
# PySNMP MIB module F5-BIGIP-SYSTEM-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/F5-BIGIP-SYSTEM-MIB
# Produced by pysmi-0.2.2 at Wed Feb 14 11:04:06 2018
# On host ? platform ? version ? by user ?
# Using Python version 2.7.9 (default, Dec 10 2014, 12:24:55) [MSC v.1500 32 bit (Intel)]
#
Integer, ObjectIdentifier, OctetString = mibBuilder.importSymbols(
    "ASN1", "Integer", "ObjectIdentifier", "OctetString"
)
(NamedValues,) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
(
    ConstraintsUnion,
    SingleValueConstraint,
    ConstraintsIntersection,
    ValueSizeConstraint,
    ValueRangeConstraint,
) = mibBuilder.importSymbols(
    "ASN1-REFINEMENT",
    "ConstraintsUnion",
    "SingleValueConstraint",
    "ConstraintsIntersection",
    "ValueSizeConstraint",
    "ValueRangeConstraint",
)
(
    bigipCompliances,
    LongDisplayString,
    bigipGroups,
    bigipTrafficMgmt,
) = mibBuilder.importSymbols(
    "F5-BIGIP-COMMON-MIB",
    "bigipCompliances",
    "LongDisplayString",
    "bigipGroups",
    "bigipTrafficMgmt",
)
InetAddress, InetAddressType = mibBuilder.importSymbols(
    "INET-ADDRESS-MIB", "InetAddress", "InetAddressType"
)
NotificationGroup, ModuleCompliance, ObjectGroup = mibBuilder.importSymbols(
    "SNMPv2-CONF", "NotificationGroup", "ModuleCompliance", "ObjectGroup"
)
(
    Integer32,
    MibScalar,
    MibTable,
    MibTableRow,
    MibTableColumn,
    NotificationType,
    MibIdentifier,
    Opaque,
    IpAddress,
    TimeTicks,
    Counter64,
    Unsigned32,
    enterprises,
    ModuleIdentity,
    Gauge32,
    iso,
    ObjectIdentity,
    Bits,
    Counter32,
) = mibBuilder.importSymbols(
    "SNMPv2-SMI",
    "Integer32",
    "MibScalar",
    "MibTable",
    "MibTableRow",
    "MibTableColumn",
    "NotificationType",
    "MibIdentifier",
    "Opaque",
    "IpAddress",
    "TimeTicks",
    "Counter64",
    "Unsigned32",
    "enterprises",
    "ModuleIdentity",
    "Gauge32",
    "iso",
    "ObjectIdentity",
    "Bits",
    "Counter32",
)
DisplayString, MacAddress, TextualConvention = mibBuilder.importSymbols(
    "SNMPv2-TC", "DisplayString", "MacAddress", "TextualConvention"
)
bigipSystem = ModuleIdentity((1, 3, 6, 1, 4, 1, 3375, 2, 1))
if mibBuilder.loadTexts:
    bigipSystem.setLastUpdated("201002172155Z")
if mibBuilder.loadTexts:
    bigipSystem.setOrganization("F5 Networks, Inc.")
sysGlobals = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1))
sysNetwork = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2))
sysPlatform = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3))
sysProduct = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 4))
sysSubMemory = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 5))
sysSystem = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 6))
sysHostInfoStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 7))
sysSystemStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 8))
sysSoftware = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 9))
sysClusters = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 10))
sysModules = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 11))
sysAdmin = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 1))
sysArpNdp = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 2))
sysDot1dBridge = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3))
sysInterfaces = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4))
sysL2 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5))
sysPacketFilters = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6))
sysRoute = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7))
sysSelfIps = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8))
sysSelfPorts = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9))
sysSpanningTree = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10))
sysTransmission = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11))
sysTrunks = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12))
sysVlans = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13))
sysGlobalAttrs = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1))
sysGlobalStats = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2))
sysGlobalAttr = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1))
sysGlobalStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1))
sysGlobalAuthStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 2))
sysGlobalConnPoolStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 3))
sysGlobalHttpStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4))
sysGlobalIcmpStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5))
sysGlobalIcmp6Stat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6))
sysGlobalIpStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7))
sysGlobalIp6Stat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8))
sysGlobalClientSslStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9))
sysGlobalServerSslStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10))
sysGlobalStreamStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 11))
sysGlobalTcpStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12))
sysGlobalUdpStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13))
sysGlobalFastHttpStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14))
sysGlobalXmlStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 15))
sysGlobalIiopStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 16))
sysGlobalRtspStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 17))
sysGlobalSctpStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18))
sysGlobalFastL4Stat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19))
sysGlobalHost = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20))
sysGlobalTmmStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21))
sysAdminIp = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 1, 1))
sysCpu = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 1))
sysChassis = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2))
sysGeneral = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 3))
sysDeviceModelOIDs = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4))
sysPlatformInfo = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 5))
sysChassisFan = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 1))
sysChassisPowerSupply = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 2))
sysChassisTemp = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 3))
sysArpStaticEntry = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 2, 1))
sysDot1dbaseStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 1))
sysDot1dbaseStatPort = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 2))
sysInterface = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1))
sysInterfaceMediaOptions = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 2))
sysInterfaceId = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 3))
sysInterfaceStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4))
sysIfxStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5))
sysInterfaceMediaSfp = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 6))
sysL2Forward = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 1))
sysL2ForwardStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 2))
sysL2ForwardAttr = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 3))
sysPacketFilter = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1))
sysPacketFilterAddress = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 2))
sysPacketFilterVlan = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 3))
sysPacketFilterMac = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 4))
sysPacketFilterStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 5))
sysRouteMgmtEntry = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1))
sysRouteStaticEntry = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2))
sysSelfIp = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1))
sysSelfPort = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 1))
sysSelfPortDefault = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 2))
sysStp = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 1))
sysStpGlobals = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 2))
sysStpInterfaceMbr = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3))
sysStpVlanMbr = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 4))
sysStpBridgeStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5))
sysStpBridgeTreeStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6))
sysStpInterfaceStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7))
sysStpInterfaceTreeStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8))
sysDot3Stat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1))
sysTrunk = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1))
sysTrunkStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2))
sysTrunkCfgMember = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 3))
sysVlan = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1))
sysVlanMember = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 2))
sysVlanGroup = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3))
sysVlanGroupMbr = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 4))
sysProxyExclusion = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 5))
sysHostMemory = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 1))
sysHostCpu = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2))
sysHostDisk = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 3))
sysMultiHost = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 4))
sysMultiHostCpu = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5))
sysSoftwareVolume = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 1))
sysSoftwareImage = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2))
sysSoftwareHotfix = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3))
sysSoftwareStatus = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 4))
sysPvaStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1))
sysTmmStat = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2))
sysCluster = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1))
sysClusterMbr = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2))
sysModuleAllocation = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 11, 1))
bigip520 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 1))
bigip540 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 2))
bigip1000 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 3))
bigip1500 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 4))
bigip2400 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 5))
bigip3400 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 6))
bigip4100 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 7))
bigip5100 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 8))
bigip5110 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 9))
bigip6400 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 10))
bigip6800 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 11))
bigip8400 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 12))
bigip8800 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 13))
em3000 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 14))
wj300 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 15))
wj400 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 16))
wj500 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 17))
wj800 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 18))
bigipPb200 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 19))
bigip1600 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 20))
bigip3600 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 21))
bigip6900 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 22))
bigip8900 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 23))
bigip3900 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 24))
bigip8950 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 25))
em4000 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 26))
bigip11050 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 27))
em500 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 28))
arx1000 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 29))
arx2000 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 30))
arx4000 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 31))
arx500 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 32))
bigip3410 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 33))
bigipPb100 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 34))
bigipPb100n = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 35))
sam4300 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 36))
firepass1200 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 37))
firepass4100 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 38))
firepass4300 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 39))
swanWJ200 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 40))
TrafficShield4100 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 41))
wa4500 = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 42))
bigipVirtualEdition = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 43))
unknown = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 4, 1000))
sysAttrArpMaxEntries = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrArpMaxEntries.setStatus("current")
sysAttrArpAddReciprocal = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 2),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrArpAddReciprocal.setStatus("current")
sysAttrArpTimeout = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrArpTimeout.setStatus("current")
sysAttrArpRetries = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrArpRetries.setStatus("current")
sysAttrBootQuiet = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 5),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrBootQuiet.setStatus("current")
sysAttrConfigsyncState = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 6), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrConfigsyncState.setStatus("current")
sysAttrConnAdaptiveReaperHiwat = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 7), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrConnAdaptiveReaperHiwat.setStatus("current")
sysAttrConnAdaptiveReaperLowat = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 8), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrConnAdaptiveReaperLowat.setStatus("current")
sysAttrConnAutoLasthop = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 9),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrConnAutoLasthop.setStatus("current")
sysAttrFailoverActiveMode = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 10),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverActiveMode.setStatus("current")
sysAttrFailoverForceActive = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 11),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverForceActive.setStatus("current")
sysAttrFailoverForceStandby = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 12),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverForceStandby.setStatus("current")
sysAttrFailoverIsRedundant = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 13),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverIsRedundant.setStatus("current")
sysAttrFailoverMemoryRestartPercent = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 14), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverMemoryRestartPercent.setStatus("deprecated")
sysAttrFailoverNetwork = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 15),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverNetwork.setStatus("current")
sysAttrFailoverStandbyLinkDownTime = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 16), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverStandbyLinkDownTime.setStatus("current")
sysAttrFailoverSslhardware = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 17),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverSslhardware.setStatus("deprecated")
sysAttrFailoverSslhardwareAction = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 18),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("failover", 0), ("reboot", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverSslhardwareAction.setStatus("deprecated")
sysAttrFailoverUnitMask = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 19), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverUnitMask.setStatus("current")
sysAttrFailoverUnitId = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 20), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrFailoverUnitId.setStatus("current")
sysAttrModeMaint = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 21),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrModeMaint.setStatus("current")
sysAttrPacketFilter = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 22),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disabled", 0), ("enabled", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrPacketFilter.setStatus("current")
sysAttrPacketFilterAllowImportantIcmp = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 23),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disabled", 0), ("enabled", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrPacketFilterAllowImportantIcmp.setStatus("current")
sysAttrPacketFilterEstablished = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 24),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disabled", 0), ("enabled", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrPacketFilterEstablished.setStatus("current")
sysAttrPacketFilterDefaultAction = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 25),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2))
    .clone(namedValues=NamedValues(("accept", 0), ("discard", 1), ("reject", 2))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrPacketFilterDefaultAction.setStatus("current")
sysAttrPacketFilterSendIcmpErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 26),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrPacketFilterSendIcmpErrors.setStatus("current")
sysAttrPvaAcceleration = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 27),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2))
    .clone(namedValues=NamedValues(("none", 0), ("partial", 1), ("full", 2))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrPvaAcceleration.setStatus("current")
sysAttrVlanFDBTimeout = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 28), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrVlanFDBTimeout.setStatus("current")
sysAttrWatchdogState = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 1, 1, 29),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("disable", 0), ("enable", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAttrWatchdogState.setStatus("current")
sysStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysStatResetStats.setStatus("current")
sysStatClientPktsIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientPktsIn.setStatus("current")
sysStatClientBytesIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientBytesIn.setStatus("current")
sysStatClientPktsOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientPktsOut.setStatus("current")
sysStatClientBytesOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientBytesOut.setStatus("current")
sysStatClientMaxConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientMaxConns.setStatus("current")
sysStatClientTotConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientTotConns.setStatus("current")
sysStatClientCurConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientCurConns.setStatus("current")
sysStatServerPktsIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerPktsIn.setStatus("current")
sysStatServerBytesIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerBytesIn.setStatus("current")
sysStatServerPktsOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerPktsOut.setStatus("current")
sysStatServerBytesOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerBytesOut.setStatus("current")
sysStatServerMaxConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerMaxConns.setStatus("current")
sysStatServerTotConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerTotConns.setStatus("current")
sysStatServerCurConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerCurConns.setStatus("current")
sysStatPvaClientPktsIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientPktsIn.setStatus("current")
sysStatPvaClientBytesIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientBytesIn.setStatus("current")
sysStatPvaClientPktsOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientPktsOut.setStatus("current")
sysStatPvaClientBytesOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 19), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientBytesOut.setStatus("current")
sysStatPvaClientMaxConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 20), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientMaxConns.setStatus("current")
sysStatPvaClientTotConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 21), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientTotConns.setStatus("current")
sysStatPvaClientCurConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 22), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientCurConns.setStatus("current")
sysStatPvaServerPktsIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 23), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerPktsIn.setStatus("current")
sysStatPvaServerBytesIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 24), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerBytesIn.setStatus("current")
sysStatPvaServerPktsOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 25), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerPktsOut.setStatus("current")
sysStatPvaServerBytesOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 26), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerBytesOut.setStatus("current")
sysStatPvaServerMaxConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 27), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerMaxConns.setStatus("current")
sysStatPvaServerTotConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 28), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerTotConns.setStatus("current")
sysStatPvaServerCurConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 29), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerCurConns.setStatus("current")
sysStatTotPvaAssistConn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 30), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatTotPvaAssistConn.setStatus("current")
sysStatCurrPvaAssistConn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 31), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatCurrPvaAssistConn.setStatus("current")
sysStatMaintenanceModeDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 32), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatMaintenanceModeDeny.setStatus("current")
sysStatMaxConnVirtualPathDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 33), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatMaxConnVirtualPathDeny.setStatus("current")
sysStatVirtualServerNonSynDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 34), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatVirtualServerNonSynDeny.setStatus("current")
sysStatNoHandlerDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 35), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatNoHandlerDeny.setStatus("current")
sysStatLicenseDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 36), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatLicenseDeny.setStatus("current")
sysStatConnectionMemoryErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 37), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatConnectionMemoryErrors.setStatus("current")
sysStatCpuCount = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 38), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatCpuCount.setStatus("current")
sysStatActiveCpuCount = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 39), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatActiveCpuCount.setStatus("current")
sysStatMultiProcessorMode = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 40),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("modeup", 0), ("modesmp", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatMultiProcessorMode.setStatus("deprecated")
sysStatTmTotalCycles = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 41), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatTmTotalCycles.setStatus("current")
sysStatTmIdleCycles = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 42), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatTmIdleCycles.setStatus("current")
sysStatTmSleepCycles = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 43), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatTmSleepCycles.setStatus("current")
sysStatMemoryTotal = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 44), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatMemoryTotal.setStatus("current")
sysStatMemoryUsed = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 45), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatMemoryUsed.setStatus("current")
sysStatDroppedPackets = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 46), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatDroppedPackets.setStatus("current")
sysStatIncomingPacketErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 47), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatIncomingPacketErrors.setStatus("current")
sysStatOutgoingPacketErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 48), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatOutgoingPacketErrors.setStatus("current")
sysStatAuthTotSessions = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 49), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatAuthTotSessions.setStatus("current")
sysStatAuthCurSessions = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 50), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatAuthCurSessions.setStatus("current")
sysStatAuthMaxSessions = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 51), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatAuthMaxSessions.setStatus("current")
sysStatAuthSuccessResults = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 52), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatAuthSuccessResults.setStatus("current")
sysStatAuthFailureResults = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 53), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatAuthFailureResults.setStatus("current")
sysStatAuthWantcredentialResults = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 54), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatAuthWantcredentialResults.setStatus("current")
sysStatAuthErrorResults = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 55), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatAuthErrorResults.setStatus("current")
sysStatHttpRequests = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 56), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatHttpRequests.setStatus("current")
sysStatHardSyncookieGen = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 57), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatHardSyncookieGen.setStatus("current")
sysStatHardSyncookieDet = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 58), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatHardSyncookieDet.setStatus("current")
sysStatClientPktsIn5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 59), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientPktsIn5s.setStatus("current")
sysStatClientBytesIn5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 60), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientBytesIn5s.setStatus("current")
sysStatClientPktsOut5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 61), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientPktsOut5s.setStatus("current")
sysStatClientBytesOut5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 62), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientBytesOut5s.setStatus("current")
sysStatClientMaxConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 63), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientMaxConns5s.setStatus("current")
sysStatClientTotConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 64), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientTotConns5s.setStatus("current")
sysStatClientCurConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 65), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientCurConns5s.setStatus("current")
sysStatServerPktsIn5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 66), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerPktsIn5s.setStatus("current")
sysStatServerBytesIn5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 67), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerBytesIn5s.setStatus("current")
sysStatServerPktsOut5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 68), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerPktsOut5s.setStatus("current")
sysStatServerBytesOut5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 69), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerBytesOut5s.setStatus("current")
sysStatServerMaxConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 70), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerMaxConns5s.setStatus("current")
sysStatServerTotConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 71), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerTotConns5s.setStatus("current")
sysStatServerCurConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 72), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerCurConns5s.setStatus("current")
sysStatClientPktsIn1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 73), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientPktsIn1m.setStatus("current")
sysStatClientBytesIn1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 74), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientBytesIn1m.setStatus("current")
sysStatClientPktsOut1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 75), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientPktsOut1m.setStatus("current")
sysStatClientBytesOut1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 76), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientBytesOut1m.setStatus("current")
sysStatClientMaxConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 77), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientMaxConns1m.setStatus("current")
sysStatClientTotConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 78), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientTotConns1m.setStatus("current")
sysStatClientCurConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 79), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientCurConns1m.setStatus("current")
sysStatServerPktsIn1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 80), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerPktsIn1m.setStatus("current")
sysStatServerBytesIn1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 81), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerBytesIn1m.setStatus("current")
sysStatServerPktsOut1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 82), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerPktsOut1m.setStatus("current")
sysStatServerBytesOut1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 83), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerBytesOut1m.setStatus("current")
sysStatServerMaxConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 84), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerMaxConns1m.setStatus("current")
sysStatServerTotConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 85), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerTotConns1m.setStatus("current")
sysStatServerCurConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 86), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerCurConns1m.setStatus("current")
sysStatClientPktsIn5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 87), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientPktsIn5m.setStatus("current")
sysStatClientBytesIn5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 88), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientBytesIn5m.setStatus("current")
sysStatClientPktsOut5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 89), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientPktsOut5m.setStatus("current")
sysStatClientBytesOut5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 90), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientBytesOut5m.setStatus("current")
sysStatClientMaxConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 91), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientMaxConns5m.setStatus("current")
sysStatClientTotConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 92), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientTotConns5m.setStatus("current")
sysStatClientCurConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 93), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatClientCurConns5m.setStatus("current")
sysStatServerPktsIn5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 94), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerPktsIn5m.setStatus("current")
sysStatServerBytesIn5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 95), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerBytesIn5m.setStatus("current")
sysStatServerPktsOut5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 96), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerPktsOut5m.setStatus("current")
sysStatServerBytesOut5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 97), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerBytesOut5m.setStatus("current")
sysStatServerMaxConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 98), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerMaxConns5m.setStatus("current")
sysStatServerTotConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 99), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerTotConns5m.setStatus("current")
sysStatServerCurConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 100), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatServerCurConns5m.setStatus("current")
sysStatPvaClientPktsIn5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 101), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientPktsIn5s.setStatus("current")
sysStatPvaClientBytesIn5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 102), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientBytesIn5s.setStatus("current")
sysStatPvaClientPktsOut5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 103), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientPktsOut5s.setStatus("current")
sysStatPvaClientBytesOut5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 104), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientBytesOut5s.setStatus("current")
sysStatPvaClientMaxConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 105), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientMaxConns5s.setStatus("current")
sysStatPvaClientTotConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 106), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientTotConns5s.setStatus("current")
sysStatPvaClientCurConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 107), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientCurConns5s.setStatus("current")
sysStatPvaServerPktsIn5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 108), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerPktsIn5s.setStatus("current")
sysStatPvaServerBytesIn5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 109), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerBytesIn5s.setStatus("current")
sysStatPvaServerPktsOut5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 110), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerPktsOut5s.setStatus("current")
sysStatPvaServerBytesOut5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 111), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerBytesOut5s.setStatus("current")
sysStatPvaServerMaxConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 112), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerMaxConns5s.setStatus("current")
sysStatPvaServerTotConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 113), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerTotConns5s.setStatus("current")
sysStatPvaServerCurConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 114), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerCurConns5s.setStatus("current")
sysStatPvaClientPktsIn1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 115), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientPktsIn1m.setStatus("current")
sysStatPvaClientBytesIn1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 116), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientBytesIn1m.setStatus("current")
sysStatPvaClientPktsOut1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 117), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientPktsOut1m.setStatus("current")
sysStatPvaClientBytesOut1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 118), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientBytesOut1m.setStatus("current")
sysStatPvaClientMaxConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 119), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientMaxConns1m.setStatus("current")
sysStatPvaClientTotConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 120), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientTotConns1m.setStatus("current")
sysStatPvaClientCurConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 121), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientCurConns1m.setStatus("current")
sysStatPvaServerPktsIn1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 122), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerPktsIn1m.setStatus("current")
sysStatPvaServerBytesIn1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 123), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerBytesIn1m.setStatus("current")
sysStatPvaServerPktsOut1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 124), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerPktsOut1m.setStatus("current")
sysStatPvaServerBytesOut1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 125), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerBytesOut1m.setStatus("current")
sysStatPvaServerMaxConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 126), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerMaxConns1m.setStatus("current")
sysStatPvaServerTotConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 127), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerTotConns1m.setStatus("current")
sysStatPvaServerCurConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 128), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerCurConns1m.setStatus("current")
sysStatPvaClientPktsIn5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 129), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientPktsIn5m.setStatus("current")
sysStatPvaClientBytesIn5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 130), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientBytesIn5m.setStatus("current")
sysStatPvaClientPktsOut5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 131), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientPktsOut5m.setStatus("current")
sysStatPvaClientBytesOut5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 132), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientBytesOut5m.setStatus("current")
sysStatPvaClientMaxConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 133), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientMaxConns5m.setStatus("current")
sysStatPvaClientTotConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 134), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientTotConns5m.setStatus("current")
sysStatPvaClientCurConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 135), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaClientCurConns5m.setStatus("current")
sysStatPvaServerPktsIn5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 136), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerPktsIn5m.setStatus("current")
sysStatPvaServerBytesIn5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 137), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerBytesIn5m.setStatus("current")
sysStatPvaServerPktsOut5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 138), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerPktsOut5m.setStatus("current")
sysStatPvaServerBytesOut5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 139), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerBytesOut5m.setStatus("current")
sysStatPvaServerMaxConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 140), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerMaxConns5m.setStatus("current")
sysStatPvaServerTotConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 141), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerTotConns5m.setStatus("current")
sysStatPvaServerCurConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 1, 142), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStatPvaServerCurConns5m.setStatus("current")
sysAuthStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 2, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysAuthStatResetStats.setStatus("current")
sysAuthStatTotSessions = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 2, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAuthStatTotSessions.setStatus("current")
sysAuthStatCurSessions = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 2, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAuthStatCurSessions.setStatus("current")
sysAuthStatMaxSessions = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 2, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAuthStatMaxSessions.setStatus("current")
sysAuthStatSuccessResults = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 2, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAuthStatSuccessResults.setStatus("current")
sysAuthStatFailureResults = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 2, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAuthStatFailureResults.setStatus("current")
sysAuthStatWantcredentialResults = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 2, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAuthStatWantcredentialResults.setStatus("current")
sysAuthStatErrorResults = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 2, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAuthStatErrorResults.setStatus("current")
sysConnPoolStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 3, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysConnPoolStatResetStats.setStatus("current")
sysConnPoolStatCurSize = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 3, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysConnPoolStatCurSize.setStatus("current")
sysConnPoolStatMaxSize = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 3, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysConnPoolStatMaxSize.setStatus("current")
sysConnPoolStatReuses = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 3, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysConnPoolStatReuses.setStatus("current")
sysConnPoolStatConnects = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 3, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysConnPoolStatConnects.setStatus("current")
sysHttpStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysHttpStatResetStats.setStatus("current")
sysHttpStatCookiePersistInserts = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatCookiePersistInserts.setStatus("current")
sysHttpStatResp2xxCnt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatResp2xxCnt.setStatus("current")
sysHttpStatResp3xxCnt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatResp3xxCnt.setStatus("current")
sysHttpStatResp4xxCnt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatResp4xxCnt.setStatus("current")
sysHttpStatResp5xxCnt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatResp5xxCnt.setStatus("current")
sysHttpStatNumberReqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatNumberReqs.setStatus("current")
sysHttpStatGetReqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatGetReqs.setStatus("current")
sysHttpStatPostReqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatPostReqs.setStatus("current")
sysHttpStatV9Reqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatV9Reqs.setStatus("current")
sysHttpStatV10Reqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatV10Reqs.setStatus("current")
sysHttpStatV11Reqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatV11Reqs.setStatus("current")
sysHttpStatV9Resp = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatV9Resp.setStatus("current")
sysHttpStatV10Resp = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatV10Resp.setStatus("current")
sysHttpStatV11Resp = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatV11Resp.setStatus("current")
sysHttpStatMaxKeepaliveReq = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatMaxKeepaliveReq.setStatus("current")
sysHttpStatRespBucket1k = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRespBucket1k.setStatus("current")
sysHttpStatRespBucket4k = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRespBucket4k.setStatus("current")
sysHttpStatRespBucket16k = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 19), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRespBucket16k.setStatus("current")
sysHttpStatRespBucket32k = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 20), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRespBucket32k.setStatus("current")
sysHttpStatPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 21), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatPrecompressBytes.setStatus("current")
sysHttpStatPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 22), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatPostcompressBytes.setStatus("current")
sysHttpStatNullCompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 23), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatNullCompressBytes.setStatus("current")
sysHttpStatHtmlPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 24), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatHtmlPrecompressBytes.setStatus("current")
sysHttpStatHtmlPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 25), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatHtmlPostcompressBytes.setStatus("current")
sysHttpStatCssPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 26), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatCssPrecompressBytes.setStatus("current")
sysHttpStatCssPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 27), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatCssPostcompressBytes.setStatus("current")
sysHttpStatJsPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 28), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatJsPrecompressBytes.setStatus("current")
sysHttpStatJsPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 29), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatJsPostcompressBytes.setStatus("current")
sysHttpStatXmlPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 30), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatXmlPrecompressBytes.setStatus("current")
sysHttpStatXmlPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 31), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatXmlPostcompressBytes.setStatus("current")
sysHttpStatSgmlPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 32), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatSgmlPrecompressBytes.setStatus("current")
sysHttpStatSgmlPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 33), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatSgmlPostcompressBytes.setStatus("current")
sysHttpStatPlainPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 34), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatPlainPrecompressBytes.setStatus("current")
sysHttpStatPlainPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 35), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatPlainPostcompressBytes.setStatus("current")
sysHttpStatOctetPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 36), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatOctetPrecompressBytes.setStatus("current")
sysHttpStatOctetPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 37), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatOctetPostcompressBytes.setStatus("current")
sysHttpStatImagePrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 38), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatImagePrecompressBytes.setStatus("current")
sysHttpStatImagePostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 39), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatImagePostcompressBytes.setStatus("current")
sysHttpStatVideoPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 40), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatVideoPrecompressBytes.setStatus("current")
sysHttpStatVideoPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 41), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatVideoPostcompressBytes.setStatus("current")
sysHttpStatAudioPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 42), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatAudioPrecompressBytes.setStatus("current")
sysHttpStatAudioPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 43), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatAudioPostcompressBytes.setStatus("current")
sysHttpStatOtherPrecompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 44), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatOtherPrecompressBytes.setStatus("current")
sysHttpStatOtherPostcompressBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 45), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatOtherPostcompressBytes.setStatus("current")
sysHttpStatRamcacheHits = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 46), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRamcacheHits.setStatus("current")
sysHttpStatRamcacheMisses = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 47), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRamcacheMisses.setStatus("current")
sysHttpStatRamcacheMissesAll = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 48), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRamcacheMissesAll.setStatus("current")
sysHttpStatRamcacheHitBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 49), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRamcacheHitBytes.setStatus("current")
sysHttpStatRamcacheMissBytes = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 50), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRamcacheMissBytes.setStatus("current")
sysHttpStatRamcacheMissBytesAll = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 51), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRamcacheMissBytesAll.setStatus("current")
sysHttpStatRamcacheSize = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 52), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRamcacheSize.setStatus("current")
sysHttpStatRamcacheCount = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 53), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRamcacheCount.setStatus("current")
sysHttpStatRamcacheEvictions = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 54), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRamcacheEvictions.setStatus("current")
sysHttpStatRespBucket64k = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 4, 55), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHttpStatRespBucket64k.setStatus("deprecated")
sysIcmpStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysIcmpStatResetStats.setStatus("current")
sysIcmpStatTx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatTx.setStatus("current")
sysIcmpStatRx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatRx.setStatus("current")
sysIcmpStatForward = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatForward.setStatus("current")
sysIcmpStatDrop = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatDrop.setStatus("current")
sysIcmpStatErrCksum = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatErrCksum.setStatus("current")
sysIcmpStatErrLen = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatErrLen.setStatus("current")
sysIcmpStatErrMem = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatErrMem.setStatus("current")
sysIcmpStatErrRtx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatErrRtx.setStatus("current")
sysIcmpStatErrProto = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatErrProto.setStatus("current")
sysIcmpStatErrOpt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatErrOpt.setStatus("current")
sysIcmpStatErr = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 5, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmpStatErr.setStatus("current")
sysIcmp6StatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysIcmp6StatResetStats.setStatus("current")
sysIcmp6StatTx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatTx.setStatus("current")
sysIcmp6StatRx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatRx.setStatus("current")
sysIcmp6StatForward = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatForward.setStatus("current")
sysIcmp6StatDrop = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatDrop.setStatus("current")
sysIcmp6StatErrCksum = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatErrCksum.setStatus("current")
sysIcmp6StatErrLen = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatErrLen.setStatus("current")
sysIcmp6StatErrMem = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatErrMem.setStatus("current")
sysIcmp6StatErrRtx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatErrRtx.setStatus("current")
sysIcmp6StatErrProto = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatErrProto.setStatus("current")
sysIcmp6StatErrOpt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatErrOpt.setStatus("current")
sysIcmp6StatErr = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 6, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIcmp6StatErr.setStatus("current")
sysIpStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysIpStatResetStats.setStatus("current")
sysIpStatTx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatTx.setStatus("current")
sysIpStatRx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatRx.setStatus("current")
sysIpStatDropped = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatDropped.setStatus("current")
sysIpStatRxFrag = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatRxFrag.setStatus("current")
sysIpStatRxFragDropped = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatRxFragDropped.setStatus("current")
sysIpStatTxFrag = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatTxFrag.setStatus("current")
sysIpStatTxFragDropped = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatTxFragDropped.setStatus("current")
sysIpStatReassembled = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatReassembled.setStatus("current")
sysIpStatErrCksum = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatErrCksum.setStatus("current")
sysIpStatErrLen = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatErrLen.setStatus("current")
sysIpStatErrMem = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatErrMem.setStatus("current")
sysIpStatErrRtx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatErrRtx.setStatus("current")
sysIpStatErrProto = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatErrProto.setStatus("current")
sysIpStatErrOpt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatErrOpt.setStatus("current")
sysIpStatErrReassembledTooLong = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 7, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIpStatErrReassembledTooLong.setStatus("current")
sysIp6StatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysIp6StatResetStats.setStatus("current")
sysIp6StatTx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatTx.setStatus("current")
sysIp6StatRx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatRx.setStatus("current")
sysIp6StatDropped = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatDropped.setStatus("current")
sysIp6StatRxFrag = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatRxFrag.setStatus("current")
sysIp6StatRxFragDropped = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatRxFragDropped.setStatus("current")
sysIp6StatTxFrag = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatTxFrag.setStatus("current")
sysIp6StatTxFragDropped = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatTxFragDropped.setStatus("current")
sysIp6StatReassembled = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatReassembled.setStatus("current")
sysIp6StatErrCksum = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatErrCksum.setStatus("current")
sysIp6StatErrLen = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatErrLen.setStatus("current")
sysIp6StatErrMem = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatErrMem.setStatus("current")
sysIp6StatErrRtx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatErrRtx.setStatus("current")
sysIp6StatErrProto = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatErrProto.setStatus("current")
sysIp6StatErrOpt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatErrOpt.setStatus("current")
sysIp6StatErrReassembledTooLong = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 8, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIp6StatErrReassembledTooLong.setStatus("current")
sysClientsslStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysClientsslStatResetStats.setStatus("current")
sysClientsslStatCurConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatCurConns.setStatus("current")
sysClientsslStatMaxConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatMaxConns.setStatus("current")
sysClientsslStatCurNativeConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatCurNativeConns.setStatus("current")
sysClientsslStatMaxNativeConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatMaxNativeConns.setStatus("current")
sysClientsslStatTotNativeConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatTotNativeConns.setStatus("current")
sysClientsslStatCurCompatConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatCurCompatConns.setStatus("current")
sysClientsslStatMaxCompatConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatMaxCompatConns.setStatus("current")
sysClientsslStatTotCompatConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatTotCompatConns.setStatus("current")
sysClientsslStatEncryptedBytesIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatEncryptedBytesIn.setStatus("current")
sysClientsslStatEncryptedBytesOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatEncryptedBytesOut.setStatus("current")
sysClientsslStatDecryptedBytesIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatDecryptedBytesIn.setStatus("current")
sysClientsslStatDecryptedBytesOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatDecryptedBytesOut.setStatus("current")
sysClientsslStatRecordsIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatRecordsIn.setStatus("current")
sysClientsslStatRecordsOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatRecordsOut.setStatus("current")
sysClientsslStatFullyHwAcceleratedConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatFullyHwAcceleratedConns.setStatus("current")
sysClientsslStatPartiallyHwAcceleratedConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatPartiallyHwAcceleratedConns.setStatus("current")
sysClientsslStatNonHwAcceleratedConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatNonHwAcceleratedConns.setStatus("current")
sysClientsslStatPrematureDisconnects = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 19), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatPrematureDisconnects.setStatus("current")
sysClientsslStatMidstreamRenegotiations = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 20), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatMidstreamRenegotiations.setStatus("current")
sysClientsslStatSessCacheCurEntries = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 21), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatSessCacheCurEntries.setStatus("current")
sysClientsslStatSessCacheHits = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 22), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatSessCacheHits.setStatus("current")
sysClientsslStatSessCacheLookups = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 23), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatSessCacheLookups.setStatus("current")
sysClientsslStatSessCacheOverflows = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 24), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatSessCacheOverflows.setStatus("current")
sysClientsslStatSessCacheInvalidations = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 25), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatSessCacheInvalidations.setStatus("current")
sysClientsslStatPeercertValid = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 26), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatPeercertValid.setStatus("current")
sysClientsslStatPeercertInvalid = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 27), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatPeercertInvalid.setStatus("current")
sysClientsslStatPeercertNone = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 28), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatPeercertNone.setStatus("current")
sysClientsslStatHandshakeFailures = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 29), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatHandshakeFailures.setStatus("current")
sysClientsslStatBadRecords = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 30), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatBadRecords.setStatus("current")
sysClientsslStatFatalAlerts = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 31), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatFatalAlerts.setStatus("current")
sysClientsslStatSslv2 = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 32), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatSslv2.setStatus("current")
sysClientsslStatSslv3 = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 33), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatSslv3.setStatus("current")
sysClientsslStatTlsv1 = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 34), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatTlsv1.setStatus("current")
sysClientsslStatAdhKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 35), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatAdhKeyxchg.setStatus("current")
sysClientsslStatDhDssKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 36), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatDhDssKeyxchg.setStatus("deprecated")
sysClientsslStatDhRsaKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 37), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatDhRsaKeyxchg.setStatus("current")
sysClientsslStatDssKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 38), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatDssKeyxchg.setStatus("deprecated")
sysClientsslStatEdhDssKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 39), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatEdhDssKeyxchg.setStatus("deprecated")
sysClientsslStatRsaKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 40), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatRsaKeyxchg.setStatus("current")
sysClientsslStatNullBulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 41), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatNullBulk.setStatus("current")
sysClientsslStatAesBulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 42), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatAesBulk.setStatus("current")
sysClientsslStatDesBulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 43), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatDesBulk.setStatus("current")
sysClientsslStatIdeaBulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 44), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatIdeaBulk.setStatus("current")
sysClientsslStatRc2Bulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 45), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatRc2Bulk.setStatus("current")
sysClientsslStatRc4Bulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 46), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatRc4Bulk.setStatus("current")
sysClientsslStatNullDigest = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 47), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatNullDigest.setStatus("current")
sysClientsslStatMd5Digest = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 48), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatMd5Digest.setStatus("current")
sysClientsslStatShaDigest = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 49), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatShaDigest.setStatus("current")
sysClientsslStatNotssl = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 50), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatNotssl.setStatus("current")
sysClientsslStatEdhRsaKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 51), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatEdhRsaKeyxchg.setStatus("current")
sysClientsslStatTotConns5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 52), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatTotConns5s.setStatus("current")
sysClientsslStatTotConns1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 53), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatTotConns1m.setStatus("current")
sysClientsslStatTotConns5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 9, 54), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClientsslStatTotConns5m.setStatus("current")
sysServersslStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysServersslStatResetStats.setStatus("current")
sysServersslStatCurConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatCurConns.setStatus("current")
sysServersslStatMaxConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatMaxConns.setStatus("current")
sysServersslStatCurNativeConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatCurNativeConns.setStatus("current")
sysServersslStatMaxNativeConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatMaxNativeConns.setStatus("current")
sysServersslStatTotNativeConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatTotNativeConns.setStatus("current")
sysServersslStatCurCompatConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatCurCompatConns.setStatus("current")
sysServersslStatMaxCompatConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatMaxCompatConns.setStatus("current")
sysServersslStatTotCompatConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatTotCompatConns.setStatus("current")
sysServersslStatEncryptedBytesIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatEncryptedBytesIn.setStatus("current")
sysServersslStatEncryptedBytesOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatEncryptedBytesOut.setStatus("current")
sysServersslStatDecryptedBytesIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatDecryptedBytesIn.setStatus("current")
sysServersslStatDecryptedBytesOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatDecryptedBytesOut.setStatus("current")
sysServersslStatRecordsIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatRecordsIn.setStatus("current")
sysServersslStatRecordsOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatRecordsOut.setStatus("current")
sysServersslStatFullyHwAcceleratedConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatFullyHwAcceleratedConns.setStatus("current")
sysServersslStatPartiallyHwAcceleratedConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatPartiallyHwAcceleratedConns.setStatus("current")
sysServersslStatNonHwAcceleratedConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatNonHwAcceleratedConns.setStatus("current")
sysServersslStatPrematureDisconnects = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 19), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatPrematureDisconnects.setStatus("current")
sysServersslStatMidstreamRenegotiations = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 20), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatMidstreamRenegotiations.setStatus("current")
sysServersslStatSessCacheCurEntries = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 21), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatSessCacheCurEntries.setStatus("current")
sysServersslStatSessCacheHits = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 22), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatSessCacheHits.setStatus("current")
sysServersslStatSessCacheLookups = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 23), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatSessCacheLookups.setStatus("current")
sysServersslStatSessCacheOverflows = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 24), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatSessCacheOverflows.setStatus("current")
sysServersslStatSessCacheInvalidations = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 25), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatSessCacheInvalidations.setStatus("current")
sysServersslStatPeercertValid = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 26), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatPeercertValid.setStatus("current")
sysServersslStatPeercertInvalid = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 27), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatPeercertInvalid.setStatus("current")
sysServersslStatPeercertNone = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 28), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatPeercertNone.setStatus("current")
sysServersslStatHandshakeFailures = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 29), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatHandshakeFailures.setStatus("current")
sysServersslStatBadRecords = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 30), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatBadRecords.setStatus("current")
sysServersslStatFatalAlerts = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 31), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatFatalAlerts.setStatus("current")
sysServersslStatSslv2 = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 32), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatSslv2.setStatus("current")
sysServersslStatSslv3 = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 33), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatSslv3.setStatus("current")
sysServersslStatTlsv1 = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 34), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatTlsv1.setStatus("current")
sysServersslStatAdhKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 35), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatAdhKeyxchg.setStatus("current")
sysServersslStatDhDssKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 36), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatDhDssKeyxchg.setStatus("deprecated")
sysServersslStatDhRsaKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 37), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatDhRsaKeyxchg.setStatus("current")
sysServersslStatDssKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 38), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatDssKeyxchg.setStatus("deprecated")
sysServersslStatEdhDssKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 39), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatEdhDssKeyxchg.setStatus("deprecated")
sysServersslStatRsaKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 40), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatRsaKeyxchg.setStatus("current")
sysServersslStatNullBulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 41), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatNullBulk.setStatus("current")
sysServersslStatAesBulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 42), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatAesBulk.setStatus("current")
sysServersslStatDesBulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 43), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatDesBulk.setStatus("current")
sysServersslStatIdeaBulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 44), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatIdeaBulk.setStatus("current")
sysServersslStatRc2Bulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 45), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatRc2Bulk.setStatus("current")
sysServersslStatRc4Bulk = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 46), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatRc4Bulk.setStatus("current")
sysServersslStatNullDigest = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 47), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatNullDigest.setStatus("current")
sysServersslStatMd5Digest = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 48), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatMd5Digest.setStatus("current")
sysServersslStatShaDigest = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 49), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatShaDigest.setStatus("current")
sysServersslStatNotssl = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 50), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatNotssl.setStatus("current")
sysServersslStatEdhRsaKeyxchg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 10, 51), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysServersslStatEdhRsaKeyxchg.setStatus("current")
sysStreamStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 11, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysStreamStatResetStats.setStatus("current")
sysStreamStatReplaces = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 11, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStreamStatReplaces.setStatus("current")
sysTcpStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysTcpStatResetStats.setStatus("current")
sysTcpStatOpen = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatOpen.setStatus("current")
sysTcpStatCloseWait = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatCloseWait.setStatus("current")
sysTcpStatFinWait = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatFinWait.setStatus("current")
sysTcpStatTimeWait = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatTimeWait.setStatus("current")
sysTcpStatAccepts = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatAccepts.setStatus("current")
sysTcpStatAcceptfails = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatAcceptfails.setStatus("current")
sysTcpStatConnects = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatConnects.setStatus("current")
sysTcpStatConnfails = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatConnfails.setStatus("current")
sysTcpStatExpires = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatExpires.setStatus("current")
sysTcpStatAbandons = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatAbandons.setStatus("current")
sysTcpStatRxrst = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatRxrst.setStatus("current")
sysTcpStatRxbadsum = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatRxbadsum.setStatus("current")
sysTcpStatRxbadseg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatRxbadseg.setStatus("current")
sysTcpStatRxooseg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatRxooseg.setStatus("current")
sysTcpStatRxcookie = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatRxcookie.setStatus("current")
sysTcpStatRxbadcookie = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatRxbadcookie.setStatus("current")
sysTcpStatSyncacheover = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatSyncacheover.setStatus("current")
sysTcpStatTxrexmits = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 12, 19), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTcpStatTxrexmits.setStatus("current")
sysUdpStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysUdpStatResetStats.setStatus("current")
sysUdpStatOpen = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatOpen.setStatus("current")
sysUdpStatAccepts = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatAccepts.setStatus("current")
sysUdpStatAcceptfails = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatAcceptfails.setStatus("current")
sysUdpStatConnects = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatConnects.setStatus("current")
sysUdpStatConnfails = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatConnfails.setStatus("current")
sysUdpStatExpires = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatExpires.setStatus("current")
sysUdpStatRxdgram = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatRxdgram.setStatus("current")
sysUdpStatRxbaddgram = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatRxbaddgram.setStatus("current")
sysUdpStatRxunreach = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatRxunreach.setStatus("current")
sysUdpStatRxbadsum = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatRxbadsum.setStatus("current")
sysUdpStatRxnosum = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatRxnosum.setStatus("current")
sysUdpStatTxdgram = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 13, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysUdpStatTxdgram.setStatus("current")
sysAdminIpNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 1, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAdminIpNumber.setStatus("current")
sysAdminIpTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 1, 1, 2),
)
if mibBuilder.loadTexts:
    sysAdminIpTable.setStatus("current")
sysAdminIpEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 1, 1, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysAdminIpAddrType"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysAdminIpAddr"),
)
if mibBuilder.loadTexts:
    sysAdminIpEntry.setStatus("current")
sysAdminIpAddrType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 1, 1, 2, 1, 1), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAdminIpAddrType.setStatus("current")
sysAdminIpAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 1, 1, 2, 1, 2), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAdminIpAddr.setStatus("current")
sysAdminIpNetmaskType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 1, 1, 2, 1, 3), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAdminIpNetmaskType.setStatus("current")
sysAdminIpNetmask = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 1, 1, 2, 1, 4), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysAdminIpNetmask.setStatus("current")
sysArpStaticEntryNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 2, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysArpStaticEntryNumber.setStatus("current")
sysArpStaticEntryTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 2, 1, 2),
)
if mibBuilder.loadTexts:
    sysArpStaticEntryTable.setStatus("current")
sysArpStaticEntryEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 2, 1, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysArpStaticEntryIpAddrType"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysArpStaticEntryIpAddr"),
)
if mibBuilder.loadTexts:
    sysArpStaticEntryEntry.setStatus("current")
sysArpStaticEntryIpAddrType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 2, 1, 2, 1, 1), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysArpStaticEntryIpAddrType.setStatus("current")
sysArpStaticEntryIpAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 2, 1, 2, 1, 2), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysArpStaticEntryIpAddr.setStatus("current")
sysArpStaticEntryMacAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 2, 1, 2, 1, 3), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysArpStaticEntryMacAddr.setStatus("current")
sysDot1dbaseStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 1, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysDot1dbaseStatResetStats.setStatus("current")
sysDot1dbaseStatMacAddr = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 1, 2), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot1dbaseStatMacAddr.setStatus("current")
sysDot1dbaseStatNumPorts = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 1, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot1dbaseStatNumPorts.setStatus("current")
sysDot1dbaseStatType = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 1, 4),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3))
    .clone(
        namedValues=NamedValues(
            ("uninitialized", 0),
            ("unknown", 1),
            ("transparentonly", 2),
            ("sourcerouteonly", 3),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot1dbaseStatType.setStatus("current")
sysDot1dbaseStatPortNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot1dbaseStatPortNumber.setStatus("current")
sysDot1dbaseStatPortTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 2, 2),
)
if mibBuilder.loadTexts:
    sysDot1dbaseStatPortTable.setStatus("current")
sysDot1dbaseStatPortEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 2, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatPortIndex"))
if mibBuilder.loadTexts:
    sysDot1dbaseStatPortEntry.setStatus("current")
sysDot1dbaseStatPortIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 2, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot1dbaseStatPortIndex.setStatus("current")
sysDot1dbaseStatPortPort = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 2, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot1dbaseStatPortPort.setStatus("current")
sysDot1dbaseStatPortName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 2, 2, 1, 3), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot1dbaseStatPortName.setStatus("current")
sysDot1dbaseStatPortDelayExceededDiscards = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 2, 2, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot1dbaseStatPortDelayExceededDiscards.setStatus("current")
sysDot1dbaseStatPortMtuExceededDiscards = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 3, 2, 2, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot1dbaseStatPortMtuExceededDiscards.setStatus("current")
sysInterfaceNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceNumber.setStatus("current")
sysInterfaceTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2),
)
if mibBuilder.loadTexts:
    sysInterfaceTable.setStatus("current")
sysInterfaceEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysInterfaceName"))
if mibBuilder.loadTexts:
    sysInterfaceEntry.setStatus("current")
sysInterfaceName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceName.setStatus("current")
sysInterfaceMediaMaxSpeed = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceMediaMaxSpeed.setStatus("current")
sysInterfaceMediaMaxDuplex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 3),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2))
    .clone(namedValues=NamedValues(("none", 0), ("half", 1), ("full", 2))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceMediaMaxDuplex.setStatus("current")
sysInterfaceMediaActiveSpeed = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceMediaActiveSpeed.setStatus("current")
sysInterfaceMediaActiveDuplex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 5),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2))
    .clone(namedValues=NamedValues(("none", 0), ("half", 1), ("full", 2))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceMediaActiveDuplex.setStatus("current")
sysInterfaceMacAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 6), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceMacAddr.setStatus("current")
sysInterfaceMtu = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 7), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceMtu.setStatus("current")
sysInterfaceEnabled = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 8),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceEnabled.setStatus("current")
sysInterfaceLearnMode = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 9),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2))
    .clone(
        namedValues=NamedValues(
            ("learnforward", 0), ("nolearnforward", 1), ("nolearndrop", 2)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceLearnMode.setStatus("current")
sysInterfaceFlowCtrlReq = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 10),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3))
    .clone(namedValues=NamedValues(("none", 0), ("txrx", 1), ("tx", 2), ("rx", 3))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceFlowCtrlReq.setStatus("current")
sysInterfaceStpLink = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 11),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2))
    .clone(namedValues=NamedValues(("linkp2p", 0), ("linkshared", 1), ("linkauto", 2))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStpLink.setStatus("current")
sysInterfaceStpEdge = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 12),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStpEdge.setStatus("current")
sysInterfaceStpEdgeActive = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 13),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStpEdgeActive.setStatus("current")
sysInterfaceStpAuto = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 14),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStpAuto.setStatus("current")
sysInterfaceStpEnable = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 15),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStpEnable.setStatus("current")
sysInterfaceStpReset = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 16),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStpReset.setStatus("current")
sysInterfaceStatus = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 17),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4, 5))
    .clone(
        namedValues=NamedValues(
            ("up", 0),
            ("down", 1),
            ("disabled", 2),
            ("uninitialized", 3),
            ("loopback", 4),
            ("unpopulated", 5),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatus.setStatus("current")
sysInterfaceComboPort = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 18),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceComboPort.setStatus("current")
sysInterfacePreferSfp = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 19),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfacePreferSfp.setStatus("current")
sysInterfaceSfpMedia = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 20),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceSfpMedia.setStatus("current")
sysInterfacePhyMaster = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 1, 2, 1, 21),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3))
    .clone(
        namedValues=NamedValues(("slave", 0), ("master", 1), ("auto", 2), ("none", 3))
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfacePhyMaster.setStatus("current")
sysIntfMediaNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIntfMediaNumber.setStatus("current")
sysIntfMediaTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 2, 2),
)
if mibBuilder.loadTexts:
    sysIntfMediaTable.setStatus("current")
sysIntfMediaEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 2, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysIntfMediaName"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysIntfMediaIndex"),
)
if mibBuilder.loadTexts:
    sysIntfMediaEntry.setStatus("current")
sysIntfMediaName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 2, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIntfMediaName.setStatus("current")
sysIntfMediaIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 2, 2, 1, 2),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIntfMediaIndex.setStatus("current")
sysIntfMediaMediaOption = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 2, 2, 1, 3),
    Integer32()
    .subtype(
        subtypeSpec=SingleValueConstraint(
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
        )
    )
    .clone(
        namedValues=NamedValues(
            ("media10THdx", 1),
            ("media10TFdx", 2),
            ("media100TxHdx", 3),
            ("media100TxFdx", 4),
            ("media1000THdx", 5),
            ("media1000TFdx", 6),
            ("media1000FxHdx", 7),
            ("media1000FxFdx", 8),
            ("media10000TxHdx", 9),
            ("media10000TFdx", 10),
            ("media10000FxHdx", 11),
            ("media10000FxFdx", 12),
            ("mediaAuto", 13),
            ("mediaInternal", 14),
            ("media1000SxHdx", 15),
            ("media1000SxFdx", 16),
            ("media1000LxHdx", 17),
            ("media1000LxFdx", 18),
            ("media10000SrFdx", 19),
            ("media10000LrFdx", 20),
            ("media10000ErFdx", 21),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIntfMediaMediaOption.setStatus("current")
sysIfNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 3, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfNumber.setStatus("current")
sysIfTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 3, 2),
)
if mibBuilder.loadTexts:
    sysIfTable.setStatus("current")
sysIfEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 3, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysIfIndex"))
if mibBuilder.loadTexts:
    sysIfEntry.setStatus("current")
sysIfIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 3, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfIndex.setStatus("current")
sysIfName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 3, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfName.setStatus("current")
sysInterfaceStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysInterfaceStatResetStats.setStatus("current")
sysInterfaceStatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatNumber.setStatus("current")
sysInterfaceStatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3),
)
if mibBuilder.loadTexts:
    sysInterfaceStatTable.setStatus("current")
sysInterfaceStatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatName"))
if mibBuilder.loadTexts:
    sysInterfaceStatEntry.setStatus("current")
sysInterfaceStatName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatName.setStatus("current")
sysInterfaceStatPktsIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatPktsIn.setStatus("current")
sysInterfaceStatBytesIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatBytesIn.setStatus("current")
sysInterfaceStatPktsOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatPktsOut.setStatus("current")
sysInterfaceStatBytesOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatBytesOut.setStatus("current")
sysInterfaceStatMcastIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatMcastIn.setStatus("current")
sysInterfaceStatMcastOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatMcastOut.setStatus("current")
sysInterfaceStatErrorsIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatErrorsIn.setStatus("current")
sysInterfaceStatErrorsOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatErrorsOut.setStatus("current")
sysInterfaceStatDropsIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatDropsIn.setStatus("current")
sysInterfaceStatDropsOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatDropsOut.setStatus("current")
sysInterfaceStatCollisions = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatCollisions.setStatus("current")
sysInterfaceStatPauseActive = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 13),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3))
    .clone(namedValues=NamedValues(("none", 0), ("txrx", 1), ("tx", 2), ("rx", 3))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysInterfaceStatPauseActive.setStatus("current")
sysIfxStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysIfxStatResetStats.setStatus("current")
sysIfxStatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatNumber.setStatus("current")
sysIfxStatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3),
)
if mibBuilder.loadTexts:
    sysIfxStatTable.setStatus("current")
sysIfxStatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysIfxStatName"))
if mibBuilder.loadTexts:
    sysIfxStatEntry.setStatus("current")
sysIfxStatName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatName.setStatus("current")
sysIfxStatInMulticastPkts = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatInMulticastPkts.setStatus("current")
sysIfxStatInBroadcastPkts = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatInBroadcastPkts.setStatus("current")
sysIfxStatOutMulticastPkts = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatOutMulticastPkts.setStatus("current")
sysIfxStatOutBroadcastPkts = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatOutBroadcastPkts.setStatus("current")
sysIfxStatHcInOctets = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatHcInOctets.setStatus("current")
sysIfxStatHcInUcastPkts = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatHcInUcastPkts.setStatus("current")
sysIfxStatHcInMulticastPkts = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatHcInMulticastPkts.setStatus("current")
sysIfxStatHcInBroadcastPkts = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatHcInBroadcastPkts.setStatus("current")
sysIfxStatHcOutOctets = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatHcOutOctets.setStatus("current")
sysIfxStatHcOutUcastPkts = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatHcOutUcastPkts.setStatus("current")
sysIfxStatHcOutMulticastPkts = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatHcOutMulticastPkts.setStatus("current")
sysIfxStatHcOutBroadcastPkts = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatHcOutBroadcastPkts.setStatus("current")
sysIfxStatHighSpeed = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 14), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatHighSpeed.setStatus("current")
sysIfxStatConnectorPresent = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 15), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatConnectorPresent.setStatus("current")
sysIfxStatCounterDiscontinuityTime = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatCounterDiscontinuityTime.setStatus("current")
sysIfxStatAlias = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 5, 3, 1, 17), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIfxStatAlias.setStatus("current")
sysL2ForwardNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardNumber.setStatus("current")
sysL2ForwardTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 1, 2),
)
if mibBuilder.loadTexts:
    sysL2ForwardTable.setStatus("current")
sysL2ForwardEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 1, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysL2ForwardVlanName"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysL2ForwardMacAddr"),
)
if mibBuilder.loadTexts:
    sysL2ForwardEntry.setStatus("current")
sysL2ForwardVlanName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 1, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardVlanName.setStatus("current")
sysL2ForwardMacAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 1, 2, 1, 2), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardMacAddr.setStatus("current")
sysL2ForwardIfname = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 1, 2, 1, 3), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardIfname.setStatus("current")
sysL2ForwardIftype = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 1, 2, 1, 4),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("interface", 0), ("trunk", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardIftype.setStatus("current")
sysL2ForwardDynamic = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 1, 2, 1, 5),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardDynamic.setStatus("current")
sysPacketFilterNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterNumber.setStatus("current")
sysPacketFilterTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1, 2),
)
if mibBuilder.loadTexts:
    sysPacketFilterTable.setStatus("current")
sysPacketFilterEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysPacketFilterRname"))
if mibBuilder.loadTexts:
    sysPacketFilterEntry.setStatus("current")
sysPacketFilterRname = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterRname.setStatus("current")
sysPacketFilterOrder = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterOrder.setStatus("current")
sysPacketFilterAction = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1, 2, 1, 3),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4))
    .clone(
        namedValues=NamedValues(
            ("none", 0), ("accept", 1), ("discard", 2), ("reject", 3), ("continue", 4)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterAction.setStatus("current")
sysPacketFilterVname = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1, 2, 1, 4), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterVname.setStatus("current")
sysPacketFilterLog = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1, 2, 1, 5),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterLog.setStatus("current")
sysPacketFilterRclass = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1, 2, 1, 6), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterRclass.setStatus("current")
sysPacketFilterExpression = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 1, 2, 1, 7), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterExpression.setStatus("current")
sysPacketFilterAddrNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterAddrNumber.setStatus("current")
sysPacketFilterAddrTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 2, 2),
)
if mibBuilder.loadTexts:
    sysPacketFilterAddrTable.setStatus("current")
sysPacketFilterAddrEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 2, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysPacketFilterAddrIndex"))
if mibBuilder.loadTexts:
    sysPacketFilterAddrEntry.setStatus("current")
sysPacketFilterAddrIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 2, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterAddrIndex.setStatus("current")
sysPacketFilterAddrIpType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 2, 2, 1, 2), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterAddrIpType.setStatus("current")
sysPacketFilterAddrIp = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 2, 2, 1, 3), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterAddrIp.setStatus("current")
sysPacketFilterVlanNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 3, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterVlanNumber.setStatus("current")
sysPacketFilterVlanTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 3, 2),
)
if mibBuilder.loadTexts:
    sysPacketFilterVlanTable.setStatus("current")
sysPacketFilterVlanEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 3, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysPacketFilterVlanIndex"))
if mibBuilder.loadTexts:
    sysPacketFilterVlanEntry.setStatus("current")
sysPacketFilterVlanIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 3, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterVlanIndex.setStatus("current")
sysPacketFilterVlanName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 3, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterVlanName.setStatus("current")
sysPacketFilterMacNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 4, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterMacNumber.setStatus("current")
sysPacketFilterMacTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 4, 2),
)
if mibBuilder.loadTexts:
    sysPacketFilterMacTable.setStatus("current")
sysPacketFilterMacEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 4, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysPacketFilterMacIndex"))
if mibBuilder.loadTexts:
    sysPacketFilterMacEntry.setStatus("current")
sysPacketFilterMacIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 4, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterMacIndex.setStatus("current")
sysPacketFilterMacAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 4, 2, 1, 2), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterMacAddr.setStatus("current")
sysPacketFilterStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 5, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysPacketFilterStatResetStats.setStatus("current")
sysPacketFilterStatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 5, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterStatNumber.setStatus("current")
sysPacketFilterStatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 5, 3),
)
if mibBuilder.loadTexts:
    sysPacketFilterStatTable.setStatus("current")
sysPacketFilterStatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 5, 3, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysPacketFilterStatRname"))
if mibBuilder.loadTexts:
    sysPacketFilterStatEntry.setStatus("current")
sysPacketFilterStatRname = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 5, 3, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterStatRname.setStatus("current")
sysPacketFilterStatHits = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 6, 5, 3, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPacketFilterStatHits.setStatus("current")
sysRouteMgmtEntryNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteMgmtEntryNumber.setStatus("current")
sysRouteMgmtEntryTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 2),
)
if mibBuilder.loadTexts:
    sysRouteMgmtEntryTable.setStatus("current")
sysRouteMgmtEntryEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryDestType"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryDest"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryNetmaskType"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryNetmask"),
)
if mibBuilder.loadTexts:
    sysRouteMgmtEntryEntry.setStatus("current")
sysRouteMgmtEntryDestType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 2, 1, 1), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteMgmtEntryDestType.setStatus("current")
sysRouteMgmtEntryDest = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 2, 1, 2), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteMgmtEntryDest.setStatus("current")
sysRouteMgmtEntryNetmaskType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 2, 1, 3), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteMgmtEntryNetmaskType.setStatus("current")
sysRouteMgmtEntryNetmask = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 2, 1, 4), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteMgmtEntryNetmask.setStatus("current")
sysRouteMgmtEntryType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 2, 1, 5),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3))
    .clone(
        namedValues=NamedValues(
            ("gateway", 0), ("pool", 1), ("interface", 2), ("blackhole", 3)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteMgmtEntryType.setStatus("current")
sysRouteMgmtEntryGatewayType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 2, 1, 6), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteMgmtEntryGatewayType.setStatus("current")
sysRouteMgmtEntryGateway = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 2, 1, 7), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteMgmtEntryGateway.setStatus("current")
sysRouteMgmtEntryMtu = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 1, 2, 1, 8), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteMgmtEntryMtu.setStatus("current")
sysRouteStaticEntryNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryNumber.setStatus("current")
sysRouteStaticEntryTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2),
)
if mibBuilder.loadTexts:
    sysRouteStaticEntryTable.setStatus("current")
sysRouteStaticEntryEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryDestType"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryDest"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryNetmaskType"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryNetmask"),
)
if mibBuilder.loadTexts:
    sysRouteStaticEntryEntry.setStatus("current")
sysRouteStaticEntryDestType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1, 1), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryDestType.setStatus("current")
sysRouteStaticEntryDest = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1, 2), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryDest.setStatus("current")
sysRouteStaticEntryNetmaskType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1, 3), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryNetmaskType.setStatus("current")
sysRouteStaticEntryNetmask = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1, 4), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryNetmask.setStatus("current")
sysRouteStaticEntryType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1, 5),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3))
    .clone(
        namedValues=NamedValues(
            ("gateway", 0), ("pool", 1), ("interface", 2), ("blackhole", 3)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryType.setStatus("current")
sysRouteStaticEntryVlanName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1, 6), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryVlanName.setStatus("current")
sysRouteStaticEntryGatewayType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1, 7), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryGatewayType.setStatus("current")
sysRouteStaticEntryGateway = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1, 8), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryGateway.setStatus("current")
sysRouteStaticEntryPoolName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1, 9), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryPoolName.setStatus("current")
sysRouteStaticEntryMtu = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 7, 2, 2, 1, 10), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRouteStaticEntryMtu.setStatus("current")
sysSelfIpNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfIpNumber.setStatus("current")
sysSelfIpTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1, 2),
)
if mibBuilder.loadTexts:
    sysSelfIpTable.setStatus("current")
sysSelfIpEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSelfIpAddrType"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSelfIpAddr"),
)
if mibBuilder.loadTexts:
    sysSelfIpEntry.setStatus("current")
sysSelfIpAddrType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1, 2, 1, 1), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfIpAddrType.setStatus("current")
sysSelfIpAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1, 2, 1, 2), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfIpAddr.setStatus("current")
sysSelfIpNetmaskType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1, 2, 1, 3), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfIpNetmaskType.setStatus("current")
sysSelfIpNetmask = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1, 2, 1, 4), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfIpNetmask.setStatus("current")
sysSelfIpUnitId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1, 2, 1, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfIpUnitId.setStatus("current")
sysSelfIpIsFloating = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1, 2, 1, 6),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfIpIsFloating.setStatus("current")
sysSelfIpVlanName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 8, 1, 2, 1, 7), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfIpVlanName.setStatus("current")
sysSelfPortNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfPortNumber.setStatus("current")
sysSelfPortTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 1, 2),
)
if mibBuilder.loadTexts:
    sysSelfPortTable.setStatus("current")
sysSelfPortEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 1, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSelfPortAddrType"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSelfPortAddr"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSelfPortProtocol"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSelfPortPort"),
)
if mibBuilder.loadTexts:
    sysSelfPortEntry.setStatus("current")
sysSelfPortAddrType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 1, 2, 1, 1), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfPortAddrType.setStatus("current")
sysSelfPortAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 1, 2, 1, 2), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfPortAddr.setStatus("current")
sysSelfPortProtocol = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 1, 2, 1, 3),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfPortProtocol.setStatus("current")
sysSelfPortPort = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 1, 2, 1, 4),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfPortPort.setStatus("current")
sysStpNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpNumber.setStatus("current")
sysStpTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 1, 2),
)
if mibBuilder.loadTexts:
    sysStpTable.setStatus("current")
sysStpEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 1, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysStpInstanceId"))
if mibBuilder.loadTexts:
    sysStpEntry.setStatus("current")
sysStpInstanceId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 1, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInstanceId.setStatus("current")
sysStpPriority = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 1, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpPriority.setStatus("current")
sysStpRootAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 1, 2, 1, 3), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpRootAddr.setStatus("current")
sysStpRegionalRootAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 1, 2, 1, 4), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpRegionalRootAddr.setStatus("current")
sysStpGlobalsMode = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 2, 1),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4))
    .clone(
        namedValues=NamedValues(
            ("disable", 0), ("stp", 1), ("rstp", 2), ("mstp", 3), ("passthru", 4)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpGlobalsMode.setStatus("current")
sysStpGlobalsFwdDelay = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 2, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpGlobalsFwdDelay.setStatus("current")
sysStpGlobalsHelloTime = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 2, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpGlobalsHelloTime.setStatus("current")
sysStpGlobalsMaxAge = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 2, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpGlobalsMaxAge.setStatus("current")
sysStpGlobalsTransmitHold = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 2, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpGlobalsTransmitHold.setStatus("current")
sysStpGlobalsMaxHops = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 2, 6), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpGlobalsMaxHops.setStatus("current")
sysStpGlobalsIdentifier = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 2, 7), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpGlobalsIdentifier.setStatus("current")
sysStpGlobalsRevision = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 2, 8), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpGlobalsRevision.setStatus("current")
sysStpInterfaceMbrNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceMbrNumber.setStatus("current")
sysStpInterfaceMbrTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 2),
)
if mibBuilder.loadTexts:
    sysStpInterfaceMbrTable.setStatus("current")
sysStpInterfaceMbrEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrInstanceId"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrName"),
)
if mibBuilder.loadTexts:
    sysStpInterfaceMbrEntry.setStatus("current")
sysStpInterfaceMbrInstanceId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceMbrInstanceId.setStatus("current")
sysStpInterfaceMbrName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceMbrName.setStatus("current")
sysStpInterfaceMbrType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 2, 1, 3),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("interface", 0), ("trunk", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceMbrType.setStatus("current")
sysStpInterfaceMbrStateActive = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 2, 1, 4),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4, 5))
    .clone(
        namedValues=NamedValues(
            ("detach", 0),
            ("block", 1),
            ("listen", 2),
            ("learn", 3),
            ("forward", 4),
            ("disable", 5),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceMbrStateActive.setStatus("current")
sysStpInterfaceMbrRole = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 2, 1, 5),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4, 5))
    .clone(
        namedValues=NamedValues(
            ("disable", 0),
            ("root", 1),
            ("designate", 2),
            ("alternate", 3),
            ("backup", 4),
            ("master", 5),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceMbrRole.setStatus("current")
sysStpInterfaceMbrPriority = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 2, 1, 6), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceMbrPriority.setStatus("current")
sysStpInterfaceMbrPathCost = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 2, 1, 7), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceMbrPathCost.setStatus("current")
sysStpInterfaceMbrStateRequested = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 3, 2, 1, 8),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4, 5))
    .clone(
        namedValues=NamedValues(
            ("detach", 0),
            ("block", 1),
            ("listen", 2),
            ("learn", 3),
            ("forward", 4),
            ("disable", 5),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceMbrStateRequested.setStatus("current")
sysStpVlanMbrNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 4, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpVlanMbrNumber.setStatus("current")
sysStpVlanMbrTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 4, 2),
)
if mibBuilder.loadTexts:
    sysStpVlanMbrTable.setStatus("current")
sysStpVlanMbrEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 4, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysStpVlanMbrInstanceId"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysStpVlanMbrVlanVname"),
)
if mibBuilder.loadTexts:
    sysStpVlanMbrEntry.setStatus("current")
sysStpVlanMbrInstanceId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 4, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpVlanMbrInstanceId.setStatus("current")
sysStpVlanMbrVlanVname = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 4, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpVlanMbrVlanVname.setStatus("current")
sysStpBridgeStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysStpBridgeStatResetStats.setStatus("current")
sysStpBridgeStatMode = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 2),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4))
    .clone(
        namedValues=NamedValues(
            ("disable", 0), ("stp", 1), ("rstp", 2), ("mstp", 3), ("passthru", 4)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatMode.setStatus("current")
sysStpBridgeStatFwdDelay = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatFwdDelay.setStatus("current")
sysStpBridgeStatHelloTime = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatHelloTime.setStatus("current")
sysStpBridgeStatMaxAge = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatMaxAge.setStatus("current")
sysStpBridgeStatBridgeFwdDelay = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 6), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatBridgeFwdDelay.setStatus("current")
sysStpBridgeStatBridgeHelloTime = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 7), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatBridgeHelloTime.setStatus("current")
sysStpBridgeStatBridgeMaxAge = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 8), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatBridgeMaxAge.setStatus("current")
sysStpBridgeStatTransmitHold = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 9), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatTransmitHold.setStatus("current")
sysStpBridgeStatPathCost = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 10), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatPathCost.setStatus("current")
sysStpBridgeStatRootPrio = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 11), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatRootPrio.setStatus("current")
sysStpBridgeStatRootAddr = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 5, 12), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeStatRootAddr.setStatus("current")
sysStpBridgeTreeStatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatNumber.setStatus("current")
sysStpBridgeTreeStatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2),
)
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatTable.setStatus("current")
sysStpBridgeTreeStatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatIndex"))
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatEntry.setStatus("current")
sysStpBridgeTreeStatIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatIndex.setStatus("current")
sysStpBridgeTreeStatInstanceId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatInstanceId.setStatus("current")
sysStpBridgeTreeStatPriority = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatPriority.setStatus("current")
sysStpBridgeTreeStatLastTc = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1, 4), TimeTicks()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatLastTc.setStatus("current")
sysStpBridgeTreeStatTcCount = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatTcCount.setStatus("current")
sysStpBridgeTreeStatDesigRootPrio = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1, 6), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatDesigRootPrio.setStatus("current")
sysStpBridgeTreeStatDesigRootAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1, 7), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatDesigRootAddr.setStatus("current")
sysStpBridgeTreeStatInternalPathCost = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1, 8), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatInternalPathCost.setStatus("current")
sysStpBridgeTreeStatRootPort = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1, 9), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatRootPort.setStatus("current")
sysStpBridgeTreeStatRootPortNum = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 6, 2, 1, 10), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpBridgeTreeStatRootPortNum.setStatus("current")
sysStpInterfaceStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysStpInterfaceStatResetStats.setStatus("current")
sysStpInterfaceStatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceStatNumber.setStatus("current")
sysStpInterfaceStatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 3),
)
if mibBuilder.loadTexts:
    sysStpInterfaceStatTable.setStatus("current")
sysStpInterfaceStatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 3, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceStatName"))
if mibBuilder.loadTexts:
    sysStpInterfaceStatEntry.setStatus("current")
sysStpInterfaceStatName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 3, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceStatName.setStatus("current")
sysStpInterfaceStatPortNum = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 3, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceStatPortNum.setStatus("current")
sysStpInterfaceStatStpEnable = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 3, 1, 3),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceStatStpEnable.setStatus("current")
sysStpInterfaceStatPathCost = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 3, 1, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceStatPathCost.setStatus("current")
sysStpInterfaceStatRootCost = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 3, 1, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceStatRootCost.setStatus("current")
sysStpInterfaceStatRootPrio = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 3, 1, 6), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceStatRootPrio.setStatus("current")
sysStpInterfaceStatRootAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 7, 3, 1, 7), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceStatRootAddr.setStatus("current")
sysStpInterfaceTreeStatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatNumber.setStatus("current")
sysStpInterfaceTreeStatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2),
)
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatTable.setStatus("current")
sysStpInterfaceTreeStatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatName"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatIndex"),
)
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatEntry.setStatus("current")
sysStpInterfaceTreeStatName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatName.setStatus("current")
sysStpInterfaceTreeStatIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 2),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatIndex.setStatus("current")
sysStpInterfaceTreeStatInstanceId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatInstanceId.setStatus("current")
sysStpInterfaceTreeStatPriority = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatPriority.setStatus("current")
sysStpInterfaceTreeStatState = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 5),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4, 5))
    .clone(
        namedValues=NamedValues(
            ("detach", 0),
            ("block", 1),
            ("listen", 2),
            ("learn", 3),
            ("forward", 4),
            ("disable", 5),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatState.setStatus("current")
sysStpInterfaceTreeStatStatRole = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 6),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4, 5))
    .clone(
        namedValues=NamedValues(
            ("disable", 0),
            ("root", 1),
            ("designate", 2),
            ("alternate", 3),
            ("backup", 4),
            ("master", 5),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatStatRole.setStatus("current")
sysStpInterfaceTreeStatDesigRootPrio = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 7), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatDesigRootPrio.setStatus("current")
sysStpInterfaceTreeStatDesigRootAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 8), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatDesigRootAddr.setStatus("current")
sysStpInterfaceTreeStatDesigCost = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 9), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatDesigCost.setStatus("current")
sysStpInterfaceTreeStatDesigBridgePrio = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 10), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatDesigBridgePrio.setStatus("current")
sysStpInterfaceTreeStatDesigBridgeAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 11), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatDesigBridgeAddr.setStatus("current")
sysStpInterfaceTreeStatDesigPortNum = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 12), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatDesigPortNum.setStatus("current")
sysStpInterfaceTreeStatDesigPortPriority = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 13), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatDesigPortPriority.setStatus("current")
sysStpInterfaceTreeStatInternalPathCost = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 14), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatInternalPathCost.setStatus("current")
sysStpInterfaceTreeStatFwdTransitions = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 10, 8, 2, 1, 15), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysStpInterfaceTreeStatFwdTransitions.setStatus("current")
sysDot3StatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysDot3StatResetStats.setStatus("current")
sysDot3StatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatNumber.setStatus("current")
sysDot3StatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3),
)
if mibBuilder.loadTexts:
    sysDot3StatTable.setStatus("current")
sysDot3StatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysDot3StatName"))
if mibBuilder.loadTexts:
    sysDot3StatEntry.setStatus("current")
sysDot3StatName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatName.setStatus("current")
sysDot3StatAlignmentErrors = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatAlignmentErrors.setStatus("current")
sysDot3StatFcsErrors = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatFcsErrors.setStatus("current")
sysDot3StatSingleCollisionFrames = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatSingleCollisionFrames.setStatus("current")
sysDot3StatMultiCollisionFrames = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatMultiCollisionFrames.setStatus("current")
sysDot3StatSqetestErrors = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatSqetestErrors.setStatus("current")
sysDot3StatDeferredTx = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatDeferredTx.setStatus("current")
sysDot3StatLateCollisions = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatLateCollisions.setStatus("current")
sysDot3StatExcessiveCollisions = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatExcessiveCollisions.setStatus("current")
sysDot3StatIntmacTxErrors = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatIntmacTxErrors.setStatus("current")
sysDot3StatCarrierSenseErrors = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatCarrierSenseErrors.setStatus("current")
sysDot3StatFrameTooLongs = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatFrameTooLongs.setStatus("current")
sysDot3StatIntmacRxErrors = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatIntmacRxErrors.setStatus("current")
sysDot3StatSymbolErrors = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatSymbolErrors.setStatus("current")
sysDot3StatDuplexStatus = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 15),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(1, 2, 3))
    .clone(
        namedValues=NamedValues(("unknown", 1), ("halfDuplex", 2), ("fullDuplex", 3))
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatDuplexStatus.setStatus("current")
sysDot3StatCollisionCount = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatCollisionCount.setStatus("current")
sysDot3StatCollisionFreq = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 11, 1, 3, 1, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysDot3StatCollisionFreq.setStatus("current")
sysTrunkNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkNumber.setStatus("current")
sysTrunkTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2),
)
if mibBuilder.loadTexts:
    sysTrunkTable.setStatus("current")
sysTrunkEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysTrunkName"))
if mibBuilder.loadTexts:
    sysTrunkEntry.setStatus("current")
sysTrunkName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkName.setStatus("current")
sysTrunkStatus = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1, 2),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4, 5))
    .clone(
        namedValues=NamedValues(
            ("up", 0),
            ("down", 1),
            ("disable", 2),
            ("uninitialized", 3),
            ("loopback", 4),
            ("unpopulated", 5),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatus.setStatus("current")
sysTrunkAggAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1, 3), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkAggAddr.setStatus("current")
sysTrunkCfgMbrCount = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkCfgMbrCount.setStatus("current")
sysTrunkOperBw = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkOperBw.setStatus("current")
sysTrunkStpEnable = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1, 6),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStpEnable.setStatus("current")
sysTrunkStpReset = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1, 7),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStpReset.setStatus("current")
sysTrunkLacpEnabled = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1, 8),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkLacpEnabled.setStatus("current")
sysTrunkActiveLacp = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1, 9),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkActiveLacp.setStatus("current")
sysTrunkShortTimeout = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 1, 2, 1, 10),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkShortTimeout.setStatus("current")
sysTrunkStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysTrunkStatResetStats.setStatus("current")
sysTrunkStatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatNumber.setStatus("current")
sysTrunkStatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3),
)
if mibBuilder.loadTexts:
    sysTrunkStatTable.setStatus("current")
sysTrunkStatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysTrunkStatName"))
if mibBuilder.loadTexts:
    sysTrunkStatEntry.setStatus("current")
sysTrunkStatName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatName.setStatus("current")
sysTrunkStatPktsIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatPktsIn.setStatus("current")
sysTrunkStatBytesIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatBytesIn.setStatus("current")
sysTrunkStatPktsOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatPktsOut.setStatus("current")
sysTrunkStatBytesOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatBytesOut.setStatus("current")
sysTrunkStatMcastIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatMcastIn.setStatus("current")
sysTrunkStatMcastOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatMcastOut.setStatus("current")
sysTrunkStatErrorsIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatErrorsIn.setStatus("current")
sysTrunkStatErrorsOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatErrorsOut.setStatus("current")
sysTrunkStatDropsIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatDropsIn.setStatus("current")
sysTrunkStatDropsOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatDropsOut.setStatus("current")
sysTrunkStatCollisions = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 2, 3, 1, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkStatCollisions.setStatus("current")
sysTrunkCfgMemberNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 3, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkCfgMemberNumber.setStatus("current")
sysTrunkCfgMemberTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 3, 2),
)
if mibBuilder.loadTexts:
    sysTrunkCfgMemberTable.setStatus("current")
sysTrunkCfgMemberEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 3, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysTrunkCfgMemberTrunkName"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysTrunkCfgMemberName"),
)
if mibBuilder.loadTexts:
    sysTrunkCfgMemberEntry.setStatus("current")
sysTrunkCfgMemberTrunkName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 3, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkCfgMemberTrunkName.setStatus("current")
sysTrunkCfgMemberName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 12, 3, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTrunkCfgMemberName.setStatus("current")
sysVlanNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanNumber.setStatus("current")
sysVlanTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2),
)
if mibBuilder.loadTexts:
    sysVlanTable.setStatus("current")
sysVlanEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysVlanVname"))
if mibBuilder.loadTexts:
    sysVlanEntry.setStatus("current")
sysVlanVname = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanVname.setStatus("current")
sysVlanId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanId.setStatus("current")
sysVlanSpanningTree = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 3),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanSpanningTree.setStatus("current")
sysVlanMacMasquerade = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 4), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanMacMasquerade.setStatus("current")
sysVlanMacTrue = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 5), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanMacTrue.setStatus("current")
sysVlanSourceCheck = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 6),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanSourceCheck.setStatus("current")
sysVlanFailsafeEnabled = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 7),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanFailsafeEnabled.setStatus("current")
sysVlanMtu = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 8), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanMtu.setStatus("current")
sysVlanFailsafeTimeout = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 9), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanFailsafeTimeout.setStatus("current")
sysVlanFailsafeAction = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 10),
    Integer32()
    .subtype(
        subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    )
    .clone(
        namedValues=NamedValues(
            ("unusedhaaction", 0),
            ("reboot", 1),
            ("restart", 2),
            ("failover", 3),
            ("goactive", 4),
            ("noaction", 5),
            ("restartall", 6),
            ("failoveraborttm", 7),
            ("gooffline", 8),
            ("goofflinerestart", 9),
            ("goofflineaborttm", 10),
            ("goofflinedownlinks", 11),
            ("goofflinedownlinksrestart", 12),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanFailsafeAction.setStatus("current")
sysVlanMirrorHashPortEnable = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 11),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanMirrorHashPortEnable.setStatus("current")
sysVlanLearnMode = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 1, 2, 1, 12),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2))
    .clone(
        namedValues=NamedValues(
            ("learnforward", 0), ("nolearnforward", 1), ("nolearndrop", 2)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanLearnMode.setStatus("current")
sysVlanMemberNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanMemberNumber.setStatus("current")
sysVlanMemberTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 2, 2),
)
if mibBuilder.loadTexts:
    sysVlanMemberTable.setStatus("current")
sysVlanMemberEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 2, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysVlanMemberParentVname"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysVlanMemberVmname"),
)
if mibBuilder.loadTexts:
    sysVlanMemberEntry.setStatus("current")
sysVlanMemberVmname = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 2, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanMemberVmname.setStatus("current")
sysVlanMemberParentVname = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 2, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanMemberParentVname.setStatus("current")
sysVlanMemberTagged = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 2, 2, 1, 3),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanMemberTagged.setStatus("current")
sysVlanMemberType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 2, 2, 1, 4),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("interface", 0), ("trunk", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanMemberType.setStatus("current")
sysVlanGroupNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupNumber.setStatus("current")
sysVlanGroupTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 2),
)
if mibBuilder.loadTexts:
    sysVlanGroupTable.setStatus("current")
sysVlanGroupEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysVlanGroupName"))
if mibBuilder.loadTexts:
    sysVlanGroupEntry.setStatus("current")
sysVlanGroupName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupName.setStatus("current")
sysVlanGroupVlanId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupVlanId.setStatus("deprecated")
sysVlanGroupMode = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 2, 1, 3),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2))
    .clone(
        namedValues=NamedValues(("transparent", 0), ("translucent", 1), ("opaque", 2))
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupMode.setStatus("current")
sysVlanGroupBridgeAllTraffic = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 2, 1, 4),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupBridgeAllTraffic.setStatus("current")
sysVlanGroupBridgeInStandby = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 2, 1, 5),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupBridgeInStandby.setStatus("current")
sysVlanGroupBridgeMulticast = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 2, 1, 6),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupBridgeMulticast.setStatus("current")
sysVlanGroupMacMasquerade = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 2, 1, 7), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupMacMasquerade.setStatus("current")
sysVlanGroupMacTrue = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 3, 2, 1, 8), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupMacTrue.setStatus("current")
sysVlanGroupMbrNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 4, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupMbrNumber.setStatus("current")
sysVlanGroupMbrTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 4, 2),
)
if mibBuilder.loadTexts:
    sysVlanGroupMbrTable.setStatus("current")
sysVlanGroupMbrEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 4, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysVlanGroupMbrGroupName"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysVlanGroupMbrVlanName"),
)
if mibBuilder.loadTexts:
    sysVlanGroupMbrEntry.setStatus("current")
sysVlanGroupMbrGroupName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 4, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupMbrGroupName.setStatus("current")
sysVlanGroupMbrVlanName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 4, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysVlanGroupMbrVlanName.setStatus("current")
sysProxyExclusionNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 5, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysProxyExclusionNumber.setStatus("current")
sysProxyExclusionTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 5, 2),
)
if mibBuilder.loadTexts:
    sysProxyExclusionTable.setStatus("current")
sysProxyExclusionEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 5, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysProxyExclusionVlangroupName"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysProxyExclusionIpType"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysProxyExclusionIp"),
)
if mibBuilder.loadTexts:
    sysProxyExclusionEntry.setStatus("current")
sysProxyExclusionVlangroupName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 5, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysProxyExclusionVlangroupName.setStatus("current")
sysProxyExclusionIpType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 5, 2, 1, 2), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysProxyExclusionIpType.setStatus("current")
sysProxyExclusionIp = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 13, 5, 2, 1, 3), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysProxyExclusionIp.setStatus("current")
sysCpuNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysCpuNumber.setStatus("current")
sysCpuTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 1, 2),
)
if mibBuilder.loadTexts:
    sysCpuTable.setStatus("current")
pysmiFakeCol1000 = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 1, 2, 1) + (1000,), Integer32()
)
sysCpuEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 1, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "pysmiFakeCol1000"))
if mibBuilder.loadTexts:
    sysCpuEntry.setStatus("current")
sysCpuIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 1, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysCpuIndex.setStatus("current")
sysCpuTemperature = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 1, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysCpuTemperature.setStatus("current")
sysCpuFanSpeed = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 1, 2, 1, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysCpuFanSpeed.setStatus("current")
sysCpuName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 1, 2, 1, 4), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysCpuName.setStatus("current")
sysCpuSlot = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 1, 2, 1, 5),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysCpuSlot.setStatus("current")
sysChassisFanNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysChassisFanNumber.setStatus("current")
sysChassisFanTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 1, 2),
)
if mibBuilder.loadTexts:
    sysChassisFanTable.setStatus("current")
sysChassisFanEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 1, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysChassisFanIndex"))
if mibBuilder.loadTexts:
    sysChassisFanEntry.setStatus("current")
sysChassisFanIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 1, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysChassisFanIndex.setStatus("current")
sysChassisFanStatus = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 1, 2, 1, 2),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2))
    .clone(namedValues=NamedValues(("bad", 0), ("good", 1), ("notpresent", 2))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysChassisFanStatus.setStatus("current")
sysChassisFanSpeed = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 1, 2, 1, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysChassisFanSpeed.setStatus("current")
sysChassisPowerSupplyNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysChassisPowerSupplyNumber.setStatus("current")
sysChassisPowerSupplyTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 2, 2),
)
if mibBuilder.loadTexts:
    sysChassisPowerSupplyTable.setStatus("current")
sysChassisPowerSupplyEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 2, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysChassisPowerSupplyIndex"))
if mibBuilder.loadTexts:
    sysChassisPowerSupplyEntry.setStatus("current")
sysChassisPowerSupplyIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 2, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysChassisPowerSupplyIndex.setStatus("current")
sysChassisPowerSupplyStatus = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 2, 2, 1, 2),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2))
    .clone(namedValues=NamedValues(("bad", 0), ("good", 1), ("notpresent", 2))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysChassisPowerSupplyStatus.setStatus("current")
sysChassisTempNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 3, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysChassisTempNumber.setStatus("current")
sysChassisTempTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 3, 2),
)
if mibBuilder.loadTexts:
    sysChassisTempTable.setStatus("current")
sysChassisTempEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 3, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysChassisTempIndex"))
if mibBuilder.loadTexts:
    sysChassisTempEntry.setStatus("current")
sysChassisTempIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 3, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysChassisTempIndex.setStatus("current")
sysChassisTempTemperature = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 2, 3, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysChassisTempTemperature.setStatus("current")
sysProductName = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 4, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysProductName.setStatus("current")
sysProductVersion = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 4, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysProductVersion.setStatus("current")
sysProductBuild = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 4, 3), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysProductBuild.setStatus("current")
sysProductEdition = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 4, 4), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysProductEdition.setStatus("current")
sysProductDate = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 4, 5), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysProductDate.setStatus("current")
sysProductHotfix = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 4, 6), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysProductHotfix.setStatus("deprecated")
sysSubMemoryResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 5, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysSubMemoryResetStats.setStatus("deprecated")
sysSubMemoryNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 5, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSubMemoryNumber.setStatus("deprecated")
sysSubMemoryTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 5, 3),
)
if mibBuilder.loadTexts:
    sysSubMemoryTable.setStatus("deprecated")
sysSubMemoryEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 5, 3, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysSubMemoryName"))
if mibBuilder.loadTexts:
    sysSubMemoryEntry.setStatus("deprecated")
sysSubMemoryName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 5, 3, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSubMemoryName.setStatus("deprecated")
sysSubMemoryAllocated = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 5, 3, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSubMemoryAllocated.setStatus("deprecated")
sysSubMemoryMaxAllocated = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 5, 3, 1, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSubMemoryMaxAllocated.setStatus("deprecated")
sysSubMemorySize = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 5, 3, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSubMemorySize.setStatus("deprecated")
sysSystemName = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 6, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSystemName.setStatus("current")
sysSystemNodeName = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 6, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSystemNodeName.setStatus("current")
sysSystemRelease = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 6, 3), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSystemRelease.setStatus("current")
sysSystemVersion = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 6, 4), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSystemVersion.setStatus("current")
sysSystemMachine = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 6, 5), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSystemMachine.setStatus("current")
sysSystemUptime = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 6, 6), TimeTicks()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSystemUptime.setStatus("current")
sysFastHttpStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysFastHttpStatResetStats.setStatus("current")
sysFastHttpStatClientSyns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatClientSyns.setStatus("current")
sysFastHttpStatClientAccepts = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatClientAccepts.setStatus("current")
sysFastHttpStatServerConnects = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatServerConnects.setStatus("current")
sysFastHttpStatConnpoolCurSize = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatConnpoolCurSize.setStatus("current")
sysFastHttpStatConnpoolMaxSize = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 6), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatConnpoolMaxSize.setStatus("current")
sysFastHttpStatConnpoolReuses = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatConnpoolReuses.setStatus("current")
sysFastHttpStatConnpoolExhausted = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatConnpoolExhausted.setStatus("current")
sysFastHttpStatNumberReqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatNumberReqs.setStatus("current")
sysFastHttpStatUnbufferedReqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatUnbufferedReqs.setStatus("current")
sysFastHttpStatGetReqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatGetReqs.setStatus("current")
sysFastHttpStatPostReqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatPostReqs.setStatus("current")
sysFastHttpStatV9Reqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatV9Reqs.setStatus("current")
sysFastHttpStatV10Reqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatV10Reqs.setStatus("current")
sysFastHttpStatV11Reqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatV11Reqs.setStatus("current")
sysFastHttpStatResp2xxCnt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatResp2xxCnt.setStatus("current")
sysFastHttpStatResp3xxCnt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatResp3xxCnt.setStatus("current")
sysFastHttpStatResp4xxCnt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatResp4xxCnt.setStatus("current")
sysFastHttpStatResp5xxCnt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 19), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatResp5xxCnt.setStatus("current")
sysFastHttpStatReqParseErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 20), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatReqParseErrors.setStatus("current")
sysFastHttpStatRespParseErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 21), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatRespParseErrors.setStatus("current")
sysFastHttpStatClientRxBad = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 22), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatClientRxBad.setStatus("current")
sysFastHttpStatServerRxBad = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 23), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatServerRxBad.setStatus("current")
sysFastHttpStatPipelinedReqs = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 14, 24), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastHttpStatPipelinedReqs.setStatus("current")
sysXmlStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 15, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysXmlStatResetStats.setStatus("current")
sysXmlStatNumErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 15, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysXmlStatNumErrors.setStatus("deprecated")
sysGeneralHwName = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 3, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGeneralHwName.setStatus("current")
sysGeneralHwNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 3, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGeneralHwNumber.setStatus("deprecated")
sysGeneralChassisSerialNum = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 3, 3), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGeneralChassisSerialNum.setStatus("current")
sysIiopStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 16, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysIiopStatResetStats.setStatus("current")
sysIiopStatNumRequests = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 16, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIiopStatNumRequests.setStatus("current")
sysIiopStatNumResponses = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 16, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIiopStatNumResponses.setStatus("current")
sysIiopStatNumCancels = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 16, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIiopStatNumCancels.setStatus("current")
sysIiopStatNumErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 16, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIiopStatNumErrors.setStatus("current")
sysIiopStatNumFragments = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 16, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIiopStatNumFragments.setStatus("current")
sysRtspStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 17, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysRtspStatResetStats.setStatus("current")
sysRtspStatNumRequests = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 17, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRtspStatNumRequests.setStatus("current")
sysRtspStatNumResponses = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 17, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRtspStatNumResponses.setStatus("current")
sysRtspStatNumErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 17, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRtspStatNumErrors.setStatus("current")
sysRtspStatNumInterleavedData = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 17, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysRtspStatNumInterleavedData.setStatus("current")
sysSctpStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysSctpStatResetStats.setStatus("current")
sysSctpStatAccepts = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSctpStatAccepts.setStatus("current")
sysSctpStatAcceptfails = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSctpStatAcceptfails.setStatus("current")
sysSctpStatConnects = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSctpStatConnects.setStatus("current")
sysSctpStatConnfails = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSctpStatConnfails.setStatus("current")
sysSctpStatExpires = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSctpStatExpires.setStatus("current")
sysSctpStatAbandons = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSctpStatAbandons.setStatus("current")
sysSctpStatRxrst = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSctpStatRxrst.setStatus("current")
sysSctpStatRxbadsum = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSctpStatRxbadsum.setStatus("current")
sysSctpStatRxcookie = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSctpStatRxcookie.setStatus("current")
sysSctpStatRxbadcookie = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 18, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSctpStatRxbadcookie.setStatus("current")
sysL2ForwardStatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardStatNumber.setStatus("current")
sysL2ForwardStatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 2, 2),
)
if mibBuilder.loadTexts:
    sysL2ForwardStatTable.setStatus("current")
sysL2ForwardStatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 2, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysL2ForwardStatVlanName"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysL2ForwardStatMacAddr"),
)
if mibBuilder.loadTexts:
    sysL2ForwardStatEntry.setStatus("current")
sysL2ForwardStatVlanName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 2, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardStatVlanName.setStatus("current")
sysL2ForwardStatMacAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 2, 2, 1, 2), MacAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardStatMacAddr.setStatus("current")
sysL2ForwardStatIfname = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 2, 2, 1, 3), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardStatIfname.setStatus("current")
sysL2ForwardStatIftype = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 2, 2, 1, 4),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("interface", 0), ("trunk", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardStatIftype.setStatus("current")
sysL2ForwardStatDynamic = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 2, 2, 1, 5),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysL2ForwardStatDynamic.setStatus("current")
sysL2ForwardAttrVlan = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 5, 3, 1), LongDisplayString()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysL2ForwardAttrVlan.setStatus("current")
sysHostMemoryTotal = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 1, 1), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostMemoryTotal.setStatus("current")
sysHostMemoryUsed = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostMemoryUsed.setStatus("current")
sysHostCpuNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostCpuNumber.setStatus("deprecated")
sysHostCpuTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2),
)
if mibBuilder.loadTexts:
    sysHostCpuTable.setStatus("deprecated")
sysHostCpuEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysHostCpuIndex"))
if mibBuilder.loadTexts:
    sysHostCpuEntry.setStatus("deprecated")
sysHostCpuIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostCpuIndex.setStatus("deprecated")
sysHostCpuId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostCpuId.setStatus("deprecated")
sysHostCpuUser = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2, 1, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostCpuUser.setStatus("deprecated")
sysHostCpuNice = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostCpuNice.setStatus("deprecated")
sysHostCpuSystem = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostCpuSystem.setStatus("deprecated")
sysHostCpuIdle = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2, 1, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostCpuIdle.setStatus("deprecated")
sysHostCpuIrq = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2, 1, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostCpuIrq.setStatus("deprecated")
sysHostCpuSoftirq = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2, 1, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostCpuSoftirq.setStatus("deprecated")
sysHostCpuIowait = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 2, 2, 1, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostCpuIowait.setStatus("deprecated")
sysHostDiskNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 3, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostDiskNumber.setStatus("current")
sysHostDiskTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 3, 2),
)
if mibBuilder.loadTexts:
    sysHostDiskTable.setStatus("current")
sysHostDiskEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 3, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysHostDiskPartition"))
if mibBuilder.loadTexts:
    sysHostDiskEntry.setStatus("current")
sysHostDiskPartition = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 3, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostDiskPartition.setStatus("current")
sysHostDiskBlockSize = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 3, 2, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostDiskBlockSize.setStatus("current")
sysHostDiskTotalBlocks = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 3, 2, 1, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostDiskTotalBlocks.setStatus("current")
sysHostDiskFreeBlocks = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 3, 2, 1, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostDiskFreeBlocks.setStatus("current")
sysHostDiskTotalNodes = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 3, 2, 1, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostDiskTotalNodes.setStatus("current")
sysHostDiskFreeNodes = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 3, 2, 1, 6), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysHostDiskFreeNodes.setStatus("current")
sysSelfPortDefNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfPortDefNumber.setStatus("current")
sysSelfPortDefTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 2, 2),
)
if mibBuilder.loadTexts:
    sysSelfPortDefTable.setStatus("current")
sysSelfPortDefEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 2, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSelfPortDefProtocol"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSelfPortDefPort"),
)
if mibBuilder.loadTexts:
    sysSelfPortDefEntry.setStatus("current")
sysSelfPortDefProtocol = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 2, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfPortDefProtocol.setStatus("current")
sysSelfPortDefPort = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 9, 2, 2, 1, 2),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSelfPortDefPort.setStatus("current")
sysIntfMediaSfpNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 6, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIntfMediaSfpNumber.setStatus("current")
sysIntfMediaSfpTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 6, 2),
)
if mibBuilder.loadTexts:
    sysIntfMediaSfpTable.setStatus("current")
sysIntfMediaSfpEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 6, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysIntfMediaSfpName"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysIntfMediaSfpIndex"),
)
if mibBuilder.loadTexts:
    sysIntfMediaSfpEntry.setStatus("current")
sysIntfMediaSfpName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 6, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIntfMediaSfpName.setStatus("current")
sysIntfMediaSfpIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 6, 2, 1, 2),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIntfMediaSfpIndex.setStatus("current")
sysIntfMediaSfpType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 6, 2, 1, 3),
    Integer32()
    .subtype(
        subtypeSpec=SingleValueConstraint(
            1, 2, 3, 4, 5, 6, 10, 13, 14, 16, 18, 19, 20, 21
        )
    )
    .clone(
        namedValues=NamedValues(
            ("media10THdx", 1),
            ("media10TFdx", 2),
            ("media100TxHdx", 3),
            ("media100TxFdx", 4),
            ("media1000THdx", 5),
            ("media1000TFdx", 6),
            ("media10000TFdx", 10),
            ("mediaAuto", 13),
            ("mediaInternal", 14),
            ("media1000SxFdx", 16),
            ("media1000LxFdx", 18),
            ("media10000SrFdx", 19),
            ("media10000LrFdx", 20),
            ("media10000ErFdx", 21),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysIntfMediaSfpType.setStatus("current")
sysPvaStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysPvaStatResetStats.setStatus("current")
sysPvaStatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatNumber.setStatus("current")
sysPvaStatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3),
)
if mibBuilder.loadTexts:
    sysPvaStatTable.setStatus("current")
sysPvaStatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysPvaStatPvaId"))
if mibBuilder.loadTexts:
    sysPvaStatEntry.setStatus("current")
sysPvaStatPvaId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatPvaId.setStatus("current")
sysPvaStatClientPktsIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatClientPktsIn.setStatus("current")
sysPvaStatClientBytesIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatClientBytesIn.setStatus("current")
sysPvaStatClientPktsOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatClientPktsOut.setStatus("current")
sysPvaStatClientBytesOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatClientBytesOut.setStatus("current")
sysPvaStatClientMaxConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatClientMaxConns.setStatus("current")
sysPvaStatClientTotConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatClientTotConns.setStatus("current")
sysPvaStatClientCurConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatClientCurConns.setStatus("current")
sysPvaStatServerPktsIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatServerPktsIn.setStatus("current")
sysPvaStatServerBytesIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatServerBytesIn.setStatus("current")
sysPvaStatServerPktsOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatServerPktsOut.setStatus("current")
sysPvaStatServerBytesOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatServerBytesOut.setStatus("current")
sysPvaStatServerMaxConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatServerMaxConns.setStatus("current")
sysPvaStatServerTotConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatServerTotConns.setStatus("current")
sysPvaStatServerCurConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatServerCurConns.setStatus("current")
sysPvaStatTotAssistConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatTotAssistConns.setStatus("current")
sysPvaStatCurAssistConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatCurAssistConns.setStatus("current")
sysPvaStatHardSyncookieGen = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatHardSyncookieGen.setStatus("current")
sysPvaStatHardSyncookieDet = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 1, 3, 1, 19), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPvaStatHardSyncookieDet.setStatus("current")
sysTmmStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysTmmStatResetStats.setStatus("current")
sysTmmStatNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatNumber.setStatus("current")
sysTmmStatTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3),
)
if mibBuilder.loadTexts:
    sysTmmStatTable.setStatus("current")
sysTmmStatEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysTmmStatTmmId"))
if mibBuilder.loadTexts:
    sysTmmStatEntry.setStatus("current")
sysTmmStatTmmId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatTmmId.setStatus("current")
sysTmmStatTmmPid = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatTmmPid.setStatus("current")
sysTmmStatCpu = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatCpu.setStatus("current")
sysTmmStatTmid = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatTmid.setStatus("current")
sysTmmStatNpus = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatNpus.setStatus("current")
sysTmmStatClientPktsIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatClientPktsIn.setStatus("current")
sysTmmStatClientBytesIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatClientBytesIn.setStatus("current")
sysTmmStatClientPktsOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatClientPktsOut.setStatus("current")
sysTmmStatClientBytesOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatClientBytesOut.setStatus("current")
sysTmmStatClientMaxConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatClientMaxConns.setStatus("current")
sysTmmStatClientTotConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatClientTotConns.setStatus("current")
sysTmmStatClientCurConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatClientCurConns.setStatus("current")
sysTmmStatServerPktsIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatServerPktsIn.setStatus("current")
sysTmmStatServerBytesIn = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatServerBytesIn.setStatus("current")
sysTmmStatServerPktsOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatServerPktsOut.setStatus("current")
sysTmmStatServerBytesOut = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatServerBytesOut.setStatus("current")
sysTmmStatServerMaxConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatServerMaxConns.setStatus("current")
sysTmmStatServerTotConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatServerTotConns.setStatus("current")
sysTmmStatServerCurConns = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 19), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatServerCurConns.setStatus("current")
sysTmmStatMaintenanceModeDeny = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 20), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatMaintenanceModeDeny.setStatus("current")
sysTmmStatMaxConnVirtualAddrDeny = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 21), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatMaxConnVirtualAddrDeny.setStatus("current")
sysTmmStatMaxConnVirtualPathDeny = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 22), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatMaxConnVirtualPathDeny.setStatus("current")
sysTmmStatVirtualServerNonSynDeny = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 23), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatVirtualServerNonSynDeny.setStatus("current")
sysTmmStatNoHandlerDeny = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 24), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatNoHandlerDeny.setStatus("current")
sysTmmStatLicenseDeny = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 25), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatLicenseDeny.setStatus("current")
sysTmmStatCmpConnRedirected = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 26), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatCmpConnRedirected.setStatus("current")
sysTmmStatConnectionMemoryErrors = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 27), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatConnectionMemoryErrors.setStatus("current")
sysTmmStatTmTotalCycles = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 28), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatTmTotalCycles.setStatus("deprecated")
sysTmmStatTmIdleCycles = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 29), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatTmIdleCycles.setStatus("deprecated")
sysTmmStatTmSleepCycles = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 30), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatTmSleepCycles.setStatus("deprecated")
sysTmmStatMemoryTotal = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 31), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatMemoryTotal.setStatus("current")
sysTmmStatMemoryUsed = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 32), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatMemoryUsed.setStatus("current")
sysTmmStatDroppedPackets = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 33), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatDroppedPackets.setStatus("current")
sysTmmStatIncomingPacketErrors = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 34), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatIncomingPacketErrors.setStatus("current")
sysTmmStatOutgoingPacketErrors = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 35), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatOutgoingPacketErrors.setStatus("current")
sysTmmStatHttpRequests = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 36), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatHttpRequests.setStatus("current")
sysTmmStatTmUsageRatio5s = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 37), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatTmUsageRatio5s.setStatus("current")
sysTmmStatTmUsageRatio1m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 38), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatTmUsageRatio1m.setStatus("current")
sysTmmStatTmUsageRatio5m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 8, 2, 3, 1, 39), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysTmmStatTmUsageRatio5m.setStatus("current")
sysMultiHostNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 4, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostNumber.setStatus("current")
sysMultiHostTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 4, 2),
)
if mibBuilder.loadTexts:
    sysMultiHostTable.setStatus("current")
sysMultiHostEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 4, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysMultiHostHostId"))
if mibBuilder.loadTexts:
    sysMultiHostEntry.setStatus("current")
sysMultiHostHostId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 4, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostHostId.setStatus("current")
sysMultiHostTotal = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 4, 2, 1, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostTotal.setStatus("current")
sysMultiHostUsed = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 4, 2, 1, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostUsed.setStatus("current")
sysMultiHostMode = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 4, 2, 1, 4),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("modeup", 0), ("modesmp", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostMode.setStatus("deprecated")
sysMultiHostCpuCount = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 4, 2, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuCount.setStatus("current")
sysMultiHostActiveCpuCount = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 4, 2, 1, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostActiveCpuCount.setStatus("current")
sysMultiHostCpuNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuNumber.setStatus("current")
sysMultiHostCpuTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2),
)
if mibBuilder.loadTexts:
    sysMultiHostCpuTable.setStatus("current")
sysMultiHostCpuEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuHostId"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIndex"),
)
if mibBuilder.loadTexts:
    sysMultiHostCpuEntry.setStatus("current")
sysMultiHostCpuHostId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuHostId.setStatus("current")
sysMultiHostCpuIndex = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 2),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIndex.setStatus("current")
sysMultiHostCpuId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuId.setStatus("current")
sysMultiHostCpuUser = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuUser.setStatus("current")
sysMultiHostCpuNice = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuNice.setStatus("current")
sysMultiHostCpuSystem = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuSystem.setStatus("current")
sysMultiHostCpuIdle = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIdle.setStatus("current")
sysMultiHostCpuIrq = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIrq.setStatus("current")
sysMultiHostCpuSoftirq = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuSoftirq.setStatus("current")
sysMultiHostCpuIowait = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIowait.setStatus("current")
sysMultiHostCpuUsageRatio = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 11), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuUsageRatio.setStatus("current")
sysMultiHostCpuUser5s = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuUser5s.setStatus("current")
sysMultiHostCpuNice5s = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuNice5s.setStatus("current")
sysMultiHostCpuSystem5s = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuSystem5s.setStatus("current")
sysMultiHostCpuIdle5s = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIdle5s.setStatus("current")
sysMultiHostCpuIrq5s = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIrq5s.setStatus("current")
sysMultiHostCpuSoftirq5s = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuSoftirq5s.setStatus("current")
sysMultiHostCpuIowait5s = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIowait5s.setStatus("current")
sysMultiHostCpuUsageRatio5s = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 19), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuUsageRatio5s.setStatus("current")
sysMultiHostCpuUser1m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 20), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuUser1m.setStatus("current")
sysMultiHostCpuNice1m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 21), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuNice1m.setStatus("current")
sysMultiHostCpuSystem1m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 22), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuSystem1m.setStatus("current")
sysMultiHostCpuIdle1m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 23), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIdle1m.setStatus("current")
sysMultiHostCpuIrq1m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 24), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIrq1m.setStatus("current")
sysMultiHostCpuSoftirq1m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 25), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuSoftirq1m.setStatus("current")
sysMultiHostCpuIowait1m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 26), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIowait1m.setStatus("current")
sysMultiHostCpuUsageRatio1m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 27), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuUsageRatio1m.setStatus("current")
sysMultiHostCpuUser5m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 28), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuUser5m.setStatus("current")
sysMultiHostCpuNice5m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 29), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuNice5m.setStatus("current")
sysMultiHostCpuSystem5m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 30), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuSystem5m.setStatus("current")
sysMultiHostCpuIdle5m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 31), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIdle5m.setStatus("current")
sysMultiHostCpuIrq5m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 32), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIrq5m.setStatus("current")
sysMultiHostCpuSoftirq5m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 33), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuSoftirq5m.setStatus("current")
sysMultiHostCpuIowait5m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 34), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuIowait5m.setStatus("current")
sysMultiHostCpuUsageRatio5m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 35), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuUsageRatio5m.setStatus("current")
sysMultiHostCpuStolen = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 36), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuStolen.setStatus("current")
sysMultiHostCpuStolen5s = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 37), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuStolen5s.setStatus("current")
sysMultiHostCpuStolen1m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 38), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuStolen1m.setStatus("current")
sysMultiHostCpuStolen5m = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 7, 5, 2, 1, 39), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysMultiHostCpuStolen5m.setStatus("current")
sysFastL4StatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysFastL4StatResetStats.setStatus("current")
sysFastL4StatOpen = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 2), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatOpen.setStatus("current")
sysFastL4StatAccepts = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatAccepts.setStatus("current")
sysFastL4StatAcceptfails = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatAcceptfails.setStatus("current")
sysFastL4StatExpires = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatExpires.setStatus("current")
sysFastL4StatRxbadpkt = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatRxbadpkt.setStatus("current")
sysFastL4StatRxunreach = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatRxunreach.setStatus("current")
sysFastL4StatRxbadunreach = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatRxbadunreach.setStatus("current")
sysFastL4StatRxbadsum = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatRxbadsum.setStatus("current")
sysFastL4StatTxerrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatTxerrors.setStatus("current")
sysFastL4StatSyncookIssue = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatSyncookIssue.setStatus("current")
sysFastL4StatSyncookAccept = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatSyncookAccept.setStatus("current")
sysFastL4StatSyncookReject = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatSyncookReject.setStatus("current")
sysFastL4StatServersynrtx = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 19, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysFastL4StatServersynrtx.setStatus("current")
sysClusterNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterNumber.setStatus("current")
sysClusterTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2),
)
if mibBuilder.loadTexts:
    sysClusterTable.setStatus("current")
sysClusterEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysClusterName"))
if mibBuilder.loadTexts:
    sysClusterEntry.setStatus("current")
sysClusterName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterName.setStatus("current")
sysClusterEnabled = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 2),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterEnabled.setStatus("current")
sysClusterFloatMgmtIpType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 3), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterFloatMgmtIpType.setStatus("current")
sysClusterFloatMgmtIp = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 4), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterFloatMgmtIp.setStatus("current")
sysClusterFloatMgmtNetmaskType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 5), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterFloatMgmtNetmaskType.setStatus("current")
sysClusterFloatMgmtNetmask = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 6), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterFloatMgmtNetmask.setStatus("current")
sysClusterMinUpMbrs = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 7), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMinUpMbrs.setStatus("current")
sysClusterMinUpMbrsEnable = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 8), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMinUpMbrsEnable.setStatus("current")
sysClusterMinUpMbrsAction = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 9),
    Integer32()
    .subtype(
        subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    )
    .clone(
        namedValues=NamedValues(
            ("unusedhaaction", 0),
            ("reboot", 1),
            ("restart", 2),
            ("failover", 3),
            ("goactive", 4),
            ("noaction", 5),
            ("restartall", 6),
            ("failoveraborttm", 7),
            ("gooffline", 8),
            ("goofflinerestart", 9),
            ("goofflineaborttm", 10),
            ("goofflinedownlinks", 11),
            ("goofflinedownlinksrestart", 12),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMinUpMbrsAction.setStatus("current")
sysClusterAvailabilityState = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 10),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4))
    .clone(
        namedValues=NamedValues(
            ("none", 0), ("green", 1), ("yellow", 2), ("red", 3), ("blue", 4)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterAvailabilityState.setStatus("current")
sysClusterEnabledStat = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 11),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3))
    .clone(
        namedValues=NamedValues(
            ("none", 0), ("enabled", 1), ("disabled", 2), ("disabledbyparent", 3)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterEnabledStat.setStatus("current")
sysClusterDisabledParentType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 12), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterDisabledParentType.setStatus("current")
sysClusterStatusReason = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 13), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterStatusReason.setStatus("current")
sysClusterHaState = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 14),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4))
    .clone(
        namedValues=NamedValues(
            ("offline", 0),
            ("forcedoffline", 1),
            ("standby", 2),
            ("active", 3),
            ("unknown", 4),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterHaState.setStatus("current")
sysClusterPriSlotId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 15), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterPriSlotId.setStatus("current")
sysClusterLastPriSlotId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 16), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterLastPriSlotId.setStatus("current")
sysClusterPriSelTime = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 1, 2, 1, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterPriSelTime.setStatus("current")
sysClusterMbrNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrNumber.setStatus("current")
sysClusterMbrTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2),
)
if mibBuilder.loadTexts:
    sysClusterMbrTable.setStatus("current")
sysClusterMbrEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysClusterMbrCluster"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysClusterMbrSlotId"),
)
if mibBuilder.loadTexts:
    sysClusterMbrEntry.setStatus("current")
sysClusterMbrCluster = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrCluster.setStatus("current")
sysClusterMbrSlotId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 2),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrSlotId.setStatus("current")
sysClusterMbrAvailabilityState = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 3),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4))
    .clone(
        namedValues=NamedValues(
            ("none", 0), ("green", 1), ("yellow", 2), ("red", 3), ("blue", 4)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrAvailabilityState.setStatus("current")
sysClusterMbrEnabledStat = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 4),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3))
    .clone(
        namedValues=NamedValues(
            ("none", 0), ("enabled", 1), ("disabled", 2), ("disabledbyparent", 3)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrEnabledStat.setStatus("current")
sysClusterMbrDisabledParentType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrDisabledParentType.setStatus("current")
sysClusterMbrStatusReason = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 6), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrStatusReason.setStatus("current")
sysClusterMbrLicensed = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 7),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrLicensed.setStatus("current")
sysClusterMbrState = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 8),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1, 2, 3, 4))
    .clone(
        namedValues=NamedValues(
            ("initial", 0),
            ("quorumwait", 1),
            ("quorum", 2),
            ("running", 3),
            ("shutdown", 4),
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrState.setStatus("current")
sysClusterMbrEnabled = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 9),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrEnabled.setStatus("current")
sysClusterMbrPriming = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 10),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrPriming.setStatus("current")
sysClusterMbrMgmtAddrType = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 11), InetAddressType()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrMgmtAddrType.setStatus("current")
sysClusterMbrMgmtAddr = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 10, 2, 2, 1, 12), InetAddress()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysClusterMbrMgmtAddr.setStatus("current")
sysSwVolumeNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwVolumeNumber.setStatus("current")
sysSwVolumeTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 1, 2),
)
if mibBuilder.loadTexts:
    sysSwVolumeTable.setStatus("current")
sysSwVolumeEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 1, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSwVolumeSlotId"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSwVolumeName"),
)
if mibBuilder.loadTexts:
    sysSwVolumeEntry.setStatus("current")
sysSwVolumeSlotId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 1, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwVolumeSlotId.setStatus("current")
sysSwVolumeName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 1, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwVolumeName.setStatus("current")
sysSwVolumeSize = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 1, 2, 1, 3), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwVolumeSize.setStatus("current")
sysSwVolumeActive = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 1, 2, 1, 4),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwVolumeActive.setStatus("current")
sysSwImageNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageNumber.setStatus("current")
sysSwImageTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2),
)
if mibBuilder.loadTexts:
    sysSwImageTable.setStatus("current")
sysSwImageEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSwImageSlotId"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSwImageFilename"),
)
if mibBuilder.loadTexts:
    sysSwImageEntry.setStatus("current")
sysSwImageSlotId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageSlotId.setStatus("current")
sysSwImageFilename = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageFilename.setStatus("current")
sysSwImageProduct = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1, 3), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageProduct.setStatus("current")
sysSwImageVersion = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1, 4), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageVersion.setStatus("current")
sysSwImageBuild = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1, 5), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageBuild.setStatus("current")
sysSwImageChksum = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1, 6), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageChksum.setStatus("current")
sysSwImageVerified = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1, 7),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageVerified.setStatus("current")
sysSwImageBuildDate = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1, 8), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageBuildDate.setStatus("current")
sysSwImageLastModified = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1, 9), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageLastModified.setStatus("current")
sysSwImageFileSize = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 2, 2, 1, 10), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwImageFileSize.setStatus("current")
sysSwHotfixNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwHotfixNumber.setStatus("current")
sysSwHotfixTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2),
)
if mibBuilder.loadTexts:
    sysSwHotfixTable.setStatus("current")
sysSwHotfixEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSwHotfixSlotId"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSwHotfixFilename"),
)
if mibBuilder.loadTexts:
    sysSwHotfixEntry.setStatus("current")
sysSwHotfixSlotId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwHotfixSlotId.setStatus("current")
sysSwHotfixFilename = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwHotfixFilename.setStatus("current")
sysSwHotfixProduct = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2, 1, 3), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwHotfixProduct.setStatus("current")
sysSwHotfixVersion = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2, 1, 4), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwHotfixVersion.setStatus("current")
sysSwHotfixBuild = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2, 1, 5), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwHotfixBuild.setStatus("current")
sysSwHotfixChksum = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2, 1, 6), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwHotfixChksum.setStatus("current")
sysSwHotfixVerified = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2, 1, 7),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwHotfixVerified.setStatus("current")
sysSwHotfixHotfixId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2, 1, 8), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwHotfixHotfixId.setStatus("current")
sysSwHotfixHotfixTitle = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 3, 2, 1, 9), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwHotfixHotfixTitle.setStatus("current")
sysSwStatusNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 4, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwStatusNumber.setStatus("current")
sysSwStatusTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 4, 2),
)
if mibBuilder.loadTexts:
    sysSwStatusTable.setStatus("current")
sysSwStatusEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 4, 2, 1),
).setIndexNames(
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSwStatusSlotId"),
    (0, "F5-BIGIP-SYSTEM-MIB", "sysSwStatusVolume"),
)
if mibBuilder.loadTexts:
    sysSwStatusEntry.setStatus("current")
sysSwStatusSlotId = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 4, 2, 1, 1),
    Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwStatusSlotId.setStatus("current")
sysSwStatusVolume = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 4, 2, 1, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwStatusVolume.setStatus("current")
sysSwStatusProduct = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 4, 2, 1, 3), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwStatusProduct.setStatus("current")
sysSwStatusVersion = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 4, 2, 1, 4), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwStatusVersion.setStatus("current")
sysSwStatusBuild = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 4, 2, 1, 5), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwStatusBuild.setStatus("current")
sysSwStatusActive = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 9, 4, 2, 1, 6),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(0, 1))
    .clone(namedValues=NamedValues(("false", 0), ("true", 1))),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysSwStatusActive.setStatus("current")
sysGlobalHostResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysGlobalHostResetStats.setStatus("current")
sysGlobalHostMemTotal = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostMemTotal.setStatus("current")
sysGlobalHostMemUsed = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostMemUsed.setStatus("current")
sysGlobalHostCpuCount = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuCount.setStatus("current")
sysGlobalHostActiveCpuCount = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostActiveCpuCount.setStatus("current")
sysGlobalHostCpuUser = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuUser.setStatus("current")
sysGlobalHostCpuNice = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuNice.setStatus("current")
sysGlobalHostCpuSystem = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuSystem.setStatus("current")
sysGlobalHostCpuIdle = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIdle.setStatus("current")
sysGlobalHostCpuIrq = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIrq.setStatus("current")
sysGlobalHostCpuSoftirq = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuSoftirq.setStatus("current")
sysGlobalHostCpuIowait = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIowait.setStatus("current")
sysGlobalHostCpuUsageRatio = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 13), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuUsageRatio.setStatus("current")
sysGlobalHostCpuUser5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuUser5s.setStatus("current")
sysGlobalHostCpuNice5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuNice5s.setStatus("current")
sysGlobalHostCpuSystem5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuSystem5s.setStatus("current")
sysGlobalHostCpuIdle5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIdle5s.setStatus("current")
sysGlobalHostCpuIrq5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIrq5s.setStatus("current")
sysGlobalHostCpuSoftirq5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 19), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuSoftirq5s.setStatus("current")
sysGlobalHostCpuIowait5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 20), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIowait5s.setStatus("current")
sysGlobalHostCpuUsageRatio5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 21), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuUsageRatio5s.setStatus("current")
sysGlobalHostCpuUser1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 22), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuUser1m.setStatus("current")
sysGlobalHostCpuNice1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 23), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuNice1m.setStatus("current")
sysGlobalHostCpuSystem1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 24), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuSystem1m.setStatus("current")
sysGlobalHostCpuIdle1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 25), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIdle1m.setStatus("current")
sysGlobalHostCpuIrq1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 26), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIrq1m.setStatus("current")
sysGlobalHostCpuSoftirq1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 27), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuSoftirq1m.setStatus("current")
sysGlobalHostCpuIowait1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 28), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIowait1m.setStatus("current")
sysGlobalHostCpuUsageRatio1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 29), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuUsageRatio1m.setStatus("current")
sysGlobalHostCpuUser5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 30), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuUser5m.setStatus("current")
sysGlobalHostCpuNice5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 31), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuNice5m.setStatus("current")
sysGlobalHostCpuSystem5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 32), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuSystem5m.setStatus("current")
sysGlobalHostCpuIdle5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 33), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIdle5m.setStatus("current")
sysGlobalHostCpuIrq5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 34), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIrq5m.setStatus("current")
sysGlobalHostCpuSoftirq5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 35), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuSoftirq5m.setStatus("current")
sysGlobalHostCpuIowait5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 36), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuIowait5m.setStatus("current")
sysGlobalHostCpuUsageRatio5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 37), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuUsageRatio5m.setStatus("current")
sysGlobalHostCpuStolen = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 38), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuStolen.setStatus("current")
sysGlobalHostCpuStolen5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 39), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuStolen5s.setStatus("current")
sysGlobalHostCpuStolen1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 40), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuStolen1m.setStatus("current")
sysGlobalHostCpuStolen5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 20, 41), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalHostCpuStolen5m.setStatus("current")
sysModuleAllocationNumber = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 11, 1, 1), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysModuleAllocationNumber.setStatus("current")
sysModuleAllocationTable = MibTable(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 11, 1, 2),
)
if mibBuilder.loadTexts:
    sysModuleAllocationTable.setStatus("current")
sysModuleAllocationEntry = MibTableRow(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 11, 1, 2, 1),
).setIndexNames((0, "F5-BIGIP-SYSTEM-MIB", "sysModuleAllocationName"))
if mibBuilder.loadTexts:
    sysModuleAllocationEntry.setStatus("current")
sysModuleAllocationName = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 11, 1, 2, 1, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysModuleAllocationName.setStatus("current")
sysModuleAllocationProvisionLevel = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 11, 1, 2, 1, 2),
    Integer32()
    .subtype(subtypeSpec=SingleValueConstraint(1, 2, 3, 4, 5))
    .clone(
        namedValues=NamedValues(
            ("none", 1), ("minimum", 2), ("nominal", 3), ("dedicated", 4), ("custom", 5)
        )
    ),
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysModuleAllocationProvisionLevel.setStatus("current")
sysModuleAllocationMemoryRatio = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 11, 1, 2, 1, 3), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysModuleAllocationMemoryRatio.setStatus("current")
sysModuleAllocationCpuRatio = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 11, 1, 2, 1, 4), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysModuleAllocationCpuRatio.setStatus("current")
sysModuleAllocationDiskRatio = MibTableColumn(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 11, 1, 2, 1, 5), Integer32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysModuleAllocationDiskRatio.setStatus("current")
sysGlobalTmmStatResetStats = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 1), Integer32()
).setMaxAccess("readwrite")
if mibBuilder.loadTexts:
    sysGlobalTmmStatResetStats.setStatus("current")
sysGlobalTmmStatNpus = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 2), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatNpus.setStatus("current")
sysGlobalTmmStatClientPktsIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 3), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatClientPktsIn.setStatus("current")
sysGlobalTmmStatClientBytesIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 4), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatClientBytesIn.setStatus("current")
sysGlobalTmmStatClientPktsOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 5), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatClientPktsOut.setStatus("current")
sysGlobalTmmStatClientBytesOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 6), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatClientBytesOut.setStatus("current")
sysGlobalTmmStatClientMaxConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 7), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatClientMaxConns.setStatus("current")
sysGlobalTmmStatClientTotConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 8), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatClientTotConns.setStatus("current")
sysGlobalTmmStatClientCurConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 9), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatClientCurConns.setStatus("current")
sysGlobalTmmStatServerPktsIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 10), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatServerPktsIn.setStatus("current")
sysGlobalTmmStatServerBytesIn = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 11), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatServerBytesIn.setStatus("current")
sysGlobalTmmStatServerPktsOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 12), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatServerPktsOut.setStatus("current")
sysGlobalTmmStatServerBytesOut = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 13), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatServerBytesOut.setStatus("current")
sysGlobalTmmStatServerMaxConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 14), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatServerMaxConns.setStatus("current")
sysGlobalTmmStatServerTotConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 15), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatServerTotConns.setStatus("current")
sysGlobalTmmStatServerCurConns = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 16), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatServerCurConns.setStatus("current")
sysGlobalTmmStatMaintenanceModeDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 17), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatMaintenanceModeDeny.setStatus("current")
sysGlobalTmmStatMaxConnVirtualAddrDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 18), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatMaxConnVirtualAddrDeny.setStatus("current")
sysGlobalTmmStatMaxConnVirtualPathDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 19), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatMaxConnVirtualPathDeny.setStatus("current")
sysGlobalTmmStatVirtualServerNonSynDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 20), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatVirtualServerNonSynDeny.setStatus("current")
sysGlobalTmmStatNoHandlerDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 21), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatNoHandlerDeny.setStatus("current")
sysGlobalTmmStatLicenseDeny = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 22), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatLicenseDeny.setStatus("current")
sysGlobalTmmStatCmpConnRedirected = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 23), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatCmpConnRedirected.setStatus("current")
sysGlobalTmmStatConnectionMemoryErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 24), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatConnectionMemoryErrors.setStatus("current")
sysGlobalTmmStatTmTotalCycles = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 25), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatTmTotalCycles.setStatus("deprecated")
sysGlobalTmmStatTmIdleCycles = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 26), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatTmIdleCycles.setStatus("deprecated")
sysGlobalTmmStatTmSleepCycles = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 27), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatTmSleepCycles.setStatus("deprecated")
sysGlobalTmmStatMemoryTotal = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 28), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatMemoryTotal.setStatus("current")
sysGlobalTmmStatMemoryUsed = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 29), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatMemoryUsed.setStatus("current")
sysGlobalTmmStatDroppedPackets = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 30), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatDroppedPackets.setStatus("current")
sysGlobalTmmStatIncomingPacketErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 31), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatIncomingPacketErrors.setStatus("current")
sysGlobalTmmStatOutgoingPacketErrors = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 32), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatOutgoingPacketErrors.setStatus("current")
sysGlobalTmmStatHttpRequests = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 33), Counter64()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatHttpRequests.setStatus("current")
sysGlobalTmmStatTmUsageRatio5s = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 34), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatTmUsageRatio5s.setStatus("current")
sysGlobalTmmStatTmUsageRatio1m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 35), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatTmUsageRatio1m.setStatus("current")
sysGlobalTmmStatTmUsageRatio5m = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 1, 2, 21, 36), Gauge32()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysGlobalTmmStatTmUsageRatio5m.setStatus("current")
sysPlatformInfoName = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 5, 1), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPlatformInfoName.setStatus("current")
sysPlatformInfoMarketingName = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 1, 3, 5, 2), LongDisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    sysPlatformInfoMarketingName.setStatus("current")
bigipSystemCompliance = ModuleCompliance(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 1, 1)
).setObjects(("F5-BIGIP-SYSTEM-MIB", "bigipSystemGroups"))

if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    bigipSystemCompliance = bigipSystemCompliance.setStatus("current")
bigipSystemGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1))
sysAttrGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 1)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrArpMaxEntries"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrArpAddReciprocal"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrArpTimeout"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrArpRetries"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrBootQuiet"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrConfigsyncState"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrConnAdaptiveReaperHiwat"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrConnAdaptiveReaperLowat"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrConnAutoLasthop"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverActiveMode"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverForceActive"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverForceStandby"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverIsRedundant"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverMemoryRestartPercent"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverNetwork"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverStandbyLinkDownTime"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverSslhardware"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverSslhardwareAction"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverUnitMask"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrFailoverUnitId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrModeMaint"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrPacketFilter"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrPacketFilterAllowImportantIcmp"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrPacketFilterEstablished"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrPacketFilterDefaultAction"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrPacketFilterSendIcmpErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrPvaAcceleration"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrVlanFDBTimeout"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAttrWatchdogState"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysAttrGroup = sysAttrGroup.setStatus("current")
sysStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 2)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientTotConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerTotConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientTotConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerTotConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatTotPvaAssistConn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatCurrPvaAssistConn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatMaintenanceModeDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatMaxConnVirtualPathDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatVirtualServerNonSynDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatNoHandlerDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatLicenseDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatConnectionMemoryErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatCpuCount"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatActiveCpuCount"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatMultiProcessorMode"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatTmTotalCycles"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatTmIdleCycles"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatTmSleepCycles"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatMemoryTotal"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatMemoryUsed"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatDroppedPackets"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatIncomingPacketErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatOutgoingPacketErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatAuthTotSessions"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatAuthCurSessions"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatAuthMaxSessions"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatAuthSuccessResults"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatAuthFailureResults"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatAuthWantcredentialResults"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatAuthErrorResults"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatHttpRequests"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatHardSyncookieGen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatHardSyncookieDet"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientPktsIn5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientBytesIn5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientPktsOut5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientBytesOut5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientMaxConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientTotConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientCurConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerPktsIn5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerBytesIn5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerPktsOut5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerBytesOut5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerMaxConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerTotConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerCurConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientPktsIn1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientBytesIn1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientPktsOut1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientBytesOut1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientMaxConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientTotConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientCurConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerPktsIn1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerBytesIn1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerPktsOut1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerBytesOut1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerMaxConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerTotConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerCurConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientPktsIn5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientBytesIn5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientPktsOut5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientBytesOut5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientMaxConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientTotConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatClientCurConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerPktsIn5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerBytesIn5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerPktsOut5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerBytesOut5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerMaxConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerTotConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatServerCurConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientPktsIn5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientBytesIn5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientPktsOut5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientBytesOut5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientMaxConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientTotConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientCurConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerPktsIn5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerBytesIn5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerPktsOut5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerBytesOut5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerMaxConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerTotConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerCurConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientPktsIn1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientBytesIn1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientPktsOut1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientBytesOut1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientMaxConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientTotConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientCurConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerPktsIn1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerBytesIn1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerPktsOut1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerBytesOut1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerMaxConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerTotConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerCurConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientPktsIn5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientBytesIn5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientPktsOut5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientBytesOut5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientMaxConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientTotConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaClientCurConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerPktsIn5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerBytesIn5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerPktsOut5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerBytesOut5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerMaxConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerTotConns5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStatPvaServerCurConns5m"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysStatGroup = sysStatGroup.setStatus("current")
sysAuthStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 3)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysAuthStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAuthStatTotSessions"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAuthStatCurSessions"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAuthStatMaxSessions"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAuthStatSuccessResults"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAuthStatFailureResults"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAuthStatWantcredentialResults"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAuthStatErrorResults"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysAuthStatGroup = sysAuthStatGroup.setStatus("current")
sysConnPoolStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 4)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysConnPoolStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysConnPoolStatCurSize"),
    ("F5-BIGIP-SYSTEM-MIB", "sysConnPoolStatMaxSize"),
    ("F5-BIGIP-SYSTEM-MIB", "sysConnPoolStatReuses"),
    ("F5-BIGIP-SYSTEM-MIB", "sysConnPoolStatConnects"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysConnPoolStatGroup = sysConnPoolStatGroup.setStatus("current")
sysHttpStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 5)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatCookiePersistInserts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatResp2xxCnt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatResp3xxCnt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatResp4xxCnt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatResp5xxCnt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatNumberReqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatGetReqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatPostReqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatV9Reqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatV10Reqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatV11Reqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatV9Resp"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatV10Resp"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatV11Resp"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatMaxKeepaliveReq"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRespBucket1k"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRespBucket4k"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRespBucket16k"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRespBucket32k"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatNullCompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatHtmlPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatHtmlPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatCssPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatCssPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatJsPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatJsPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatXmlPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatXmlPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatSgmlPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatSgmlPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatPlainPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatPlainPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatOctetPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatOctetPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatImagePrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatImagePostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatVideoPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatVideoPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatAudioPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatAudioPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatOtherPrecompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatOtherPostcompressBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRamcacheHits"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRamcacheMisses"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRamcacheMissesAll"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRamcacheHitBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRamcacheMissBytes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRamcacheMissBytesAll"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRamcacheSize"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRamcacheCount"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRamcacheEvictions"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHttpStatRespBucket64k"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysHttpStatGroup = sysHttpStatGroup.setStatus("current")
sysIcmpStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 6)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatTx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatRx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatForward"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatDrop"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatErrCksum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatErrLen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatErrMem"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatErrRtx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatErrProto"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatErrOpt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmpStatErr"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysIcmpStatGroup = sysIcmpStatGroup.setStatus("current")
sysIcmp6StatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 7)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatTx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatRx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatForward"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatDrop"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatErrCksum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatErrLen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatErrMem"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatErrRtx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatErrProto"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatErrOpt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIcmp6StatErr"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysIcmp6StatGroup = sysIcmp6StatGroup.setStatus("current")
sysIpStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 8)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatTx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatRx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatDropped"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatRxFrag"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatRxFragDropped"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatTxFrag"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatTxFragDropped"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatReassembled"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatErrCksum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatErrLen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatErrMem"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatErrRtx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatErrProto"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatErrOpt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIpStatErrReassembledTooLong"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysIpStatGroup = sysIpStatGroup.setStatus("current")
sysIp6StatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 9)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatTx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatRx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatDropped"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatRxFrag"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatRxFragDropped"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatTxFrag"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatTxFragDropped"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatReassembled"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatErrCksum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatErrLen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatErrMem"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatErrRtx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatErrProto"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatErrOpt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIp6StatErrReassembledTooLong"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysIp6StatGroup = sysIp6StatGroup.setStatus("current")
sysClientsslStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 10)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatCurNativeConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatMaxNativeConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatTotNativeConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatCurCompatConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatMaxCompatConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatTotCompatConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatEncryptedBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatEncryptedBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatDecryptedBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatDecryptedBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatRecordsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatRecordsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatFullyHwAcceleratedConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatPartiallyHwAcceleratedConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatNonHwAcceleratedConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatPrematureDisconnects"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatMidstreamRenegotiations"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatSessCacheCurEntries"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatSessCacheHits"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatSessCacheLookups"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatSessCacheOverflows"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatSessCacheInvalidations"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatPeercertValid"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatPeercertInvalid"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatPeercertNone"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatHandshakeFailures"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatBadRecords"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatFatalAlerts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatSslv2"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatSslv3"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatTlsv1"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatAdhKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatDhDssKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatDhRsaKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatDssKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatEdhDssKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatRsaKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatNullBulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatAesBulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatDesBulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatIdeaBulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatRc2Bulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatRc4Bulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatNullDigest"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatMd5Digest"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatShaDigest"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatNotssl"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatEdhRsaKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatTotConns5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatTotConns1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClientsslStatTotConns5m"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysClientsslStatGroup = sysClientsslStatGroup.setStatus("current")
sysServersslStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 11)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatCurNativeConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatMaxNativeConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatTotNativeConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatCurCompatConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatMaxCompatConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatTotCompatConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatEncryptedBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatEncryptedBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatDecryptedBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatDecryptedBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatRecordsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatRecordsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatFullyHwAcceleratedConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatPartiallyHwAcceleratedConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatNonHwAcceleratedConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatPrematureDisconnects"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatMidstreamRenegotiations"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatSessCacheCurEntries"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatSessCacheHits"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatSessCacheLookups"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatSessCacheOverflows"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatSessCacheInvalidations"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatPeercertValid"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatPeercertInvalid"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatPeercertNone"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatHandshakeFailures"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatBadRecords"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatFatalAlerts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatSslv2"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatSslv3"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatTlsv1"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatAdhKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatDhDssKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatDhRsaKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatDssKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatEdhDssKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatRsaKeyxchg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatNullBulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatAesBulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatDesBulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatIdeaBulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatRc2Bulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatRc4Bulk"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatNullDigest"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatMd5Digest"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatShaDigest"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatNotssl"),
    ("F5-BIGIP-SYSTEM-MIB", "sysServersslStatEdhRsaKeyxchg"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysServersslStatGroup = sysServersslStatGroup.setStatus("current")
sysStreamStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 12)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysStreamStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStreamStatReplaces"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysStreamStatGroup = sysStreamStatGroup.setStatus("current")
sysTcpStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 13)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatOpen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatCloseWait"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatFinWait"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatTimeWait"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatAccepts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatAcceptfails"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatConnects"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatConnfails"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatExpires"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatAbandons"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatRxrst"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatRxbadsum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatRxbadseg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatRxooseg"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatRxcookie"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatRxbadcookie"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatSyncacheover"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTcpStatTxrexmits"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysTcpStatGroup = sysTcpStatGroup.setStatus("current")
sysUdpStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 14)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatOpen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatAccepts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatAcceptfails"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatConnects"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatConnfails"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatExpires"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatRxdgram"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatRxbaddgram"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatRxunreach"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatRxbadsum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatRxnosum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysUdpStatTxdgram"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysUdpStatGroup = sysUdpStatGroup.setStatus("current")
sysAdminIpGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 15)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysAdminIpNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAdminIpAddrType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAdminIpAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAdminIpNetmaskType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysAdminIpNetmask"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysAdminIpGroup = sysAdminIpGroup.setStatus("current")
sysArpStaticEntryGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 16)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysArpStaticEntryNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysArpStaticEntryIpAddrType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysArpStaticEntryIpAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysArpStaticEntryMacAddr"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysArpStaticEntryGroup = sysArpStaticEntryGroup.setStatus("current")
sysDot1dbaseStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 17)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatMacAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatNumPorts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatType"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysDot1dbaseStatGroup = sysDot1dbaseStatGroup.setStatus("current")
sysDot1dbaseStatPortGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 18)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatPortNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatPortIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatPortPort"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatPortName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatPortDelayExceededDiscards"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot1dbaseStatPortMtuExceededDiscards"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysDot1dbaseStatPortGroup = sysDot1dbaseStatPortGroup.setStatus("current")
sysInterfaceGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 19)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceMediaMaxSpeed"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceMediaMaxDuplex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceMediaActiveSpeed"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceMediaActiveDuplex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceMacAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceMtu"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceEnabled"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceLearnMode"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceFlowCtrlReq"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStpLink"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStpEdge"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStpEdgeActive"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStpAuto"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStpEnable"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStpReset"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatus"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceComboPort"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfacePreferSfp"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceSfpMedia"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfacePhyMaster"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysInterfaceGroup = sysInterfaceGroup.setStatus("current")
sysIntfMediaGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 20)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysIntfMediaNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIntfMediaName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIntfMediaIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIntfMediaMediaOption"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysIntfMediaGroup = sysIntfMediaGroup.setStatus("current")
sysIfGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 21)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysIfNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfName"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysIfGroup = sysIfGroup.setStatus("current")
sysInterfaceStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 22)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatMcastIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatMcastOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatErrorsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatErrorsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatDropsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatDropsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatCollisions"),
    ("F5-BIGIP-SYSTEM-MIB", "sysInterfaceStatPauseActive"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysInterfaceStatGroup = sysInterfaceStatGroup.setStatus("current")
sysIfxStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 23)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatInMulticastPkts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatInBroadcastPkts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatOutMulticastPkts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatOutBroadcastPkts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatHcInOctets"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatHcInUcastPkts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatHcInMulticastPkts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatHcInBroadcastPkts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatHcOutOctets"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatHcOutUcastPkts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatHcOutMulticastPkts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatHcOutBroadcastPkts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatHighSpeed"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatConnectorPresent"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatCounterDiscontinuityTime"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIfxStatAlias"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysIfxStatGroup = sysIfxStatGroup.setStatus("current")
sysL2ForwardGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 24)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardVlanName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardMacAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardIfname"),
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardIftype"),
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardDynamic"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysL2ForwardGroup = sysL2ForwardGroup.setStatus("current")
sysPacketFilterGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 25)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterRname"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterOrder"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterAction"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterVname"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterLog"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterRclass"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterExpression"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysPacketFilterGroup = sysPacketFilterGroup.setStatus("current")
sysPacketFilterAddrGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 26)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterAddrNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterAddrIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterAddrIpType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterAddrIp"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysPacketFilterAddrGroup = sysPacketFilterAddrGroup.setStatus("current")
sysPacketFilterVlanGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 27)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterVlanNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterVlanIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterVlanName"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysPacketFilterVlanGroup = sysPacketFilterVlanGroup.setStatus("current")
sysPacketFilterMacGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 28)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterMacNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterMacIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterMacAddr"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysPacketFilterMacGroup = sysPacketFilterMacGroup.setStatus("current")
sysPacketFilterStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 29)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterStatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterStatRname"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPacketFilterStatHits"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysPacketFilterStatGroup = sysPacketFilterStatGroup.setStatus("current")
sysRouteMgmtEntryGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 30)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryDestType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryDest"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryNetmaskType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryNetmask"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryGatewayType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryGateway"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteMgmtEntryMtu"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysRouteMgmtEntryGroup = sysRouteMgmtEntryGroup.setStatus("current")
sysRouteStaticEntryGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 31)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryDestType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryDest"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryNetmaskType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryNetmask"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryVlanName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryGatewayType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryGateway"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryPoolName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRouteStaticEntryMtu"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysRouteStaticEntryGroup = sysRouteStaticEntryGroup.setStatus("current")
sysSelfIpGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 32)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfIpNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfIpAddrType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfIpAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfIpNetmaskType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfIpNetmask"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfIpUnitId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfIpIsFloating"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfIpVlanName"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysSelfIpGroup = sysSelfIpGroup.setStatus("current")
sysSelfPortGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 33)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfPortNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfPortAddrType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfPortAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfPortProtocol"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfPortPort"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysSelfPortGroup = sysSelfPortGroup.setStatus("current")
sysStpGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 34)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysStpNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInstanceId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpPriority"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpRootAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpRegionalRootAddr"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysStpGroup = sysStpGroup.setStatus("current")
sysStpGlobalsGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 35)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysStpGlobalsMode"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpGlobalsFwdDelay"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpGlobalsHelloTime"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpGlobalsMaxAge"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpGlobalsTransmitHold"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpGlobalsMaxHops"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpGlobalsIdentifier"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpGlobalsRevision"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysStpGlobalsGroup = sysStpGlobalsGroup.setStatus("current")
sysStpInterfaceMbrGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 36)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrInstanceId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrStateActive"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrRole"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrPriority"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrPathCost"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceMbrStateRequested"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysStpInterfaceMbrGroup = sysStpInterfaceMbrGroup.setStatus("current")
sysStpVlanMbrGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 37)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysStpVlanMbrNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpVlanMbrInstanceId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpVlanMbrVlanVname"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysStpVlanMbrGroup = sysStpVlanMbrGroup.setStatus("current")
sysStpBridgeStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 38)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatMode"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatFwdDelay"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatHelloTime"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatMaxAge"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatBridgeFwdDelay"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatBridgeHelloTime"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatBridgeMaxAge"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatTransmitHold"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatPathCost"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatRootPrio"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeStatRootAddr"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysStpBridgeStatGroup = sysStpBridgeStatGroup.setStatus("current")
sysStpBridgeTreeStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 39)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatInstanceId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatPriority"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatLastTc"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatTcCount"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatDesigRootPrio"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatDesigRootAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatInternalPathCost"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatRootPort"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpBridgeTreeStatRootPortNum"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysStpBridgeTreeStatGroup = sysStpBridgeTreeStatGroup.setStatus("current")
sysStpInterfaceStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 40)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceStatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceStatName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceStatPortNum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceStatStpEnable"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceStatPathCost"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceStatRootCost"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceStatRootPrio"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceStatRootAddr"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysStpInterfaceStatGroup = sysStpInterfaceStatGroup.setStatus("current")
sysStpInterfaceTreeStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 41)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatInstanceId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatPriority"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatState"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatStatRole"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatDesigRootPrio"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatDesigRootAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatDesigCost"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatDesigBridgePrio"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatDesigBridgeAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatDesigPortNum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatDesigPortPriority"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatInternalPathCost"),
    ("F5-BIGIP-SYSTEM-MIB", "sysStpInterfaceTreeStatFwdTransitions"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysStpInterfaceTreeStatGroup = sysStpInterfaceTreeStatGroup.setStatus("current")
sysDot3StatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 42)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatAlignmentErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatFcsErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatSingleCollisionFrames"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatMultiCollisionFrames"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatSqetestErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatDeferredTx"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatLateCollisions"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatExcessiveCollisions"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatIntmacTxErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatCarrierSenseErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatFrameTooLongs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatIntmacRxErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatSymbolErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatDuplexStatus"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatCollisionCount"),
    ("F5-BIGIP-SYSTEM-MIB", "sysDot3StatCollisionFreq"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysDot3StatGroup = sysDot3StatGroup.setStatus("current")
sysTrunkGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 43)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatus"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkAggAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkCfgMbrCount"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkOperBw"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStpEnable"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStpReset"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkLacpEnabled"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkActiveLacp"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkShortTimeout"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysTrunkGroup = sysTrunkGroup.setStatus("current")
sysTrunkStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 44)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatMcastIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatMcastOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatErrorsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatErrorsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatDropsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatDropsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkStatCollisions"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysTrunkStatGroup = sysTrunkStatGroup.setStatus("current")
sysTrunkCfgMemberGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 45)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkCfgMemberNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkCfgMemberTrunkName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTrunkCfgMemberName"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysTrunkCfgMemberGroup = sysTrunkCfgMemberGroup.setStatus("current")
sysVlanDataGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 46)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanVname"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanSpanningTree"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanMacMasquerade"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanMacTrue"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanSourceCheck"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanFailsafeEnabled"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanMtu"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanFailsafeTimeout"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanFailsafeAction"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanMirrorHashPortEnable"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanLearnMode"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysVlanDataGroup = sysVlanDataGroup.setStatus("current")
sysVlanMemberGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 47)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanMemberNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanMemberVmname"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanMemberParentVname"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanMemberTagged"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanMemberType"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysVlanMemberGroup = sysVlanMemberGroup.setStatus("current")
sysVlanGroupGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 48)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupVlanId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupMode"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupBridgeAllTraffic"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupBridgeInStandby"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupBridgeMulticast"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupMacMasquerade"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupMacTrue"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysVlanGroupGroup = sysVlanGroupGroup.setStatus("current")
sysVlanGroupMbrGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 49)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupMbrNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupMbrGroupName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysVlanGroupMbrVlanName"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysVlanGroupMbrGroup = sysVlanGroupMbrGroup.setStatus("current")
sysProxyExclusionGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 50)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysProxyExclusionNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysProxyExclusionVlangroupName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysProxyExclusionIpType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysProxyExclusionIp"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysProxyExclusionGroup = sysProxyExclusionGroup.setStatus("current")
sysCpuGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 51)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysCpuNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysCpuIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysCpuTemperature"),
    ("F5-BIGIP-SYSTEM-MIB", "sysCpuFanSpeed"),
    ("F5-BIGIP-SYSTEM-MIB", "sysCpuName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysCpuSlot"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysCpuGroup = sysCpuGroup.setStatus("current")
sysChassisFanGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 52)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysChassisFanNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysChassisFanIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysChassisFanStatus"),
    ("F5-BIGIP-SYSTEM-MIB", "sysChassisFanSpeed"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysChassisFanGroup = sysChassisFanGroup.setStatus("current")
sysChassisPowerSupplyGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 53)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysChassisPowerSupplyNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysChassisPowerSupplyIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysChassisPowerSupplyStatus"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysChassisPowerSupplyGroup = sysChassisPowerSupplyGroup.setStatus("current")
sysChassisTempGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 54)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysChassisTempNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysChassisTempIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysChassisTempTemperature"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysChassisTempGroup = sysChassisTempGroup.setStatus("current")
sysProductGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 55)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysProductName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysProductVersion"),
    ("F5-BIGIP-SYSTEM-MIB", "sysProductBuild"),
    ("F5-BIGIP-SYSTEM-MIB", "sysProductEdition"),
    ("F5-BIGIP-SYSTEM-MIB", "sysProductDate"),
    ("F5-BIGIP-SYSTEM-MIB", "sysProductHotfix"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysProductGroup = sysProductGroup.setStatus("current")
sysSubMemoryGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 56)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysSubMemoryResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSubMemoryNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSubMemoryName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSubMemoryAllocated"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSubMemoryMaxAllocated"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSubMemorySize"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysSubMemoryGroup = sysSubMemoryGroup.setStatus("current")
sysSystemGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 57)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysSystemName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSystemNodeName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSystemRelease"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSystemVersion"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSystemMachine"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSystemUptime"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysSystemGroup = sysSystemGroup.setStatus("current")
sysFastHttpStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 58)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatClientSyns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatClientAccepts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatServerConnects"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatConnpoolCurSize"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatConnpoolMaxSize"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatConnpoolReuses"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatConnpoolExhausted"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatNumberReqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatUnbufferedReqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatGetReqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatPostReqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatV9Reqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatV10Reqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatV11Reqs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatResp2xxCnt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatResp3xxCnt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatResp4xxCnt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatResp5xxCnt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatReqParseErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatRespParseErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatClientRxBad"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatServerRxBad"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastHttpStatPipelinedReqs"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysFastHttpStatGroup = sysFastHttpStatGroup.setStatus("current")
sysXmlStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 59)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysXmlStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysXmlStatNumErrors"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysXmlStatGroup = sysXmlStatGroup.setStatus("current")
sysGeneralGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 60)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysGeneralHwName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGeneralHwNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGeneralChassisSerialNum"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysGeneralGroup = sysGeneralGroup.setStatus("current")
sysIiopStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 61)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysIiopStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIiopStatNumRequests"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIiopStatNumResponses"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIiopStatNumCancels"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIiopStatNumErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIiopStatNumFragments"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysIiopStatGroup = sysIiopStatGroup.setStatus("current")
sysRtspStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 62)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysRtspStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRtspStatNumRequests"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRtspStatNumResponses"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRtspStatNumErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysRtspStatNumInterleavedData"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysRtspStatGroup = sysRtspStatGroup.setStatus("current")
sysSctpStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 63)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatAccepts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatAcceptfails"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatConnects"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatConnfails"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatExpires"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatAbandons"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatRxrst"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatRxbadsum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatRxcookie"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSctpStatRxbadcookie"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysSctpStatGroup = sysSctpStatGroup.setStatus("current")
sysL2ForwardStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 64)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardStatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardStatVlanName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardStatMacAddr"),
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardStatIfname"),
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardStatIftype"),
    ("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardStatDynamic"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysL2ForwardStatGroup = sysL2ForwardStatGroup.setStatus("current")
sysL2ForwardAttrGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 65)
).setObjects(("F5-BIGIP-SYSTEM-MIB", "sysL2ForwardAttrVlan"))
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysL2ForwardAttrGroup = sysL2ForwardAttrGroup.setStatus("current")
sysHostMemoryGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 66)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysHostMemoryTotal"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostMemoryUsed"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysHostMemoryGroup = sysHostMemoryGroup.setStatus("current")
sysHostCpuGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 67)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysHostCpuNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostCpuIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostCpuId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostCpuUser"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostCpuNice"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostCpuSystem"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostCpuIdle"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostCpuIrq"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostCpuSoftirq"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostCpuIowait"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysHostCpuGroup = sysHostCpuGroup.setStatus("current")
sysHostDiskGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 68)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysHostDiskNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostDiskPartition"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostDiskBlockSize"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostDiskTotalBlocks"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostDiskFreeBlocks"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostDiskTotalNodes"),
    ("F5-BIGIP-SYSTEM-MIB", "sysHostDiskFreeNodes"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysHostDiskGroup = sysHostDiskGroup.setStatus("current")
sysSelfPortDefGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 69)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfPortDefNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfPortDefProtocol"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSelfPortDefPort"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysSelfPortDefGroup = sysSelfPortDefGroup.setStatus("current")
sysIntfMediaSfpGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 70)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysIntfMediaSfpNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIntfMediaSfpName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIntfMediaSfpIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysIntfMediaSfpType"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysIntfMediaSfpGroup = sysIntfMediaSfpGroup.setStatus("current")
sysPvaStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 71)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatPvaId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatClientPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatClientBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatClientPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatClientBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatClientMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatClientTotConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatClientCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatServerPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatServerBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatServerPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatServerBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatServerMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatServerTotConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatServerCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatTotAssistConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatCurAssistConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatHardSyncookieGen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPvaStatHardSyncookieDet"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysPvaStatGroup = sysPvaStatGroup.setStatus("current")
sysTmmStatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 72)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatTmmId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatTmmPid"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatCpu"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatTmid"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatNpus"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatClientPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatClientBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatClientPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatClientBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatClientMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatClientTotConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatClientCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatServerPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatServerBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatServerPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatServerBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatServerMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatServerTotConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatServerCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatMaintenanceModeDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatMaxConnVirtualAddrDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatMaxConnVirtualPathDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatVirtualServerNonSynDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatNoHandlerDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatLicenseDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatCmpConnRedirected"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatConnectionMemoryErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatTmTotalCycles"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatTmIdleCycles"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatTmSleepCycles"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatMemoryTotal"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatMemoryUsed"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatDroppedPackets"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatIncomingPacketErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatOutgoingPacketErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatHttpRequests"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatTmUsageRatio5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatTmUsageRatio1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysTmmStatTmUsageRatio5m"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysTmmStatGroup = sysTmmStatGroup.setStatus("current")
sysMultiHostGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 73)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostHostId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostTotal"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostUsed"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostMode"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuCount"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostActiveCpuCount"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysMultiHostGroup = sysMultiHostGroup.setStatus("current")
sysMultiHostCpuGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 74)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuHostId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIndex"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuUser"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuNice"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuSystem"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIdle"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIrq"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuSoftirq"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIowait"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuUsageRatio"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuUser5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuNice5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuSystem5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIdle5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIrq5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuSoftirq5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIowait5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuUsageRatio5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuUser1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuNice1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuSystem1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIdle1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIrq1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuSoftirq1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIowait1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuUsageRatio1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuUser5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuNice5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuSystem5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIdle5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIrq5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuSoftirq5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuIowait5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuUsageRatio5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuStolen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuStolen5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuStolen1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysMultiHostCpuStolen5m"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysMultiHostCpuGroup = sysMultiHostCpuGroup.setStatus("current")
sysFastL4StatGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 75)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatOpen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatAccepts"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatAcceptfails"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatExpires"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatRxbadpkt"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatRxunreach"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatRxbadunreach"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatRxbadsum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatTxerrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatSyncookIssue"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatSyncookAccept"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatSyncookReject"),
    ("F5-BIGIP-SYSTEM-MIB", "sysFastL4StatServersynrtx"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysFastL4StatGroup = sysFastL4StatGroup.setStatus("current")
sysClusterGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 76)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterEnabled"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterFloatMgmtIpType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterFloatMgmtIp"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterFloatMgmtNetmaskType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterFloatMgmtNetmask"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMinUpMbrs"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMinUpMbrsEnable"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMinUpMbrsAction"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterAvailabilityState"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterEnabledStat"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterDisabledParentType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterStatusReason"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterHaState"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterPriSlotId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterLastPriSlotId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterPriSelTime"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysClusterGroup = sysClusterGroup.setStatus("current")
sysClusterMbrGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 77)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrCluster"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrSlotId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrAvailabilityState"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrEnabledStat"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrDisabledParentType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrStatusReason"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrLicensed"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrState"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrEnabled"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrPriming"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrMgmtAddrType"),
    ("F5-BIGIP-SYSTEM-MIB", "sysClusterMbrMgmtAddr"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysClusterMbrGroup = sysClusterMbrGroup.setStatus("current")
sysSwVolumeGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 78)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysSwVolumeNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwVolumeSlotId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwVolumeName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwVolumeSize"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwVolumeActive"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysSwVolumeGroup = sysSwVolumeGroup.setStatus("current")
sysSwImageGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 79)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageSlotId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageFilename"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageProduct"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageVersion"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageBuild"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageChksum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageVerified"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageBuildDate"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageLastModified"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwImageFileSize"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysSwImageGroup = sysSwImageGroup.setStatus("current")
sysSwHotfixGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 80)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysSwHotfixNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwHotfixSlotId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwHotfixFilename"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwHotfixProduct"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwHotfixVersion"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwHotfixBuild"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwHotfixChksum"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwHotfixVerified"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwHotfixHotfixId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwHotfixHotfixTitle"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysSwHotfixGroup = sysSwHotfixGroup.setStatus("current")
sysSwStatusGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 81)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysSwStatusNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwStatusSlotId"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwStatusVolume"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwStatusProduct"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwStatusVersion"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwStatusBuild"),
    ("F5-BIGIP-SYSTEM-MIB", "sysSwStatusActive"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysSwStatusGroup = sysSwStatusGroup.setStatus("current")
sysGlobalHostGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 82)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostMemTotal"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostMemUsed"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuCount"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostActiveCpuCount"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuUser"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuNice"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuSystem"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIdle"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIrq"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuSoftirq"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIowait"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuUsageRatio"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuUser5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuNice5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuSystem5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIdle5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIrq5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuSoftirq5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIowait5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuUsageRatio5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuUser1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuNice1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuSystem1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIdle1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIrq1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuSoftirq1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIowait1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuUsageRatio1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuUser5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuNice5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuSystem5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIdle5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIrq5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuSoftirq5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuIowait5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuUsageRatio5m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuStolen"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuStolen5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuStolen1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalHostCpuStolen5m"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysGlobalHostGroup = sysGlobalHostGroup.setStatus("current")
sysModuleAllocationGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 83)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysModuleAllocationNumber"),
    ("F5-BIGIP-SYSTEM-MIB", "sysModuleAllocationName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysModuleAllocationProvisionLevel"),
    ("F5-BIGIP-SYSTEM-MIB", "sysModuleAllocationMemoryRatio"),
    ("F5-BIGIP-SYSTEM-MIB", "sysModuleAllocationCpuRatio"),
    ("F5-BIGIP-SYSTEM-MIB", "sysModuleAllocationDiskRatio"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysModuleAllocationGroup = sysModuleAllocationGroup.setStatus("current")
sysGlobalTmmStatGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 84)
).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatResetStats"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatNpus"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatClientPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatClientBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatClientPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatClientBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatClientMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatClientTotConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatClientCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatServerPktsIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatServerBytesIn"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatServerPktsOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatServerBytesOut"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatServerMaxConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatServerTotConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatServerCurConns"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatMaintenanceModeDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatMaxConnVirtualAddrDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatMaxConnVirtualPathDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatVirtualServerNonSynDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatNoHandlerDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatLicenseDeny"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatCmpConnRedirected"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatConnectionMemoryErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatTmTotalCycles"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatTmIdleCycles"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatTmSleepCycles"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatMemoryTotal"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatMemoryUsed"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatDroppedPackets"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatIncomingPacketErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatOutgoingPacketErrors"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatHttpRequests"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatTmUsageRatio5s"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatTmUsageRatio1m"),
    ("F5-BIGIP-SYSTEM-MIB", "sysGlobalTmmStatTmUsageRatio5m"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysGlobalTmmStatGroup = sysGlobalTmmStatGroup.setStatus("current")
sysPlatformInfoGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 1, 85)).setObjects(
    ("F5-BIGIP-SYSTEM-MIB", "sysPlatformInfoName"),
    ("F5-BIGIP-SYSTEM-MIB", "sysPlatformInfoMarketingName"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    sysPlatformInfoGroup = sysPlatformInfoGroup.setStatus("current")
mibBuilder.exportSymbols(
    "F5-BIGIP-SYSTEM-MIB",
    sysChassisPowerSupplyNumber=sysChassisPowerSupplyNumber,
    sysIpStatErrRtx=sysIpStatErrRtx,
    sysStpBridgeStatHelloTime=sysStpBridgeStatHelloTime,
    sysHttpStatRamcacheHits=sysHttpStatRamcacheHits,
    sysHostCpuEntry=sysHostCpuEntry,
    sysVlanMemberGroup=sysVlanMemberGroup,
    sysTmmStatMemoryTotal=sysTmmStatMemoryTotal,
    sysSystemNodeName=sysSystemNodeName,
    sysPacketFilterOrder=sysPacketFilterOrder,
    sysIp6StatRx=sysIp6StatRx,
    sysDot1dbaseStatPortTable=sysDot1dbaseStatPortTable,
    bigipPb200=bigipPb200,
    sysL2ForwardTable=sysL2ForwardTable,
    sysVlanGroupVlanId=sysVlanGroupVlanId,
    sysServersslStatCurConns=sysServersslStatCurConns,
    sysPvaStatResetStats=sysPvaStatResetStats,
    sysMultiHostCpuIrq5s=sysMultiHostCpuIrq5s,
    sysStatPvaClientMaxConns5s=sysStatPvaClientMaxConns5s,
    sysGlobalHostCpuNice5s=sysGlobalHostCpuNice5s,
    sysInterfaceEntry=sysInterfaceEntry,
    sysServersslStatMd5Digest=sysServersslStatMd5Digest,
    sysServersslStatBadRecords=sysServersslStatBadRecords,
    sysAttrGroup=sysAttrGroup,
    sysFastL4StatOpen=sysFastL4StatOpen,
    sysIpStatResetStats=sysIpStatResetStats,
    sysAdminIpNumber=sysAdminIpNumber,
    sysGlobalHostResetStats=sysGlobalHostResetStats,
    sysServersslStatSessCacheOverflows=sysServersslStatSessCacheOverflows,
    sysDot1dbaseStatPortGroup=sysDot1dbaseStatPortGroup,
    sysVlans=sysVlans,
    sysVlanGroupMacMasquerade=sysVlanGroupMacMasquerade,
    sysPvaStatEntry=sysPvaStatEntry,
    sysStatPvaClientPktsOut5s=sysStatPvaClientPktsOut5s,
    sysAuthStatCurSessions=sysAuthStatCurSessions,
    sysStatClientBytesOut1m=sysStatClientBytesOut1m,
    sysVlanGroupBridgeAllTraffic=sysVlanGroupBridgeAllTraffic,
    sysStatPvaServerBytesIn=sysStatPvaServerBytesIn,
    sysSwVolumeName=sysSwVolumeName,
    sysPvaStatClientPktsIn=sysPvaStatClientPktsIn,
    sysClientsslStatAdhKeyxchg=sysClientsslStatAdhKeyxchg,
    sysMultiHostNumber=sysMultiHostNumber,
    sysProxyExclusionIpType=sysProxyExclusionIpType,
    sysInterfaceStatName=sysInterfaceStatName,
    sysXmlStatNumErrors=sysXmlStatNumErrors,
    sysDot3StatDuplexStatus=sysDot3StatDuplexStatus,
    sysGlobalTmmStatConnectionMemoryErrors=sysGlobalTmmStatConnectionMemoryErrors,
    sysClusterFloatMgmtIp=sysClusterFloatMgmtIp,
    sysClusterFloatMgmtNetmask=sysClusterFloatMgmtNetmask,
    sysHttpStatXmlPostcompressBytes=sysHttpStatXmlPostcompressBytes,
    sysStpBridgeStatTransmitHold=sysStpBridgeStatTransmitHold,
    sysTmmStatDroppedPackets=sysTmmStatDroppedPackets,
    sysGeneralGroup=sysGeneralGroup,
    sysFastHttpStatUnbufferedReqs=sysFastHttpStatUnbufferedReqs,
    sysAttrFailoverActiveMode=sysAttrFailoverActiveMode,
    sysIp6StatErrRtx=sysIp6StatErrRtx,
    sysStatPvaClientCurConns=sysStatPvaClientCurConns,
    sysSelfPortDefEntry=sysSelfPortDefEntry,
    bigip6900=bigip6900,
    sysClientsslStatRecordsIn=sysClientsslStatRecordsIn,
    sysConnPoolStatGroup=sysConnPoolStatGroup,
    firepass4300=firepass4300,
    sysStatAuthSuccessResults=sysStatAuthSuccessResults,
    sysIfxStatHcOutOctets=sysIfxStatHcOutOctets,
    sysSwStatusEntry=sysSwStatusEntry,
    sysInterface=sysInterface,
    sysGlobalTmmStatTmUsageRatio5m=sysGlobalTmmStatTmUsageRatio5m,
    sysSwImageTable=sysSwImageTable,
    sysMultiHostCpuIdle1m=sysMultiHostCpuIdle1m,
    sysClientsslStatPeercertValid=sysClientsslStatPeercertValid,
    sysTmmStatMemoryUsed=sysTmmStatMemoryUsed,
    sysHostCpuIowait=sysHostCpuIowait,
    sysIntfMediaSfpType=sysIntfMediaSfpType,
    sysInterfaceStatPauseActive=sysInterfaceStatPauseActive,
    sysClusterTable=sysClusterTable,
    sysInterfaceStpReset=sysInterfaceStpReset,
    sysIiopStatNumErrors=sysIiopStatNumErrors,
    sysClientsslStatPrematureDisconnects=sysClientsslStatPrematureDisconnects,
    sysTmmStatNpus=sysTmmStatNpus,
    sysIpStatErrMem=sysIpStatErrMem,
    sysPacketFilterVlanEntry=sysPacketFilterVlanEntry,
    sysSelfPortNumber=sysSelfPortNumber,
    sysHostCpuIrq=sysHostCpuIrq,
    sysClusterMbrEntry=sysClusterMbrEntry,
    sysSelfPortTable=sysSelfPortTable,
    sysInterfaceStat=sysInterfaceStat,
    sysMultiHostEntry=sysMultiHostEntry,
    bigip1500=bigip1500,
    sysInterfaceStatMcastOut=sysInterfaceStatMcastOut,
    sysTmmStatVirtualServerNonSynDeny=sysTmmStatVirtualServerNonSynDeny,
    sysStatServerPktsIn5s=sysStatServerPktsIn5s,
    sysClusterMbrState=sysClusterMbrState,
    sysTmmStatTmTotalCycles=sysTmmStatTmTotalCycles,
    sysHostCpuIdle=sysHostCpuIdle,
    sysStatClientPktsOut1m=sysStatClientPktsOut1m,
    sysTcpStatAbandons=sysTcpStatAbandons,
    sysMultiHostCpuIndex=sysMultiHostCpuIndex,
    sysClientsslStatRc4Bulk=sysClientsslStatRc4Bulk,
    sysPacketFilterStatResetStats=sysPacketFilterStatResetStats,
    arx4000=arx4000,
    sysClientsslStatAesBulk=sysClientsslStatAesBulk,
    sysStatServerTotConns5m=sysStatServerTotConns5m,
    sysRouteStaticEntryType=sysRouteStaticEntryType,
    sysClientsslStatEncryptedBytesIn=sysClientsslStatEncryptedBytesIn,
    sysTmmStatMaxConnVirtualPathDeny=sysTmmStatMaxConnVirtualPathDeny,
    sysStpEntry=sysStpEntry,
    sysServersslStatDhDssKeyxchg=sysServersslStatDhDssKeyxchg,
    sysTrunkCfgMemberTable=sysTrunkCfgMemberTable,
    sysStatServerPktsOut5s=sysStatServerPktsOut5s,
    sysAttrConnAdaptiveReaperLowat=sysAttrConnAdaptiveReaperLowat,
    sysL2ForwardStatEntry=sysL2ForwardStatEntry,
    sysStpVlanMbrEntry=sysStpVlanMbrEntry,
    sysMultiHostCpuIowait=sysMultiHostCpuIowait,
    sysSelfIpNetmask=sysSelfIpNetmask,
    sysIfxStatTable=sysIfxStatTable,
    sysTmmStatClientBytesIn=sysTmmStatClientBytesIn,
    sysIfxStatConnectorPresent=sysIfxStatConnectorPresent,
    sysHttpStatSgmlPrecompressBytes=sysHttpStatSgmlPrecompressBytes,
    sysClusterEnabled=sysClusterEnabled,
    sysStatClientMaxConns1m=sysStatClientMaxConns1m,
    sysSelfIpEntry=sysSelfIpEntry,
    sysStatClientTotConns1m=sysStatClientTotConns1m,
    sysUdpStatRxbadsum=sysUdpStatRxbadsum,
    sysGlobalHttpStat=sysGlobalHttpStat,
    bigip11050=bigip11050,
    sysPacketFilterVlanIndex=sysPacketFilterVlanIndex,
    sysStatAuthErrorResults=sysStatAuthErrorResults,
    sysTmmStatMaintenanceModeDeny=sysTmmStatMaintenanceModeDeny,
    sysServersslStatRc2Bulk=sysServersslStatRc2Bulk,
    sysIp6StatTx=sysIp6StatTx,
    sysSelfIpVlanName=sysSelfIpVlanName,
    sysRouteStaticEntryTable=sysRouteStaticEntryTable,
    sysTmmStatTmUsageRatio5m=sysTmmStatTmUsageRatio5m,
    sysGlobalTmmStatClientTotConns=sysGlobalTmmStatClientTotConns,
    sysPvaStatServerTotConns=sysPvaStatServerTotConns,
    sysModuleAllocationCpuRatio=sysModuleAllocationCpuRatio,
    sysTrunkStatPktsOut=sysTrunkStatPktsOut,
    sysSelfIpGroup=sysSelfIpGroup,
    sysGlobalHostCpuUser=sysGlobalHostCpuUser,
    sysHostMemory=sysHostMemory,
    sysSwImageGroup=sysSwImageGroup,
    sysPacketFilterStatNumber=sysPacketFilterStatNumber,
    sysServersslStatRc4Bulk=sysServersslStatRc4Bulk,
    sysInterfaceStatNumber=sysInterfaceStatNumber,
    sysGlobalTmmStatHttpRequests=sysGlobalTmmStatHttpRequests,
    sysGlobalIpStat=sysGlobalIpStat,
    sysInterfaceMediaActiveDuplex=sysInterfaceMediaActiveDuplex,
    sysInterfaceMtu=sysInterfaceMtu,
    sysMultiHostCpuIrq1m=sysMultiHostCpuIrq1m,
    sysGeneralHwName=sysGeneralHwName,
    sysChassisPowerSupplyIndex=sysChassisPowerSupplyIndex,
    sysGlobalHostCpuUsageRatio=sysGlobalHostCpuUsageRatio,
    sysPvaStatServerPktsIn=sysPvaStatServerPktsIn,
    sysPvaStatClientPktsOut=sysPvaStatClientPktsOut,
    wj300=wj300,
    sysStatServerBytesIn=sysStatServerBytesIn,
    sysSwStatusProduct=sysSwStatusProduct,
    sysInterfaceStatBytesOut=sysInterfaceStatBytesOut,
    sysFastL4StatRxunreach=sysFastL4StatRxunreach,
    sysClientsslStatSslv3=sysClientsslStatSslv3,
    sysL2ForwardStatMacAddr=sysL2ForwardStatMacAddr,
    sysStpInterfaceTreeStatDesigBridgePrio=sysStpInterfaceTreeStatDesigBridgePrio,
    sysTrunkStatResetStats=sysTrunkStatResetStats,
    sysServersslStatPrematureDisconnects=sysServersslStatPrematureDisconnects,
    sysTcpStatRxbadseg=sysTcpStatRxbadseg,
    sysProductName=sysProductName,
    sysClientsslStatSessCacheHits=sysClientsslStatSessCacheHits,
    sysDot3StatCarrierSenseErrors=sysDot3StatCarrierSenseErrors,
    sysAdminIpEntry=sysAdminIpEntry,
    sysStatPvaClientTotConns5m=sysStatPvaClientTotConns5m,
    sysIpStatErrCksum=sysIpStatErrCksum,
    sysRouteMgmtEntryDest=sysRouteMgmtEntryDest,
    sysInterfaceStatDropsIn=sysInterfaceStatDropsIn,
    sysClientsslStatPeercertInvalid=sysClientsslStatPeercertInvalid,
    sysMultiHostUsed=sysMultiHostUsed,
    sysHostInfoStat=sysHostInfoStat,
    sysGlobalIcmpStat=sysGlobalIcmpStat,
    sysGlobalIcmp6Stat=sysGlobalIcmp6Stat,
    sysHostCpuGroup=sysHostCpuGroup,
    sysFastHttpStatReqParseErrors=sysFastHttpStatReqParseErrors,
    sysServersslStatPartiallyHwAcceleratedConns=sysServersslStatPartiallyHwAcceleratedConns,
    sysStpBridgeStatBridgeHelloTime=sysStpBridgeStatBridgeHelloTime,
    sysRtspStatNumRequests=sysRtspStatNumRequests,
    sysMultiHostCpuStolen5s=sysMultiHostCpuStolen5s,
    sysFastL4StatResetStats=sysFastL4StatResetStats,
    sysGlobalHostCpuIdle5m=sysGlobalHostCpuIdle5m,
    sysHostCpu=sysHostCpu,
    sysMultiHostCpuNumber=sysMultiHostCpuNumber,
    sysAttrPacketFilter=sysAttrPacketFilter,
    sysHttpStatResp3xxCnt=sysHttpStatResp3xxCnt,
    sysGlobalHostCpuUsageRatio5s=sysGlobalHostCpuUsageRatio5s,
    sysServersslStatEncryptedBytesOut=sysServersslStatEncryptedBytesOut,
    sysClusters=sysClusters,
    sysStpInterfaceTreeStatFwdTransitions=sysStpInterfaceTreeStatFwdTransitions,
    sysTmmStatLicenseDeny=sysTmmStatLicenseDeny,
    sysUdpStatResetStats=sysUdpStatResetStats,
    sysStatConnectionMemoryErrors=sysStatConnectionMemoryErrors,
    sysServersslStatShaDigest=sysServersslStatShaDigest,
    sysPvaStatNumber=sysPvaStatNumber,
    sysStpInterfaceTreeStatIndex=sysStpInterfaceTreeStatIndex,
    sysVlanGroupName=sysVlanGroupName,
    sysServersslStatFullyHwAcceleratedConns=sysServersslStatFullyHwAcceleratedConns,
    sysChassisFanStatus=sysChassisFanStatus,
    sysStatResetStats=sysStatResetStats,
    sysSwHotfixProduct=sysSwHotfixProduct,
    sysStpInterfaceMbrStateRequested=sysStpInterfaceMbrStateRequested,
    sysClientsslStatCurCompatConns=sysClientsslStatCurCompatConns,
    sysStatServerTotConns5s=sysStatServerTotConns5s,
    sysHostDisk=sysHostDisk,
    sysClusterMbrStatusReason=sysClusterMbrStatusReason,
    sysDot3StatSqetestErrors=sysDot3StatSqetestErrors,
    sysChassisTempNumber=sysChassisTempNumber,
    sysIcmp6StatErrOpt=sysIcmp6StatErrOpt,
    sysHostCpuSoftirq=sysHostCpuSoftirq,
    sysGlobalTmmStatServerPktsIn=sysGlobalTmmStatServerPktsIn,
    sysL2ForwardStatIftype=sysL2ForwardStatIftype,
    sysHttpStatPlainPostcompressBytes=sysHttpStatPlainPostcompressBytes,
    sysIp6StatGroup=sysIp6StatGroup,
    sysAttrPacketFilterSendIcmpErrors=sysAttrPacketFilterSendIcmpErrors,
    sysSelfIpUnitId=sysSelfIpUnitId,
    sysInterfaceStatus=sysInterfaceStatus,
    sysCpuFanSpeed=sysCpuFanSpeed,
    sysInterfaceStatGroup=sysInterfaceStatGroup,
    sysAttrFailoverForceActive=sysAttrFailoverForceActive,
    sysIpStatTxFrag=sysIpStatTxFrag,
    sysSystemUptime=sysSystemUptime,
    sysClientsslStatDhDssKeyxchg=sysClientsslStatDhDssKeyxchg,
    sysIfxStatHcInUcastPkts=sysIfxStatHcInUcastPkts,
    sysFastHttpStatConnpoolMaxSize=sysFastHttpStatConnpoolMaxSize,
    sysStpGlobalsHelloTime=sysStpGlobalsHelloTime,
    sysStpBridgeTreeStatEntry=sysStpBridgeTreeStatEntry,
    sysClusterMbrAvailabilityState=sysClusterMbrAvailabilityState,
    sysPacketFilterNumber=sysPacketFilterNumber,
    sysMultiHostCpuIrq5m=sysMultiHostCpuIrq5m,
    bigip5100=bigip5100,
    sysDot1dbaseStatResetStats=sysDot1dbaseStatResetStats,
    sysStatLicenseDeny=sysStatLicenseDeny,
    sysStatClientCurConns5s=sysStatClientCurConns5s,
    sysMultiHostCpuSoftirq=sysMultiHostCpuSoftirq,
    sysClusterPriSlotId=sysClusterPriSlotId,
    sysTrunkStatCollisions=sysTrunkStatCollisions,
    sysStatPvaServerPktsIn=sysStatPvaServerPktsIn,
    sysTrunkName=sysTrunkName,
    sysMultiHostCpuUsageRatio=sysMultiHostCpuUsageRatio,
    sysClusterMinUpMbrsAction=sysClusterMinUpMbrsAction,
    sysInterfaceEnabled=sysInterfaceEnabled,
    sysStatClientBytesIn=sysStatClientBytesIn,
    sysTmmStatServerPktsOut=sysTmmStatServerPktsOut,
    sysSwHotfixGroup=sysSwHotfixGroup,
    sysGlobalTcpStat=sysGlobalTcpStat,
    sysPacketFilterGroup=sysPacketFilterGroup,
    sysTcpStatOpen=sysTcpStatOpen,
    sysSctpStatExpires=sysSctpStatExpires,
    sysStatPvaClientMaxConns1m=sysStatPvaClientMaxConns1m,
    sysTcpStatRxbadcookie=sysTcpStatRxbadcookie,
)
mibBuilder.exportSymbols(
    "F5-BIGIP-SYSTEM-MIB",
    swanWJ200=swanWJ200,
    sysFastHttpStatResetStats=sysFastHttpStatResetStats,
    sysStatClientBytesOut=sysStatClientBytesOut,
    sysPacketFilterMacAddr=sysPacketFilterMacAddr,
    sysServersslStatEdhRsaKeyxchg=sysServersslStatEdhRsaKeyxchg,
    sysTrunkStatMcastOut=sysTrunkStatMcastOut,
    sysVlanGroupMbrEntry=sysVlanGroupMbrEntry,
    sysSystem=sysSystem,
    sysVlanGroupMbrTable=sysVlanGroupMbrTable,
    sysInterfaceStpLink=sysInterfaceStpLink,
    sysStatAuthCurSessions=sysStatAuthCurSessions,
    sysStatServerCurConns=sysStatServerCurConns,
    sysFastHttpStatResp2xxCnt=sysFastHttpStatResp2xxCnt,
    sysMultiHostCpuStolen5m=sysMultiHostCpuStolen5m,
    sysVlanSourceCheck=sysVlanSourceCheck,
    sysAdminIp=sysAdminIp,
    sysStpRegionalRootAddr=sysStpRegionalRootAddr,
    bigipSystemCompliance=bigipSystemCompliance,
    sysServersslStatPeercertInvalid=sysServersslStatPeercertInvalid,
    sysPvaStatClientMaxConns=sysPvaStatClientMaxConns,
    sysDot1dbaseStatGroup=sysDot1dbaseStatGroup,
    sysIp6StatResetStats=sysIp6StatResetStats,
    sysTmmStatTmid=sysTmmStatTmid,
    sysIfxStatHighSpeed=sysIfxStatHighSpeed,
    sysClientsslStatCurConns=sysClientsslStatCurConns,
    sysMultiHostCpuIowait1m=sysMultiHostCpuIowait1m,
    sysStpInterfaceStatGroup=sysStpInterfaceStatGroup,
    sysCpuSlot=sysCpuSlot,
    sysArpNdp=sysArpNdp,
    sysSubMemoryResetStats=sysSubMemoryResetStats,
    sysVlanSpanningTree=sysVlanSpanningTree,
    sysAttrWatchdogState=sysAttrWatchdogState,
    sysGlobalHostCpuIrq5m=sysGlobalHostCpuIrq5m,
    sysGlobalStreamStat=sysGlobalStreamStat,
    sysGlobalTmmStatServerCurConns=sysGlobalTmmStatServerCurConns,
    sysMultiHostCpuUser1m=sysMultiHostCpuUser1m,
    sysRouteStaticEntryGroup=sysRouteStaticEntryGroup,
    sysStatServerPktsIn=sysStatServerPktsIn,
    sysMultiHostMode=sysMultiHostMode,
    sysVlanFailsafeTimeout=sysVlanFailsafeTimeout,
    sysPlatformInfoName=sysPlatformInfoName,
    sysTmmStatTable=sysTmmStatTable,
    sysDot3StatDeferredTx=sysDot3StatDeferredTx,
    sysIcmpStatErrMem=sysIcmpStatErrMem,
    sysStatPvaClientCurConns1m=sysStatPvaClientCurConns1m,
    sysFastL4StatAcceptfails=sysFastL4StatAcceptfails,
    sysVlanGroupMacTrue=sysVlanGroupMacTrue,
    sysGlobals=sysGlobals,
    sysStatPvaServerTotConns=sysStatPvaServerTotConns,
    sysGlobalStat=sysGlobalStat,
    sysStatHardSyncookieDet=sysStatHardSyncookieDet,
    sysPacketFilterAddrEntry=sysPacketFilterAddrEntry,
    sysHttpStatRamcacheMissesAll=sysHttpStatRamcacheMissesAll,
    sysMultiHostCpuUsageRatio5s=sysMultiHostCpuUsageRatio5s,
    sysAttrPacketFilterEstablished=sysAttrPacketFilterEstablished,
    sysVlanMemberType=sysVlanMemberType,
    sysStatPvaClientPktsOut5m=sysStatPvaClientPktsOut5m,
    sysMultiHostCpuEntry=sysMultiHostCpuEntry,
    bigip2400=bigip2400,
    sysStpInterfaceMbrName=sysStpInterfaceMbrName,
    sysTmmStatServerPktsIn=sysTmmStatServerPktsIn,
    sysIp6StatRxFragDropped=sysIp6StatRxFragDropped,
    sysPacketFilterVname=sysPacketFilterVname,
    sysL2ForwardMacAddr=sysL2ForwardMacAddr,
    sysServersslStatNotssl=sysServersslStatNotssl,
    sysSwVolumeActive=sysSwVolumeActive,
    sysClientsslStatDssKeyxchg=sysClientsslStatDssKeyxchg,
    sysIntfMediaSfpTable=sysIntfMediaSfpTable,
    sysFastHttpStatServerRxBad=sysFastHttpStatServerRxBad,
    sysIp6StatErrMem=sysIp6StatErrMem,
    sysIpStatReassembled=sysIpStatReassembled,
    sysStpInterfaceMbrRole=sysStpInterfaceMbrRole,
    sysTcpStatAccepts=sysTcpStatAccepts,
    sysAdminIpAddr=sysAdminIpAddr,
    sysPlatform=sysPlatform,
    sysInterfaceGroup=sysInterfaceGroup,
    sysSwHotfixNumber=sysSwHotfixNumber,
    sysTcpStatRxbadsum=sysTcpStatRxbadsum,
    sysModuleAllocationEntry=sysModuleAllocationEntry,
    sysVlanMacMasquerade=sysVlanMacMasquerade,
    sysTcpStatSyncacheover=sysTcpStatSyncacheover,
    sysFastL4StatSyncookAccept=sysFastL4StatSyncookAccept,
    bigip4100=bigip4100,
    sysStatPvaServerPktsOut=sysStatPvaServerPktsOut,
    sysStpBridgeTreeStatIndex=sysStpBridgeTreeStatIndex,
    sysGlobalHostCpuIdle1m=sysGlobalHostCpuIdle1m,
    sysUdpStatRxbaddgram=sysUdpStatRxbaddgram,
    sysIpStatErrLen=sysIpStatErrLen,
    sysUdpStatConnects=sysUdpStatConnects,
    sysSwVolumeEntry=sysSwVolumeEntry,
    sysGlobalHostCpuStolen1m=sysGlobalHostCpuStolen1m,
    sysTmmStatGroup=sysTmmStatGroup,
    sysProduct=sysProduct,
    sysGlobalTmmStatTmUsageRatio5s=sysGlobalTmmStatTmUsageRatio5s,
    sysSelfIpTable=sysSelfIpTable,
    sysMultiHostTable=sysMultiHostTable,
    sysIfTable=sysIfTable,
    sysSwVolumeGroup=sysSwVolumeGroup,
    sysClientsslStatTotCompatConns=sysClientsslStatTotCompatConns,
    sysServersslStatPeercertValid=sysServersslStatPeercertValid,
    sysAttrModeMaint=sysAttrModeMaint,
    sysHostMemoryGroup=sysHostMemoryGroup,
    sysGlobalRtspStat=sysGlobalRtspStat,
    sysProductDate=sysProductDate,
    sysPvaStatPvaId=sysPvaStatPvaId,
    sysStatPvaClientBytesIn5m=sysStatPvaClientBytesIn5m,
    sysFastHttpStatClientAccepts=sysFastHttpStatClientAccepts,
    sysArpStaticEntryEntry=sysArpStaticEntryEntry,
    sysGlobalIiopStat=sysGlobalIiopStat,
    sysServersslStatRecordsIn=sysServersslStatRecordsIn,
    sysPvaStatServerBytesIn=sysPvaStatServerBytesIn,
    sysStatPvaServerPktsIn1m=sysStatPvaServerPktsIn1m,
    sysStpInterfaceMbrTable=sysStpInterfaceMbrTable,
    sysStpInterfaceTreeStatDesigRootPrio=sysStpInterfaceTreeStatDesigRootPrio,
    sysAttrPacketFilterAllowImportantIcmp=sysAttrPacketFilterAllowImportantIcmp,
    sysSoftwareStatus=sysSoftwareStatus,
    sysIcmpStatErrProto=sysIcmpStatErrProto,
    sysPacketFilterMac=sysPacketFilterMac,
    sysSubMemoryAllocated=sysSubMemoryAllocated,
    sysSctpStatRxbadsum=sysSctpStatRxbadsum,
    sysStatAuthFailureResults=sysStatAuthFailureResults,
    sysStatPvaServerPktsOut5s=sysStatPvaServerPktsOut5s,
    sysIiopStatNumResponses=sysIiopStatNumResponses,
    sysSoftwareImage=sysSoftwareImage,
    sysIfName=sysIfName,
    sysHttpStatOctetPostcompressBytes=sysHttpStatOctetPostcompressBytes,
    sysTrunkEntry=sysTrunkEntry,
    sysGlobalHostCpuIowait5m=sysGlobalHostCpuIowait5m,
    sysIntfMediaIndex=sysIntfMediaIndex,
    sysStatPvaClientMaxConns=sysStatPvaClientMaxConns,
    sysIp6StatErrOpt=sysIp6StatErrOpt,
    sysVlanGroupMode=sysVlanGroupMode,
    sysStpGlobalsMaxHops=sysStpGlobalsMaxHops,
    sysInterfaceStatTable=sysInterfaceStatTable,
    sysStpBridgeStatFwdDelay=sysStpBridgeStatFwdDelay,
    sysTcpStatConnfails=sysTcpStatConnfails,
    sysXmlStatResetStats=sysXmlStatResetStats,
    sysClientsslStatRc2Bulk=sysClientsslStatRc2Bulk,
    sysGlobalTmmStatClientPktsIn=sysGlobalTmmStatClientPktsIn,
    sysMultiHostCpuSoftirq5s=sysMultiHostCpuSoftirq5s,
    sysSwImageVersion=sysSwImageVersion,
    sysFastL4StatExpires=sysFastL4StatExpires,
    sysStatServerBytesOut5m=sysStatServerBytesOut5m,
    sysClientsslStatSessCacheOverflows=sysClientsslStatSessCacheOverflows,
    sysServersslStatMaxCompatConns=sysServersslStatMaxCompatConns,
    sysTcpStatAcceptfails=sysTcpStatAcceptfails,
    sysCpuGroup=sysCpuGroup,
    sysAttrArpRetries=sysAttrArpRetries,
    sysDot3StatTable=sysDot3StatTable,
    sysStpInterfaceMbrInstanceId=sysStpInterfaceMbrInstanceId,
    sysTmmStatServerTotConns=sysTmmStatServerTotConns,
    sysTmmStatOutgoingPacketErrors=sysTmmStatOutgoingPacketErrors,
    sysDeviceModelOIDs=sysDeviceModelOIDs,
    sysRouteStaticEntryDest=sysRouteStaticEntryDest,
    sysHttpStatPlainPrecompressBytes=sysHttpStatPlainPrecompressBytes,
    sysChassisPowerSupplyEntry=sysChassisPowerSupplyEntry,
    sysSelfPortEntry=sysSelfPortEntry,
    sysDot3StatAlignmentErrors=sysDot3StatAlignmentErrors,
    sysGlobalTmmStatMaxConnVirtualPathDeny=sysGlobalTmmStatMaxConnVirtualPathDeny,
    sysTmmStatClientTotConns=sysTmmStatClientTotConns,
    sysServersslStatCurNativeConns=sysServersslStatCurNativeConns,
    sysStpInterfaceStatTable=sysStpInterfaceStatTable,
    sysTmmStatCmpConnRedirected=sysTmmStatCmpConnRedirected,
    sysSpanningTree=sysSpanningTree,
    sysClientsslStatTotConns5s=sysClientsslStatTotConns5s,
    firepass4100=firepass4100,
    sysAttrFailoverNetwork=sysAttrFailoverNetwork,
    sysStatCurrPvaAssistConn=sysStatCurrPvaAssistConn,
    sysPvaStatServerCurConns=sysPvaStatServerCurConns,
    sysMultiHostHostId=sysMultiHostHostId,
    sysHttpStatCssPrecompressBytes=sysHttpStatCssPrecompressBytes,
    sysRouteStaticEntryGateway=sysRouteStaticEntryGateway,
    sysPacketFilterAddrTable=sysPacketFilterAddrTable,
    sysGlobalHostCpuSystem5s=sysGlobalHostCpuSystem5s,
    sysChassisPowerSupplyGroup=sysChassisPowerSupplyGroup,
    sysDot3StatCollisionFreq=sysDot3StatCollisionFreq,
    sysStpInstanceId=sysStpInstanceId,
    sysIfGroup=sysIfGroup,
    sysSctpStatConnects=sysSctpStatConnects,
    sysSwVolumeTable=sysSwVolumeTable,
    sysRouteStaticEntryEntry=sysRouteStaticEntryEntry,
    sysPacketFilterRclass=sysPacketFilterRclass,
    sysHostDiskFreeNodes=sysHostDiskFreeNodes,
    sysTrunkStatName=sysTrunkStatName,
    sysGlobalHostCpuStolen=sysGlobalHostCpuStolen,
    sysSctpStatGroup=sysSctpStatGroup,
    sysStatPvaClientBytesIn=sysStatPvaClientBytesIn,
    sysTmmStatClientBytesOut=sysTmmStatClientBytesOut,
    wj800=wj800,
    sysInterfaceStatDropsOut=sysInterfaceStatDropsOut,
    sysStatMemoryUsed=sysStatMemoryUsed,
    sysFastL4StatRxbadunreach=sysFastL4StatRxbadunreach,
    sysClusterMbrGroup=sysClusterMbrGroup,
    sysStatGroup=sysStatGroup,
    sysStpInterfaceStatEntry=sysStpInterfaceStatEntry,
    sysStatClientMaxConns5m=sysStatClientMaxConns5m,
    sysIcmp6StatErrMem=sysIcmp6StatErrMem,
    sysStpInterfaceMbrPriority=sysStpInterfaceMbrPriority,
    sysPlatformInfoMarketingName=sysPlatformInfoMarketingName,
    sysL2ForwardIfname=sysL2ForwardIfname,
    sysHostCpuUser=sysHostCpuUser,
    sysStpInterfaceTreeStatPriority=sysStpInterfaceTreeStatPriority,
    sysStpInterfaceTreeStatDesigPortNum=sysStpInterfaceTreeStatDesigPortNum,
    sysPacketFilterStatTable=sysPacketFilterStatTable,
    sysIcmp6StatGroup=sysIcmp6StatGroup,
    sysSelfIpNetmaskType=sysSelfIpNetmaskType,
    sysGlobalTmmStatTmTotalCycles=sysGlobalTmmStatTmTotalCycles,
    sysStpGlobalsMode=sysStpGlobalsMode,
    sysStpInterfaceStatRootPrio=sysStpInterfaceStatRootPrio,
    sysL2ForwardAttrGroup=sysL2ForwardAttrGroup,
    sysTmmStatClientPktsIn=sysTmmStatClientPktsIn,
    sysHostCpuTable=sysHostCpuTable,
    sysVlanMemberTagged=sysVlanMemberTagged,
    bigip5110=bigip5110,
    sysDot3StatGroup=sysDot3StatGroup,
    bigip3600=bigip3600,
    sysIntfMediaSfpName=sysIntfMediaSfpName,
    sysTrunkStatErrorsOut=sysTrunkStatErrorsOut,
    sysSwHotfixVerified=sysSwHotfixVerified,
    sysRouteMgmtEntryGateway=sysRouteMgmtEntryGateway,
    sysSctpStatRxrst=sysSctpStatRxrst,
    sysStpBridgeTreeStatInternalPathCost=sysStpBridgeTreeStatInternalPathCost,
    sysStreamStatReplaces=sysStreamStatReplaces,
    sysSwStatusGroup=sysSwStatusGroup,
    sysArpStaticEntryNumber=sysArpStaticEntryNumber,
    sysStatAuthTotSessions=sysStatAuthTotSessions,
    sysSctpStatConnfails=sysSctpStatConnfails,
    sysTrunkCfgMember=sysTrunkCfgMember,
    sysAttrConfigsyncState=sysAttrConfigsyncState,
    sysStatClientTotConns5s=sysStatClientTotConns5s,
    arx500=arx500,
    sysTmmStatNumber=sysTmmStatNumber,
    sysSctpStatRxbadcookie=sysSctpStatRxbadcookie,
    sysSoftwareVolume=sysSoftwareVolume,
    sysStatActiveCpuCount=sysStatActiveCpuCount,
    sysL2=sysL2,
    sysL2ForwardStatVlanName=sysL2ForwardStatVlanName,
    sysGlobalHostCpuSoftirq1m=sysGlobalHostCpuSoftirq1m,
    sysDot1dbaseStatMacAddr=sysDot1dbaseStatMacAddr,
    sysDot3StatLateCollisions=sysDot3StatLateCollisions,
    sysIp6StatReassembled=sysIp6StatReassembled,
    sysAttrFailoverForceStandby=sysAttrFailoverForceStandby,
    sysChassisFanEntry=sysChassisFanEntry,
    sysStatPvaClientPktsIn5s=sysStatPvaClientPktsIn5s,
    sysPacketFilterVlanTable=sysPacketFilterVlanTable,
    sysStatPvaClientBytesOut1m=sysStatPvaClientBytesOut1m,
    sysStatClientPktsIn5s=sysStatClientPktsIn5s,
    sysServersslStatSessCacheCurEntries=sysServersslStatSessCacheCurEntries,
    sysGlobalHostCpuStolen5s=sysGlobalHostCpuStolen5s,
    sysTmmStatTmSleepCycles=sysTmmStatTmSleepCycles,
    sysSwImageNumber=sysSwImageNumber,
    sysChassisTempGroup=sysChassisTempGroup,
    sysStatPvaClientBytesOut5m=sysStatPvaClientBytesOut5m,
    sysTcpStatRxooseg=sysTcpStatRxooseg,
)
mibBuilder.exportSymbols(
    "F5-BIGIP-SYSTEM-MIB",
    sysSwStatusActive=sysSwStatusActive,
    sysStatServerBytesIn5s=sysStatServerBytesIn5s,
    sysTrunkStatGroup=sysTrunkStatGroup,
    sysHttpStatV9Resp=sysHttpStatV9Resp,
    sysRouteStaticEntryNetmask=sysRouteStaticEntryNetmask,
    sysIcmpStatErrOpt=sysIcmpStatErrOpt,
    sysSelfPortDefPort=sysSelfPortDefPort,
    sysInterfaceStpEdge=sysInterfaceStpEdge,
    sysServersslStatMaxConns=sysServersslStatMaxConns,
    sysStatServerBytesOut=sysStatServerBytesOut,
    sysStpBridgeTreeStatPriority=sysStpBridgeTreeStatPriority,
    sysSwHotfixSlotId=sysSwHotfixSlotId,
    sysDot3StatNumber=sysDot3StatNumber,
    sysClientsslStatDesBulk=sysClientsslStatDesBulk,
    sysStatMultiProcessorMode=sysStatMultiProcessorMode,
    sysStpInterfaceStatPortNum=sysStpInterfaceStatPortNum,
    sysGlobalHostCpuSoftirq=sysGlobalHostCpuSoftirq,
    sysChassisTempTemperature=sysChassisTempTemperature,
    sysGlobalHostCpuUsageRatio5m=sysGlobalHostCpuUsageRatio5m,
    sysSwHotfixEntry=sysSwHotfixEntry,
    sysIfEntry=sysIfEntry,
    sysGlobalTmmStatServerBytesOut=sysGlobalTmmStatServerBytesOut,
    PYSNMP_MODULE_ID=bigipSystem,
    sysHostCpuSystem=sysHostCpuSystem,
    sysCpuName=sysCpuName,
    sysStatServerPktsIn1m=sysStatServerPktsIn1m,
    sysVlanNumber=sysVlanNumber,
    sysDot1dbaseStatPortEntry=sysDot1dbaseStatPortEntry,
    sysSwImageBuild=sysSwImageBuild,
    sysStatPvaServerMaxConns1m=sysStatPvaServerMaxConns1m,
    sysSctpStatAccepts=sysSctpStatAccepts,
    sysStpGlobalsTransmitHold=sysStpGlobalsTransmitHold,
    sysSelfPorts=sysSelfPorts,
    sysUdpStatRxnosum=sysUdpStatRxnosum,
    sysStatClientPktsIn1m=sysStatClientPktsIn1m,
    sysSoftware=sysSoftware,
    sysGeneralHwNumber=sysGeneralHwNumber,
    sysPvaStatHardSyncookieDet=sysPvaStatHardSyncookieDet,
    sysIcmpStatErrLen=sysIcmpStatErrLen,
    sysSystemVersion=sysSystemVersion,
    sysUdpStatAcceptfails=sysUdpStatAcceptfails,
    sysRouteMgmtEntryNetmaskType=sysRouteMgmtEntryNetmaskType,
    sysHttpStatV10Resp=sysHttpStatV10Resp,
    sysIiopStatNumFragments=sysIiopStatNumFragments,
    sysIcmpStatTx=sysIcmpStatTx,
    sysIp6StatTxFrag=sysIp6StatTxFrag,
    sysIntfMediaMediaOption=sysIntfMediaMediaOption,
    sysStreamStatGroup=sysStreamStatGroup,
    sysGlobalFastL4Stat=sysGlobalFastL4Stat,
    sysStatClientBytesOut5s=sysStatClientBytesOut5s,
    sysStatPvaServerBytesOut1m=sysStatPvaServerBytesOut1m,
    sysVlanGroupTable=sysVlanGroupTable,
    sysHttpStatCssPostcompressBytes=sysHttpStatCssPostcompressBytes,
    sysGlobalTmmStatMaintenanceModeDeny=sysGlobalTmmStatMaintenanceModeDeny,
    sysIp6StatErrCksum=sysIp6StatErrCksum,
    sysProductVersion=sysProductVersion,
    sysStatServerPktsOut5m=sysStatServerPktsOut5m,
    sysMultiHostActiveCpuCount=sysMultiHostActiveCpuCount,
    bigipSystemGroups=bigipSystemGroups,
    sysStpInterfaceStatStpEnable=sysStpInterfaceStatStpEnable,
    sysSubMemorySize=sysSubMemorySize,
    sysHttpStatRamcacheMissBytesAll=sysHttpStatRamcacheMissBytesAll,
    sysStpInterfaceTreeStatEntry=sysStpInterfaceTreeStatEntry,
    sysIfxStatInMulticastPkts=sysIfxStatInMulticastPkts,
    sysDot3StatFrameTooLongs=sysDot3StatFrameTooLongs,
    wj500=wj500,
    sysAuthStatMaxSessions=sysAuthStatMaxSessions,
    sysGlobalTmmStatNoHandlerDeny=sysGlobalTmmStatNoHandlerDeny,
    sysRouteStaticEntryDestType=sysRouteStaticEntryDestType,
    sysIntfMediaSfpGroup=sysIntfMediaSfpGroup,
    sysSubMemoryEntry=sysSubMemoryEntry,
    unknown=unknown,
    sysTrunkOperBw=sysTrunkOperBw,
    sysSwStatusVersion=sysSwStatusVersion,
    sysDot1dbaseStatPortMtuExceededDiscards=sysDot1dbaseStatPortMtuExceededDiscards,
    sysGlobalHostMemUsed=sysGlobalHostMemUsed,
    sysIfxStat=sysIfxStat,
    sysGlobalTmmStatMemoryTotal=sysGlobalTmmStatMemoryTotal,
    sysSctpStatAbandons=sysSctpStatAbandons,
    sysClusterName=sysClusterName,
    sysProductGroup=sysProductGroup,
    sysHttpStatGetReqs=sysHttpStatGetReqs,
    sysPacketFilterAddress=sysPacketFilterAddress,
    sysArpStaticEntryTable=sysArpStaticEntryTable,
    bigip6400=bigip6400,
    sysVlanGroupBridgeMulticast=sysVlanGroupBridgeMulticast,
    sysMultiHostGroup=sysMultiHostGroup,
    sysAttrArpMaxEntries=sysAttrArpMaxEntries,
    sysStatTmSleepCycles=sysStatTmSleepCycles,
    sysStatClientPktsOut5s=sysStatClientPktsOut5s,
    sysClientsslStatSessCacheLookups=sysClientsslStatSessCacheLookups,
    sysStatPvaServerBytesOut5s=sysStatPvaServerBytesOut5s,
    sysUdpStatAccepts=sysUdpStatAccepts,
    sysIiopStatResetStats=sysIiopStatResetStats,
    sysHttpStatResp2xxCnt=sysHttpStatResp2xxCnt,
    sysTrunkStatDropsIn=sysTrunkStatDropsIn,
    sysSwVolumeSlotId=sysSwVolumeSlotId,
    sysTcpStatTxrexmits=sysTcpStatTxrexmits,
    sysStpInterfaceMbrStateActive=sysStpInterfaceMbrStateActive,
    sysAdminIpTable=sysAdminIpTable,
    sysIcmp6StatDrop=sysIcmp6StatDrop,
    sysDot3StatIntmacTxErrors=sysDot3StatIntmacTxErrors,
    sysIcmp6StatTx=sysIcmp6StatTx,
    sysStatClientBytesIn1m=sysStatClientBytesIn1m,
    sysRtspStatNumResponses=sysRtspStatNumResponses,
    sysHttpStatNullCompressBytes=sysHttpStatNullCompressBytes,
    sysFastL4StatAccepts=sysFastL4StatAccepts,
    sysTmmStatServerBytesOut=sysTmmStatServerBytesOut,
    sysRouteStaticEntryPoolName=sysRouteStaticEntryPoolName,
    sysAttrVlanFDBTimeout=sysAttrVlanFDBTimeout,
    sysStatServerPktsIn5m=sysStatServerPktsIn5m,
    sysStatHttpRequests=sysStatHttpRequests,
    sysSwImageFilename=sysSwImageFilename,
    sysModuleAllocationProvisionLevel=sysModuleAllocationProvisionLevel,
    sysIfxStatHcOutUcastPkts=sysIfxStatHcOutUcastPkts,
    sysDot1dbaseStatPortNumber=sysDot1dbaseStatPortNumber,
    sysIntfMediaSfpNumber=sysIntfMediaSfpNumber,
    sysPvaStatTable=sysPvaStatTable,
    sysL2ForwardStatGroup=sysL2ForwardStatGroup,
    sysUdpStatTxdgram=sysUdpStatTxdgram,
    sysIfxStatInBroadcastPkts=sysIfxStatInBroadcastPkts,
    sysTrunkShortTimeout=sysTrunkShortTimeout,
    sysClusterMbrPriming=sysClusterMbrPriming,
    sysFastHttpStatPipelinedReqs=sysFastHttpStatPipelinedReqs,
    sysServersslStatRecordsOut=sysServersslStatRecordsOut,
    sysClientsslStatTotConns1m=sysClientsslStatTotConns1m,
    sysPacketFilterEntry=sysPacketFilterEntry,
    sysConnPoolStatConnects=sysConnPoolStatConnects,
    sysIp6StatErrProto=sysIp6StatErrProto,
    sysAttrPacketFilterDefaultAction=sysAttrPacketFilterDefaultAction,
    sysTcpStatCloseWait=sysTcpStatCloseWait,
    sysMultiHostCpuStolen=sysMultiHostCpuStolen,
    sysSoftwareHotfix=sysSoftwareHotfix,
    sysGlobalHostGroup=sysGlobalHostGroup,
    sysRouteMgmtEntryType=sysRouteMgmtEntryType,
    sysIpStatDropped=sysIpStatDropped,
    sysSwStatusBuild=sysSwStatusBuild,
    sysSelfIps=sysSelfIps,
    sysHttpStatRespBucket1k=sysHttpStatRespBucket1k,
    sysHttpStatGroup=sysHttpStatGroup,
    sysGlobalHostCpuSoftirq5s=sysGlobalHostCpuSoftirq5s,
    sysSwImageEntry=sysSwImageEntry,
    sysRtspStatNumErrors=sysRtspStatNumErrors,
    sysTransmission=sysTransmission,
    sysStatServerCurConns5m=sysStatServerCurConns5m,
    sysPacketFilterMacTable=sysPacketFilterMacTable,
    sysStpInterfaceTreeStatInternalPathCost=sysStpInterfaceTreeStatInternalPathCost,
    sysClientsslStatFatalAlerts=sysClientsslStatFatalAlerts,
    sysMultiHostCpuSystem1m=sysMultiHostCpuSystem1m,
    sysClientsslStatMd5Digest=sysClientsslStatMd5Digest,
    sysInterfaceId=sysInterfaceId,
    sysFastHttpStatConnpoolExhausted=sysFastHttpStatConnpoolExhausted,
    sysSelfPortDefProtocol=sysSelfPortDefProtocol,
    sysModuleAllocationMemoryRatio=sysModuleAllocationMemoryRatio,
    sysClusterMbrEnabled=sysClusterMbrEnabled,
    sysHostCpuIndex=sysHostCpuIndex,
    sysGlobalTmmStatServerBytesIn=sysGlobalTmmStatServerBytesIn,
    sysStatPvaClientCurConns5s=sysStatPvaClientCurConns5s,
    sysHttpStatRamcacheHitBytes=sysHttpStatRamcacheHitBytes,
    sysStpVlanMbrTable=sysStpVlanMbrTable,
    sysCpuTable=sysCpuTable,
    sysHostDiskPartition=sysHostDiskPartition,
    sysPacketFilterMacIndex=sysPacketFilterMacIndex,
    sysHttpStatV11Reqs=sysHttpStatV11Reqs,
    sysGlobalTmmStatOutgoingPacketErrors=sysGlobalTmmStatOutgoingPacketErrors,
    sysTmmStatNoHandlerDeny=sysTmmStatNoHandlerDeny,
    sysInterfaceStatCollisions=sysInterfaceStatCollisions,
    sysStatPvaClientTotConns1m=sysStatPvaClientTotConns1m,
    sysHttpStatRamcacheCount=sysHttpStatRamcacheCount,
    sysStatClientCurConns5m=sysStatClientCurConns5m,
    sysServersslStatEdhDssKeyxchg=sysServersslStatEdhDssKeyxchg,
    sysStatPvaServerCurConns5m=sysStatPvaServerCurConns5m,
    sysStpBridgeStatMode=sysStpBridgeStatMode,
    sysClientsslStatPeercertNone=sysClientsslStatPeercertNone,
    sysVlanId=sysVlanId,
    sysStatPvaClientBytesIn5s=sysStatPvaClientBytesIn5s,
    sysVlanMemberTable=sysVlanMemberTable,
    sysVlanGroupGroup=sysVlanGroupGroup,
    sysIcmp6StatErr=sysIcmp6StatErr,
    sysAttrBootQuiet=sysAttrBootQuiet,
    sysStatClientCurConns=sysStatClientCurConns,
    sysIfxStatHcOutBroadcastPkts=sysIfxStatHcOutBroadcastPkts,
    sysClusterMbrDisabledParentType=sysClusterMbrDisabledParentType,
    sysClientsslStatBadRecords=sysClientsslStatBadRecords,
    firepass1200=firepass1200,
    sysStpInterfaceTreeStatName=sysStpInterfaceTreeStatName,
    sysGlobalTmmStatMaxConnVirtualAddrDeny=sysGlobalTmmStatMaxConnVirtualAddrDeny,
    sysHostCpuNice=sysHostCpuNice,
    sysTmmStatHttpRequests=sysTmmStatHttpRequests,
    sysStatServerTotConns1m=sysStatServerTotConns1m,
    sysSelfIpIsFloating=sysSelfIpIsFloating,
    em500=em500,
    sysIntfMediaGroup=sysIntfMediaGroup,
    sysPacketFilters=sysPacketFilters,
    sysGlobalTmmStatServerMaxConns=sysGlobalTmmStatServerMaxConns,
    sysPacketFilterVlanGroup=sysPacketFilterVlanGroup,
    sysPacketFilterAddrIpType=sysPacketFilterAddrIpType,
    sysStatPvaServerTotConns1m=sysStatPvaServerTotConns1m,
    sysClusterMinUpMbrs=sysClusterMinUpMbrs,
    sysGlobalHostCpuStolen5m=sysGlobalHostCpuStolen5m,
    sysTcpStatTimeWait=sysTcpStatTimeWait,
    sysStpGlobalsRevision=sysStpGlobalsRevision,
    sysDot1dBridge=sysDot1dBridge,
    sysRouteMgmtEntryEntry=sysRouteMgmtEntryEntry,
    sysStpInterfaceTreeStatDesigPortPriority=sysStpInterfaceTreeStatDesigPortPriority,
    sysPacketFilterVlanName=sysPacketFilterVlanName,
    sysIcmp6StatErrRtx=sysIcmp6StatErrRtx,
    sysInterfaceNumber=sysInterfaceNumber,
    sysSelfPortProtocol=sysSelfPortProtocol,
    sysChassisTempTable=sysChassisTempTable,
    sysMultiHostCpuNice5m=sysMultiHostCpuNice5m,
    sysIfxStatHcOutMulticastPkts=sysIfxStatHcOutMulticastPkts,
    bigip8950=bigip8950,
    sysPvaStatCurAssistConns=sysPvaStatCurAssistConns,
    sysInterfaceStatPktsOut=sysInterfaceStatPktsOut,
    sysClusterFloatMgmtNetmaskType=sysClusterFloatMgmtNetmaskType,
    sysDot1dbaseStatType=sysDot1dbaseStatType,
    sysStpBridgeTreeStatTcCount=sysStpBridgeTreeStatTcCount,
    sysHttpStatResp4xxCnt=sysHttpStatResp4xxCnt,
    sysConnPoolStatResetStats=sysConnPoolStatResetStats,
    sysGlobalHostCpuIdle5s=sysGlobalHostCpuIdle5s,
    sysClusterMbr=sysClusterMbr,
    sysClusterStatusReason=sysClusterStatusReason,
    sysModuleAllocationTable=sysModuleAllocationTable,
    sysStpInterfaceTreeStat=sysStpInterfaceTreeStat,
    sysTrunkStatBytesIn=sysTrunkStatBytesIn,
    sysDot3StatResetStats=sysDot3StatResetStats,
    sysClientsslStatNullBulk=sysClientsslStatNullBulk,
    sysStatMemoryTotal=sysStatMemoryTotal,
    sysSelfPortDefTable=sysSelfPortDefTable,
    sysUdpStatRxdgram=sysUdpStatRxdgram,
    sysGlobalHostCpuUser5s=sysGlobalHostCpuUser5s,
    sysTmmStatTmUsageRatio5s=sysTmmStatTmUsageRatio5s,
    sysGlobalAuthStat=sysGlobalAuthStat,
    sysVlanDataGroup=sysVlanDataGroup,
    sysStpBridgeStatRootPrio=sysStpBridgeStatRootPrio,
    sysHttpStatCookiePersistInserts=sysHttpStatCookiePersistInserts,
    sysMultiHostCpuNice=sysMultiHostCpuNice,
    sysGlobalTmmStatClientBytesIn=sysGlobalTmmStatClientBytesIn,
    sysInterfaceStatPktsIn=sysInterfaceStatPktsIn,
    sysVlanEntry=sysVlanEntry,
    sysClusterMbrCluster=sysClusterMbrCluster,
    sysInterfaceSfpMedia=sysInterfaceSfpMedia,
    sysRouteMgmtEntry=sysRouteMgmtEntry,
    sysVlanTable=sysVlanTable,
    sysPvaStatServerPktsOut=sysPvaStatServerPktsOut,
    sysStatTmTotalCycles=sysStatTmTotalCycles,
    sysFastL4StatRxbadsum=sysFastL4StatRxbadsum,
    sysGlobalHostCpuIowait1m=sysGlobalHostCpuIowait1m,
    sysStatPvaClientCurConns5m=sysStatPvaClientCurConns5m,
    sysL2ForwardAttr=sysL2ForwardAttr,
    sysSwImageBuildDate=sysSwImageBuildDate,
    sysStpGlobals=sysStpGlobals,
    sysHttpStatRamcacheMisses=sysHttpStatRamcacheMisses,
)
mibBuilder.exportSymbols(
    "F5-BIGIP-SYSTEM-MIB",
    sysVlanMemberNumber=sysVlanMemberNumber,
    sysStatPvaServerBytesOut5m=sysStatPvaServerBytesOut5m,
    sysGlobalHost=sysGlobalHost,
    sysStatServerMaxConns=sysStatServerMaxConns,
    sysStpBridgeTreeStatInstanceId=sysStpBridgeTreeStatInstanceId,
    sysMultiHostCpuIrq=sysMultiHostCpuIrq,
    sysTmmStatTmmId=sysTmmStatTmmId,
    sysSwHotfixBuild=sysSwHotfixBuild,
    sysGlobalIp6Stat=sysGlobalIp6Stat,
    sysHttpStatPrecompressBytes=sysHttpStatPrecompressBytes,
    sysServersslStatAesBulk=sysServersslStatAesBulk,
    sysStatPvaClientTotConns5s=sysStatPvaClientTotConns5s,
    sysStatPvaServerPktsIn5m=sysStatPvaServerPktsIn5m,
    sysSwHotfixFilename=sysSwHotfixFilename,
    sysStpInterfaceMbrPathCost=sysStpInterfaceMbrPathCost,
    sysAttrPvaAcceleration=sysAttrPvaAcceleration,
    sysServersslStatAdhKeyxchg=sysServersslStatAdhKeyxchg,
    sysSwHotfixHotfixId=sysSwHotfixHotfixId,
    sysStpTable=sysStpTable,
    sysStpInterfaceTreeStatDesigRootAddr=sysStpInterfaceTreeStatDesigRootAddr,
    sysStpBridgeTreeStatTable=sysStpBridgeTreeStatTable,
    sysAdmin=sysAdmin,
    sysHttpStatImagePrecompressBytes=sysHttpStatImagePrecompressBytes,
    sysServersslStatRsaKeyxchg=sysServersslStatRsaKeyxchg,
    sysStpInterfaceMbrEntry=sysStpInterfaceMbrEntry,
    sysDot3StatEntry=sysDot3StatEntry,
    sysHostMemoryTotal=sysHostMemoryTotal,
    sysTmmStatClientCurConns=sysTmmStatClientCurConns,
    sysClusterHaState=sysClusterHaState,
    sysChassisFanTable=sysChassisFanTable,
    sysVlanLearnMode=sysVlanLearnMode,
    sysStpPriority=sysStpPriority,
    sysGlobalHostCpuNice5m=sysGlobalHostCpuNice5m,
    sysMultiHostCpuStolen1m=sysMultiHostCpuStolen1m,
    sysStatPvaServerBytesIn5m=sysStatPvaServerBytesIn5m,
    sysPacketFilterVlan=sysPacketFilterVlan,
    sysClusterMbrLicensed=sysClusterMbrLicensed,
    sysDot3Stat=sysDot3Stat,
    sysStpBridgeStatBridgeMaxAge=sysStpBridgeStatBridgeMaxAge,
    sysGlobalHostCpuIrq5s=sysGlobalHostCpuIrq5s,
    sysNetwork=sysNetwork,
    sysIpStatRxFrag=sysIpStatRxFrag,
    sysGlobalHostCpuSystem1m=sysGlobalHostCpuSystem1m,
    sysFastHttpStatServerConnects=sysFastHttpStatServerConnects,
    sysAuthStatTotSessions=sysAuthStatTotSessions,
    sysIntfMediaSfpIndex=sysIntfMediaSfpIndex,
    sysTrunkStatPktsIn=sysTrunkStatPktsIn,
    sysSwHotfixTable=sysSwHotfixTable,
    sysRouteStaticEntryNetmaskType=sysRouteStaticEntryNetmaskType,
    sysStpBridgeTreeStatGroup=sysStpBridgeTreeStatGroup,
    sysFastHttpStatRespParseErrors=sysFastHttpStatRespParseErrors,
    arx1000=arx1000,
    sysClientsslStatResetStats=sysClientsslStatResetStats,
    sysIcmpStatErrCksum=sysIcmpStatErrCksum,
    sysHttpStatRespBucket64k=sysHttpStatRespBucket64k,
    sysClientsslStatMaxConns=sysClientsslStatMaxConns,
    sysRouteMgmtEntryMtu=sysRouteMgmtEntryMtu,
    sysStatServerMaxConns5s=sysStatServerMaxConns5s,
    sysIcmp6StatErrLen=sysIcmp6StatErrLen,
    sysProxyExclusionEntry=sysProxyExclusionEntry,
    sysGlobalHostCpuSystem5m=sysGlobalHostCpuSystem5m,
    sysIcmp6StatRx=sysIcmp6StatRx,
    sysFastHttpStatV11Reqs=sysFastHttpStatV11Reqs,
    sysStatServerMaxConns1m=sysStatServerMaxConns1m,
    sysMultiHost=sysMultiHost,
    sysUdpStatOpen=sysUdpStatOpen,
    sysTrunkStatTable=sysTrunkStatTable,
    sysVlan=sysVlan,
    sysHttpStatRespBucket32k=sysHttpStatRespBucket32k,
    sysHttpStatOtherPostcompressBytes=sysHttpStatOtherPostcompressBytes,
    sysTrunks=sysTrunks,
    sysIp6StatDropped=sysIp6StatDropped,
    sysServersslStatNullBulk=sysServersslStatNullBulk,
    sysMultiHostCpuNice5s=sysMultiHostCpuNice5s,
    sysHttpStatPostReqs=sysHttpStatPostReqs,
    sysHostDiskTotalBlocks=sysHostDiskTotalBlocks,
    sysHttpStatAudioPrecompressBytes=sysHttpStatAudioPrecompressBytes,
    sysFastHttpStatConnpoolCurSize=sysFastHttpStatConnpoolCurSize,
    sysInterfaceMediaActiveSpeed=sysInterfaceMediaActiveSpeed,
    TrafficShield4100=TrafficShield4100,
    sysMultiHostCpuUsageRatio1m=sysMultiHostCpuUsageRatio1m,
    sysClientsslStatFullyHwAcceleratedConns=sysClientsslStatFullyHwAcceleratedConns,
    sysStpBridgeStatPathCost=sysStpBridgeStatPathCost,
    sysAttrArpTimeout=sysAttrArpTimeout,
    sysStatPvaClientPktsIn1m=sysStatPvaClientPktsIn1m,
    bigip540=bigip540,
    sysMultiHostCpuIowait5s=sysMultiHostCpuIowait5s,
    bigipSystem=bigipSystem,
    sysProductBuild=sysProductBuild,
    sysGlobalHostCpuIowait5s=sysGlobalHostCpuIowait5s,
    sysAuthStatFailureResults=sysAuthStatFailureResults,
    sysStatPvaServerMaxConns5s=sysStatPvaServerMaxConns5s,
    sysInterfaceStpEdgeActive=sysInterfaceStpEdgeActive,
    sysDot3StatIntmacRxErrors=sysDot3StatIntmacRxErrors,
    sysSwImageSlotId=sysSwImageSlotId,
    sysVlanGroupNumber=sysVlanGroupNumber,
    sysGlobalTmmStatClientBytesOut=sysGlobalTmmStatClientBytesOut,
    sysHttpStatV11Resp=sysHttpStatV11Resp,
    sysHttpStatResp5xxCnt=sysHttpStatResp5xxCnt,
    sysTrunkGroup=sysTrunkGroup,
    sysSubMemory=sysSubMemory,
    sysGlobalTmmStatClientCurConns=sysGlobalTmmStatClientCurConns,
    sysStatAuthMaxSessions=sysStatAuthMaxSessions,
    sysStatClientCurConns1m=sysStatClientCurConns1m,
    sysIcmp6StatErrCksum=sysIcmp6StatErrCksum,
    sysHttpStatVideoPostcompressBytes=sysHttpStatVideoPostcompressBytes,
    sysStpRootAddr=sysStpRootAddr,
    sysL2Forward=sysL2Forward,
    sysServersslStatHandshakeFailures=sysServersslStatHandshakeFailures,
    sysClientsslStatMaxCompatConns=sysClientsslStatMaxCompatConns,
    sysClientsslStatCurNativeConns=sysClientsslStatCurNativeConns,
    sysHostDiskNumber=sysHostDiskNumber,
    sysFastL4StatGroup=sysFastL4StatGroup,
    sysRouteMgmtEntryNumber=sysRouteMgmtEntryNumber,
    sysUdpStatConnfails=sysUdpStatConnfails,
    sysInterfaces=sysInterfaces,
    sysPacketFilterRname=sysPacketFilterRname,
    sysStatPvaServerTotConns5m=sysStatPvaServerTotConns5m,
    sysStatClientMaxConns=sysStatClientMaxConns,
    bigip8400=bigip8400,
    sysTrunkStatEntry=sysTrunkStatEntry,
    sysSubMemoryTable=sysSubMemoryTable,
    sysClientsslStatSslv2=sysClientsslStatSslv2,
    sysStpBridgeTreeStatDesigRootAddr=sysStpBridgeTreeStatDesigRootAddr,
    sysGlobalStats=sysGlobalStats,
    sysHttpStatV9Reqs=sysHttpStatV9Reqs,
    sysInterfaceMediaMaxSpeed=sysInterfaceMediaMaxSpeed,
    sysRouteStaticEntry=sysRouteStaticEntry,
    sysSwStatusNumber=sysSwStatusNumber,
    sysVlanGroupMbrGroupName=sysVlanGroupMbrGroupName,
    sysModuleAllocation=sysModuleAllocation,
    sysVlanMemberParentVname=sysVlanMemberParentVname,
    sysSelfPortAddrType=sysSelfPortAddrType,
    sysIntfMediaEntry=sysIntfMediaEntry,
    sysStatServerTotConns=sysStatServerTotConns,
    sysProductHotfix=sysProductHotfix,
    sysStatOutgoingPacketErrors=sysStatOutgoingPacketErrors,
    sysHostCpuNumber=sysHostCpuNumber,
    sysGlobalHostCpuCount=sysGlobalHostCpuCount,
    sysRtspStatResetStats=sysRtspStatResetStats,
    sysStpGlobalsGroup=sysStpGlobalsGroup,
    sysClientsslStatNotssl=sysClientsslStatNotssl,
    sysStatPvaServerMaxConns5m=sysStatPvaServerMaxConns5m,
    sysInterfacePreferSfp=sysInterfacePreferSfp,
    sysGeneralChassisSerialNum=sysGeneralChassisSerialNum,
    sysClientsslStatHandshakeFailures=sysClientsslStatHandshakeFailures,
    sysGlobalHostMemTotal=sysGlobalHostMemTotal,
    sysSubMemoryName=sysSubMemoryName,
    sysChassisFan=sysChassisFan,
    sysStatPvaServerMaxConns=sysStatPvaServerMaxConns,
    sysRouteStaticEntryVlanName=sysRouteStaticEntryVlanName,
    sysTrunkActiveLacp=sysTrunkActiveLacp,
    sysPacketFilterAddrNumber=sysPacketFilterAddrNumber,
    sysVlanMirrorHashPortEnable=sysVlanMirrorHashPortEnable,
    sysHttpStatHtmlPostcompressBytes=sysHttpStatHtmlPostcompressBytes,
    sysPacketFilterStatGroup=sysPacketFilterStatGroup,
    sysSwStatusVolume=sysSwStatusVolume,
    sysServersslStatMidstreamRenegotiations=sysServersslStatMidstreamRenegotiations,
    sysHostDiskEntry=sysHostDiskEntry,
    sysCluster=sysCluster,
    sysStpInterfaceStatResetStats=sysStpInterfaceStatResetStats,
    sysHttpStatJsPostcompressBytes=sysHttpStatJsPostcompressBytes,
    sysInterfaceLearnMode=sysInterfaceLearnMode,
    sysTmmStatResetStats=sysTmmStatResetStats,
    sysClientsslStatEdhRsaKeyxchg=sysClientsslStatEdhRsaKeyxchg,
    sysServersslStatPeercertNone=sysServersslStatPeercertNone,
    sysFastHttpStatResp5xxCnt=sysFastHttpStatResp5xxCnt,
    sysMultiHostCpuSystem5m=sysMultiHostCpuSystem5m,
    sysClusterMbrEnabledStat=sysClusterMbrEnabledStat,
    sysFastHttpStatGroup=sysFastHttpStatGroup,
    sysClusterFloatMgmtIpType=sysClusterFloatMgmtIpType,
    sysVlanVname=sysVlanVname,
    sysStpGlobalsIdentifier=sysStpGlobalsIdentifier,
    sysRtspStatNumInterleavedData=sysRtspStatNumInterleavedData,
    sysServersslStatSslv2=sysServersslStatSslv2,
    sysServersslStatDesBulk=sysServersslStatDesBulk,
    sysClientsslStatTlsv1=sysClientsslStatTlsv1,
    sysGlobalAttr=sysGlobalAttr,
    sysMultiHostCpuCount=sysMultiHostCpuCount,
    sysStatServerBytesIn1m=sysStatServerBytesIn1m,
    sysIp6StatTxFragDropped=sysIp6StatTxFragDropped,
    sysStatNoHandlerDeny=sysStatNoHandlerDeny,
    sysTrunkCfgMemberNumber=sysTrunkCfgMemberNumber,
    sysChassisPowerSupplyStatus=sysChassisPowerSupplyStatus,
    sysMultiHostCpuUsageRatio5m=sysMultiHostCpuUsageRatio5m,
    sysFastL4StatSyncookIssue=sysFastL4StatSyncookIssue,
    sysVlanGroupBridgeInStandby=sysVlanGroupBridgeInStandby,
    sysFastHttpStatNumberReqs=sysFastHttpStatNumberReqs,
    sysChassisPowerSupplyTable=sysChassisPowerSupplyTable,
    sysRouteMgmtEntryNetmask=sysRouteMgmtEntryNetmask,
    sysVlanGroupEntry=sysVlanGroupEntry,
    sysRouteMgmtEntryGatewayType=sysRouteMgmtEntryGatewayType,
    sysTmmStatTmUsageRatio1m=sysTmmStatTmUsageRatio1m,
    sysHttpStatRamcacheEvictions=sysHttpStatRamcacheEvictions,
    sysSubMemoryGroup=sysSubMemoryGroup,
    sysPacketFilterVlanNumber=sysPacketFilterVlanNumber,
    sysGlobalTmmStatIncomingPacketErrors=sysGlobalTmmStatIncomingPacketErrors,
    sysPacketFilterMacGroup=sysPacketFilterMacGroup,
    sysGlobalTmmStatClientMaxConns=sysGlobalTmmStatClientMaxConns,
    sysSctpStatAcceptfails=sysSctpStatAcceptfails,
    sysSelfIpNumber=sysSelfIpNumber,
    sysDot3StatFcsErrors=sysDot3StatFcsErrors,
    sysStatClientTotConns5m=sysStatClientTotConns5m,
    sysSwImageProduct=sysSwImageProduct,
    sysServersslStatResetStats=sysServersslStatResetStats,
    sysStpGlobalsMaxAge=sysStpGlobalsMaxAge,
    sysSelfPortGroup=sysSelfPortGroup,
    sysStatPvaServerPktsOut5m=sysStatPvaServerPktsOut5m,
    sysTmmStatServerMaxConns=sysTmmStatServerMaxConns,
    sysInterfaceStatMcastIn=sysInterfaceStatMcastIn,
    sysInterfaceStatErrorsIn=sysInterfaceStatErrorsIn,
    sysTcpStatRxcookie=sysTcpStatRxcookie,
    sysMultiHostCpuNice1m=sysMultiHostCpuNice1m,
    sysServersslStatSessCacheLookups=sysServersslStatSessCacheLookups,
    sysHostDiskFreeBlocks=sysHostDiskFreeBlocks,
    sysFastHttpStatV10Reqs=sysFastHttpStatV10Reqs,
    sysHttpStatVideoPrecompressBytes=sysHttpStatVideoPrecompressBytes,
    sysClientsslStatPartiallyHwAcceleratedConns=sysClientsslStatPartiallyHwAcceleratedConns,
    sysIp6StatRxFrag=sysIp6StatRxFrag,
    sysIiopStatGroup=sysIiopStatGroup,
    sysGlobalServerSslStat=sysGlobalServerSslStat,
    sysVlanGroupMbrGroup=sysVlanGroupMbrGroup,
    sysStpInterfaceStatNumber=sysStpInterfaceStatNumber,
    sysPvaStatClientCurConns=sysPvaStatClientCurConns,
    sysMultiHostCpuIdle=sysMultiHostCpuIdle,
    sam4300=sam4300,
    sysTmmStatServerCurConns=sysTmmStatServerCurConns,
    sysStpInterfaceStatPathCost=sysStpInterfaceStatPathCost,
    sysClientsslStatRecordsOut=sysClientsslStatRecordsOut,
    sysHttpStatNumberReqs=sysHttpStatNumberReqs,
    sysStpInterfaceMbrGroup=sysStpInterfaceMbrGroup,
    sysSwHotfixVersion=sysSwHotfixVersion,
    sysGlobalTmmStatNpus=sysGlobalTmmStatNpus,
    sysStatPvaServerBytesIn5s=sysStatPvaServerBytesIn5s,
    sysTmmStatClientPktsOut=sysTmmStatClientPktsOut,
    sysStatCpuCount=sysStatCpuCount,
    sysHostDiskGroup=sysHostDiskGroup,
    sysHttpStatRespBucket4k=sysHttpStatRespBucket4k,
    sysChassisTemp=sysChassisTemp,
    sysSwHotfixChksum=sysSwHotfixChksum,
    sysStatPvaServerPktsIn5s=sysStatPvaServerPktsIn5s,
    sysClusterMbrMgmtAddr=sysClusterMbrMgmtAddr,
    sysTrunkStpEnable=sysTrunkStpEnable,
    sysServersslStatDecryptedBytesOut=sysServersslStatDecryptedBytesOut,
    sysIcmp6StatResetStats=sysIcmp6StatResetStats,
    sysPacketFilter=sysPacketFilter,
    sysInterfaceName=sysInterfaceName,
    sysCpuTemperature=sysCpuTemperature,
    sysStpInterfaceStatName=sysStpInterfaceStatName,
    sysStpInterfaceTreeStatTable=sysStpInterfaceTreeStatTable,
    sysServersslStatCurCompatConns=sysServersslStatCurCompatConns,
    sysStpBridgeTreeStatRootPortNum=sysStpBridgeTreeStatRootPortNum,
    sysGlobalAttrs=sysGlobalAttrs,
    sysDot3StatMultiCollisionFrames=sysDot3StatMultiCollisionFrames,
)
mibBuilder.exportSymbols(
    "F5-BIGIP-SYSTEM-MIB",
    sysIfxStatGroup=sysIfxStatGroup,
    sysPacketFilterStatHits=sysPacketFilterStatHits,
    sysStatDroppedPackets=sysStatDroppedPackets,
    sysIcmpStatRx=sysIcmpStatRx,
    sysTrunk=sysTrunk,
    sysClusterGroup=sysClusterGroup,
    sysTrunkStatErrorsIn=sysTrunkStatErrorsIn,
    sysGlobalHostCpuIdle=sysGlobalHostCpuIdle,
    sysVlanMemberEntry=sysVlanMemberEntry,
    sysPacketFilterStatEntry=sysPacketFilterStatEntry,
    bigip8900=bigip8900,
    sysTmmStat=sysTmmStat,
    sysAttrFailoverSslhardwareAction=sysAttrFailoverSslhardwareAction,
    sysPacketFilterAddrIndex=sysPacketFilterAddrIndex,
    sysServersslStatTotNativeConns=sysServersslStatTotNativeConns,
    sysStatPvaClientBytesOut5s=sysStatPvaClientBytesOut5s,
    sysIntfMediaName=sysIntfMediaName,
    sysStatPvaClientTotConns=sysStatPvaClientTotConns,
    sysTrunkStatDropsOut=sysTrunkStatDropsOut,
    sysInterfaceMediaMaxDuplex=sysInterfaceMediaMaxDuplex,
    sysIpStatErrOpt=sysIpStatErrOpt,
    sysL2ForwardStatNumber=sysL2ForwardStatNumber,
    sysHttpStatRamcacheMissBytes=sysHttpStatRamcacheMissBytes,
    sysInterfaceStatErrorsOut=sysInterfaceStatErrorsOut,
    sysTmmStatMaxConnVirtualAddrDeny=sysTmmStatMaxConnVirtualAddrDeny,
    sysIntfMediaNumber=sysIntfMediaNumber,
    sysStatClientBytesOut5m=sysStatClientBytesOut5m,
    sysProductEdition=sysProductEdition,
    sysL2ForwardStat=sysL2ForwardStat,
    sysRtspStatGroup=sysRtspStatGroup,
    sysStpInterfaceTreeStatNumber=sysStpInterfaceTreeStatNumber,
    sysTrunkStpReset=sysTrunkStpReset,
    sysGlobalTmmStatCmpConnRedirected=sysGlobalTmmStatCmpConnRedirected,
    sysIntfMediaTable=sysIntfMediaTable,
    sysInterfaceStpAuto=sysInterfaceStpAuto,
    sysGlobalTmmStatMemoryUsed=sysGlobalTmmStatMemoryUsed,
    sysMultiHostCpuIdle5m=sysMultiHostCpuIdle5m,
    sysServersslStatSslv3=sysServersslStatSslv3,
    sysClusterMbrMgmtAddrType=sysClusterMbrMgmtAddrType,
    sysTrunkNumber=sysTrunkNumber,
    bigip3900=bigip3900,
    sysGlobalTmmStatResetStats=sysGlobalTmmStatResetStats,
    sysGlobalHostCpuIrq=sysGlobalHostCpuIrq,
    sysPvaStatHardSyncookieGen=sysPvaStatHardSyncookieGen,
    sysProxyExclusion=sysProxyExclusion,
    sysPvaStatGroup=sysPvaStatGroup,
    sysGlobalTmmStatDroppedPackets=sysGlobalTmmStatDroppedPackets,
    sysStatPvaClientMaxConns5m=sysStatPvaClientMaxConns5m,
    sysAttrFailoverMemoryRestartPercent=sysAttrFailoverMemoryRestartPercent,
    sysHttpStatJsPrecompressBytes=sysHttpStatJsPrecompressBytes,
    sysVlanMacTrue=sysVlanMacTrue,
    sysL2ForwardEntry=sysL2ForwardEntry,
    sysDot3StatCollisionCount=sysDot3StatCollisionCount,
    sysClientsslStatEdhDssKeyxchg=sysClientsslStatEdhDssKeyxchg,
    sysStpBridgeStatMaxAge=sysStpBridgeStatMaxAge,
    sysStatServerBytesOut1m=sysStatServerBytesOut1m,
    sysStatServerMaxConns5m=sysStatServerMaxConns5m,
    bigipPb100n=bigipPb100n,
    sysStatTmIdleCycles=sysStatTmIdleCycles,
    bigip520=bigip520,
    sysDot1dbaseStatPortPort=sysDot1dbaseStatPortPort,
    sysClientsslStatTotConns5m=sysClientsslStatTotConns5m,
    sysMultiHostCpuSoftirq1m=sysMultiHostCpuSoftirq1m,
    sysVlanFailsafeEnabled=sysVlanFailsafeEnabled,
    sysClientsslStatNullDigest=sysClientsslStatNullDigest,
    sysL2ForwardGroup=sysL2ForwardGroup,
    sysRouteMgmtEntryTable=sysRouteMgmtEntryTable,
    sysIfxStatEntry=sysIfxStatEntry,
    sysFastL4StatSyncookReject=sysFastL4StatSyncookReject,
    sysStpInterfaceStatRootAddr=sysStpInterfaceStatRootAddr,
    sysGlobalHostCpuSoftirq5m=sysGlobalHostCpuSoftirq5m,
    sysAttrConnAdaptiveReaperHiwat=sysAttrConnAdaptiveReaperHiwat,
    sysUdpStatRxunreach=sysUdpStatRxunreach,
    em3000=em3000,
    sysTrunkStatNumber=sysTrunkStatNumber,
    sysL2ForwardStatDynamic=sysL2ForwardStatDynamic,
    sysPacketFilterMacEntry=sysPacketFilterMacEntry,
    sysServersslStatFatalAlerts=sysServersslStatFatalAlerts,
    sysIfxStatCounterDiscontinuityTime=sysIfxStatCounterDiscontinuityTime,
    sysDot3StatName=sysDot3StatName,
    sysIfxStatHcInOctets=sysIfxStatHcInOctets,
    sysTcpStatRxrst=sysTcpStatRxrst,
    sysStpBridgeStatResetStats=sysStpBridgeStatResetStats,
    sysStatServerCurConns1m=sysStatServerCurConns1m,
    sysIp6StatErrReassembledTooLong=sysIp6StatErrReassembledTooLong,
    sysMultiHostCpuUser5m=sysMultiHostCpuUser5m,
    sysServersslStatEncryptedBytesIn=sysServersslStatEncryptedBytesIn,
    sysMultiHostCpu=sysMultiHostCpu,
    sysHttpStatV10Reqs=sysHttpStatV10Reqs,
    sysFastHttpStatConnpoolReuses=sysFastHttpStatConnpoolReuses,
    sysCpuIndex=sysCpuIndex,
    sysRouteMgmtEntryGroup=sysRouteMgmtEntryGroup,
    sysL2ForwardVlanName=sysL2ForwardVlanName,
    sysGlobalXmlStat=sysGlobalXmlStat,
    sysGlobalTmmStatTmIdleCycles=sysGlobalTmmStatTmIdleCycles,
    sysStatPvaClientBytesIn1m=sysStatPvaClientBytesIn1m,
    sysVlanGroupMbrNumber=sysVlanGroupMbrNumber,
    sysGlobalTmmStatServerPktsOut=sysGlobalTmmStatServerPktsOut,
    sysStpInterfaceTreeStatDesigCost=sysStpInterfaceTreeStatDesigCost,
    sysHttpStatResetStats=sysHttpStatResetStats,
    sysStpInterfaceMbrType=sysStpInterfaceMbrType,
    sysTcpStatGroup=sysTcpStatGroup,
    sysInterfaceStatBytesIn=sysInterfaceStatBytesIn,
    sysUdpStatGroup=sysUdpStatGroup,
    sysStatPvaServerBytesOut=sysStatPvaServerBytesOut,
    sysHttpStatOtherPrecompressBytes=sysHttpStatOtherPrecompressBytes,
    sysDot1dbaseStatNumPorts=sysDot1dbaseStatNumPorts,
    sysConnPoolStatCurSize=sysConnPoolStatCurSize,
    sysMultiHostCpuIowait5m=sysMultiHostCpuIowait5m,
    sysIcmpStatForward=sysIcmpStatForward,
    sysChassisTempEntry=sysChassisTempEntry,
    sysIcmpStatErr=sysIcmpStatErr,
    sysStpVlanMbrVlanVname=sysStpVlanMbrVlanVname,
    sysStatTotPvaAssistConn=sysStatTotPvaAssistConn,
    sysIpStatErrProto=sysIpStatErrProto,
    sysGlobalTmmStat=sysGlobalTmmStat,
    sysPlatformInfoGroup=sysPlatformInfoGroup,
    sysStatIncomingPacketErrors=sysStatIncomingPacketErrors,
    sysVlanMtu=sysVlanMtu,
    sysHostDiskTotalNodes=sysHostDiskTotalNodes,
    sysSystemMachine=sysSystemMachine,
    bigip3400=bigip3400,
    em4000=em4000,
    sysProxyExclusionGroup=sysProxyExclusionGroup,
    sysTmmStatServerBytesIn=sysTmmStatServerBytesIn,
    sysStpGroup=sysStpGroup,
    sysRoute=sysRoute,
    sysMultiHostCpuGroup=sysMultiHostCpuGroup,
    sysStatServerBytesOut5s=sysStatServerBytesOut5s,
    sysArpStaticEntryMacAddr=sysArpStaticEntryMacAddr,
    sysSelfPortDefGroup=sysSelfPortDefGroup,
    sysHttpStatImagePostcompressBytes=sysHttpStatImagePostcompressBytes,
    sysTrunkStatus=sysTrunkStatus,
    sysTmmStatEntry=sysTmmStatEntry,
    sysTrunkTable=sysTrunkTable,
    sysClientsslStatDhRsaKeyxchg=sysClientsslStatDhRsaKeyxchg,
    sysSwStatusSlotId=sysSwStatusSlotId,
    sysIntfMediaSfpEntry=sysIntfMediaSfpEntry,
    sysStatVirtualServerNonSynDeny=sysStatVirtualServerNonSynDeny,
    sysStatPvaServerCurConns=sysStatPvaServerCurConns,
    sysInterfaceMediaOptions=sysInterfaceMediaOptions,
    sysStatClientMaxConns5s=sysStatClientMaxConns5s,
    sysTrunkCfgMemberTrunkName=sysTrunkCfgMemberTrunkName,
    sysServersslStatDssKeyxchg=sysServersslStatDssKeyxchg,
    sysGlobalUdpStat=sysGlobalUdpStat,
    sysAttrFailoverSslhardware=sysAttrFailoverSslhardware,
    sysStatClientPktsOut=sysStatClientPktsOut,
    sysInterfaceMediaSfp=sysInterfaceMediaSfp,
    sysIp6StatErrLen=sysIp6StatErrLen,
    sysStatPvaClientBytesOut=sysStatPvaClientBytesOut,
    sysStatPvaServerTotConns5s=sysStatPvaServerTotConns5s,
    sysSystemGroup=sysSystemGroup,
    sysSelfPortDefNumber=sysSelfPortDefNumber,
    sysAuthStatErrorResults=sysAuthStatErrorResults,
    sysTrunkCfgMemberGroup=sysTrunkCfgMemberGroup,
    sysStatMaxConnVirtualPathDeny=sysStatMaxConnVirtualPathDeny,
    sysModuleAllocationDiskRatio=sysModuleAllocationDiskRatio,
    sysStatPvaServerCurConns1m=sysStatPvaServerCurConns1m,
    sysClientsslStatGroup=sysClientsslStatGroup,
    sysIpStatErrReassembledTooLong=sysIpStatErrReassembledTooLong,
    sysPvaStatServerBytesOut=sysPvaStatServerBytesOut,
    sysProxyExclusionNumber=sysProxyExclusionNumber,
    sysIcmpStatDrop=sysIcmpStatDrop,
    sysStpBridgeStat=sysStpBridgeStat,
    sysClusterEnabledStat=sysClusterEnabledStat,
    bigip6800=bigip6800,
    sysSubMemoryNumber=sysSubMemoryNumber,
    sysIfxStatHcInBroadcastPkts=sysIfxStatHcInBroadcastPkts,
    sysIfNumber=sysIfNumber,
    sysIiopStatNumCancels=sysIiopStatNumCancels,
    sysClientsslStatIdeaBulk=sysClientsslStatIdeaBulk,
    sysStpVlanMbrInstanceId=sysStpVlanMbrInstanceId,
    sysRouteStaticEntryGatewayType=sysRouteStaticEntryGatewayType,
    sysAttrArpAddReciprocal=sysAttrArpAddReciprocal,
    sysStpInterfaceStat=sysStpInterfaceStat,
    sysL2ForwardNumber=sysL2ForwardNumber,
    sysSelfIpAddr=sysSelfIpAddr,
    sysTrunkStatMcastIn=sysTrunkStatMcastIn,
    sysFastHttpStatResp3xxCnt=sysFastHttpStatResp3xxCnt,
    sysTmmStatIncomingPacketErrors=sysTmmStatIncomingPacketErrors,
    sysTmmStatCpu=sysTmmStatCpu,
    sysIiopStatNumRequests=sysIiopStatNumRequests,
    sysStpInterfaceStatRootCost=sysStpInterfaceStatRootCost,
    sysChassisFanGroup=sysChassisFanGroup,
    sysIpStatGroup=sysIpStatGroup,
    bigip3410=bigip3410,
    sysStreamStatResetStats=sysStreamStatResetStats,
    arx2000=arx2000,
    sysVlanFailsafeAction=sysVlanFailsafeAction,
    sysVlanMember=sysVlanMember,
    sysStpBridgeTreeStatRootPort=sysStpBridgeTreeStatRootPort,
    sysClientsslStatDecryptedBytesIn=sysClientsslStatDecryptedBytesIn,
    sysGlobalSctpStat=sysGlobalSctpStat,
    sysModules=sysModules,
    sysServersslStatGroup=sysServersslStatGroup,
    sysDot1dbaseStatPort=sysDot1dbaseStatPort,
    sysDot1dbaseStatPortName=sysDot1dbaseStatPortName,
    bigip1600=bigip1600,
    sysIfIndex=sysIfIndex,
    sysStpBridgeTreeStatDesigRootPrio=sysStpBridgeTreeStatDesigRootPrio,
    sysIfxStatName=sysIfxStatName,
    sysStpInterfaceTreeStatStatRole=sysStpInterfaceTreeStatStatRole,
    sysSwHotfixHotfixTitle=sysSwHotfixHotfixTitle,
    sysStpInterfaceMbrNumber=sysStpInterfaceMbrNumber,
    sysStpVlanMbrNumber=sysStpVlanMbrNumber,
    sysClusterPriSelTime=sysClusterPriSelTime,
    sysL2ForwardStatTable=sysL2ForwardStatTable,
    sysAuthStatResetStats=sysAuthStatResetStats,
    sysSelfPort=sysSelfPort,
    sysHttpStatMaxKeepaliveReq=sysHttpStatMaxKeepaliveReq,
    sysStatPvaServerPktsOut1m=sysStatPvaServerPktsOut1m,
    sysSwImageVerified=sysSwImageVerified,
    sysChassis=sysChassis,
    sysSystemRelease=sysSystemRelease,
    sysPacketFilterAddrIp=sysPacketFilterAddrIp,
    sysIpStatRxFragDropped=sysIpStatRxFragDropped,
    sysInterfacePhyMaster=sysInterfacePhyMaster,
    sysVlanMemberVmname=sysVlanMemberVmname,
    sysConnPoolStatReuses=sysConnPoolStatReuses,
    sysL2ForwardIftype=sysL2ForwardIftype,
    sysRouteStaticEntryMtu=sysRouteStaticEntryMtu,
    sysTrunkLacpEnabled=sysTrunkLacpEnabled,
    sysClientsslStatDecryptedBytesOut=sysClientsslStatDecryptedBytesOut,
    sysHostCpuId=sysHostCpuId,
    sysGlobalFastHttpStat=sysGlobalFastHttpStat,
    sysTrunkStatBytesOut=sysTrunkStatBytesOut,
    sysServersslStatMaxNativeConns=sysServersslStatMaxNativeConns,
    sysPvaStatTotAssistConns=sysPvaStatTotAssistConns,
    sysAuthStatSuccessResults=sysAuthStatSuccessResults,
    bigipVirtualEdition=bigipVirtualEdition,
    sysL2ForwardDynamic=sysL2ForwardDynamic,
    sysGlobalTmmStatVirtualServerNonSynDeny=sysGlobalTmmStatVirtualServerNonSynDeny,
    sysMultiHostCpuUser5s=sysMultiHostCpuUser5s,
    sysStatPvaServerCurConns5s=sysStatPvaServerCurConns5s,
    sysSwImageFileSize=sysSwImageFileSize,
    sysStatServerBytesIn5m=sysStatServerBytesIn5m,
    sysChassisPowerSupply=sysChassisPowerSupply,
    sysXmlStatGroup=sysXmlStatGroup,
    sysServersslStatSessCacheInvalidations=sysServersslStatSessCacheInvalidations,
    sysVlanGroupMbrVlanName=sysVlanGroupMbrVlanName,
    sysStatClientPktsOut5m=sysStatClientPktsOut5m,
    sysHttpStatRespBucket16k=sysHttpStatRespBucket16k,
    sysIfxStatHcInMulticastPkts=sysIfxStatHcInMulticastPkts,
    sysGlobalConnPoolStat=sysGlobalConnPoolStat,
    sysFastL4StatServersynrtx=sysFastL4StatServersynrtx,
    sysPacketFilterStatRname=sysPacketFilterStatRname,
    sysStpVlanMbr=sysStpVlanMbr,
    sysProxyExclusionTable=sysProxyExclusionTable,
    sysSelfIp=sysSelfIp,
    sysPacketFilterAddrGroup=sysPacketFilterAddrGroup,
    sysMultiHostCpuUser=sysMultiHostCpuUser,
    sysCpuEntry=sysCpuEntry,
    sysStatClientBytesIn5m=sysStatClientBytesIn5m,
    sysClusterMbrSlotId=sysClusterMbrSlotId,
)
mibBuilder.exportSymbols(
    "F5-BIGIP-SYSTEM-MIB",
    sysTrunkCfgMemberEntry=sysTrunkCfgMemberEntry,
    sysStpBridgeStatRootAddr=sysStpBridgeStatRootAddr,
    sysSwVolumeSize=sysSwVolumeSize,
    sysIcmpStatResetStats=sysIcmpStatResetStats,
    sysServersslStatNullDigest=sysServersslStatNullDigest,
    sysSelfPortPort=sysSelfPortPort,
    sysStatMaintenanceModeDeny=sysStatMaintenanceModeDeny,
    sysServersslStatNonHwAcceleratedConns=sysServersslStatNonHwAcceleratedConns,
    sysStpInterfaceMbr=sysStpInterfaceMbr,
    sysFastHttpStatPostReqs=sysFastHttpStatPostReqs,
    sysGlobalTmmStatClientPktsOut=sysGlobalTmmStatClientPktsOut,
    sysInterfaceStatEntry=sysInterfaceStatEntry,
    sysFastHttpStatClientRxBad=sysFastHttpStatClientRxBad,
    sysServersslStatTotCompatConns=sysServersslStatTotCompatConns,
    sysInterfaceStatResetStats=sysInterfaceStatResetStats,
    sysStpInterfaceTreeStatDesigBridgeAddr=sysStpInterfaceTreeStatDesigBridgeAddr,
    wj400=wj400,
    sysMultiHostCpuId=sysMultiHostCpuId,
    sysStp=sysStp,
    sysGlobalTmmStatServerTotConns=sysGlobalTmmStatServerTotConns,
    sysHttpStatHtmlPrecompressBytes=sysHttpStatHtmlPrecompressBytes,
    sysHttpStatOctetPrecompressBytes=sysHttpStatOctetPrecompressBytes,
    sysPvaStat=sysPvaStat,
    sysSwStatusTable=sysSwStatusTable,
    sysStatPvaClientPktsOut1m=sysStatPvaClientPktsOut1m,
    sysInterfaceComboPort=sysInterfaceComboPort,
    sysInterfaceFlowCtrlReq=sysInterfaceFlowCtrlReq,
    sysRouteMgmtEntryDestType=sysRouteMgmtEntryDestType,
    bigip1000=bigip1000,
    pysmiFakeCol1000=pysmiFakeCol1000,
    sysSwImageLastModified=sysSwImageLastModified,
    sysClientsslStatMaxNativeConns=sysClientsslStatMaxNativeConns,
    sysGlobalHostCpuIrq1m=sysGlobalHostCpuIrq1m,
    sysAdminIpGroup=sysAdminIpGroup,
    sysPvaStatClientBytesIn=sysPvaStatClientBytesIn,
    sysAuthStatWantcredentialResults=sysAuthStatWantcredentialResults,
    sysStpNumber=sysStpNumber,
    sysMultiHostTotal=sysMultiHostTotal,
    sysStatClientPktsIn=sysStatClientPktsIn,
    sysStpVlanMbrGroup=sysStpVlanMbrGroup,
    sysHttpStatAudioPostcompressBytes=sysHttpStatAudioPostcompressBytes,
    sysStatPvaClientPktsOut=sysStatPvaClientPktsOut,
    sysPvaStatServerMaxConns=sysPvaStatServerMaxConns,
    sysChassisFanNumber=sysChassisFanNumber,
    sysStatClientBytesIn5s=sysStatClientBytesIn5s,
    sysClientsslStatEncryptedBytesOut=sysClientsslStatEncryptedBytesOut,
    sysStatPvaClientPktsIn=sysStatPvaClientPktsIn,
    sysClusterMbrNumber=sysClusterMbrNumber,
    sysChassisFanIndex=sysChassisFanIndex,
    sysStatHardSyncookieGen=sysStatHardSyncookieGen,
    sysRouteStaticEntryNumber=sysRouteStaticEntryNumber,
    sysGlobalHostCpuIowait=sysGlobalHostCpuIowait,
    sysAttrConnAutoLasthop=sysAttrConnAutoLasthop,
    sysPlatformInfo=sysPlatformInfo,
    sysDot1dbaseStatPortIndex=sysDot1dbaseStatPortIndex,
    sysTmmStatClientMaxConns=sysTmmStatClientMaxConns,
    sysGlobalHostActiveCpuCount=sysGlobalHostActiveCpuCount,
    sysAttrFailoverIsRedundant=sysAttrFailoverIsRedundant,
    sysStpInterfaceTreeStatInstanceId=sysStpInterfaceTreeStatInstanceId,
    sysHttpStatPostcompressBytes=sysHttpStatPostcompressBytes,
    sysL2ForwardAttrVlan=sysL2ForwardAttrVlan,
    sysStpBridgeTreeStatNumber=sysStpBridgeTreeStatNumber,
    sysSctpStatRxcookie=sysSctpStatRxcookie,
    sysTmmStatTmmPid=sysTmmStatTmmPid,
    sysMultiHostCpuSoftirq5m=sysMultiHostCpuSoftirq5m,
    sysDot3StatSymbolErrors=sysDot3StatSymbolErrors,
    sysPacketFilterStat=sysPacketFilterStat,
    sysSelfIpAddrType=sysSelfIpAddrType,
    sysAttrFailoverUnitMask=sysAttrFailoverUnitMask,
    sysDot3StatExcessiveCollisions=sysDot3StatExcessiveCollisions,
    sysServersslStatTlsv1=sysServersslStatTlsv1,
    sysStpGlobalsFwdDelay=sysStpGlobalsFwdDelay,
    sysClusterDisabledParentType=sysClusterDisabledParentType,
    sysIcmpStatErrRtx=sysIcmpStatErrRtx,
    sysGlobalTmmStatLicenseDeny=sysGlobalTmmStatLicenseDeny,
    sysGlobalHostCpuUser5m=sysGlobalHostCpuUser5m,
    sysHostMemoryUsed=sysHostMemoryUsed,
    sysMultiHostCpuSystem=sysMultiHostCpuSystem,
    sysPvaStatClientTotConns=sysPvaStatClientTotConns,
    sysUdpStatExpires=sysUdpStatExpires,
    sysStpInterfaceTreeStatGroup=sysStpInterfaceTreeStatGroup,
    sysGlobalHostCpuNice1m=sysGlobalHostCpuNice1m,
    sysFastHttpStatClientSyns=sysFastHttpStatClientSyns,
    sysClientsslStatSessCacheInvalidations=sysClientsslStatSessCacheInvalidations,
    sysStpBridgeStatBridgeFwdDelay=sysStpBridgeStatBridgeFwdDelay,
    sysClusterMbrTable=sysClusterMbrTable,
    sysClientsslStatMidstreamRenegotiations=sysClientsslStatMidstreamRenegotiations,
    sysGlobalHostCpuNice=sysGlobalHostCpuNice,
    sysL2ForwardStatIfname=sysL2ForwardStatIfname,
    sysIfxStatOutBroadcastPkts=sysIfxStatOutBroadcastPkts,
    sysPacketFilterExpression=sysPacketFilterExpression,
    sysTrunkCfgMbrCount=sysTrunkCfgMbrCount,
    sysClientsslStatSessCacheCurEntries=sysClientsslStatSessCacheCurEntries,
    sysGlobalHostCpuUser1m=sysGlobalHostCpuUser1m,
    sysSubMemoryMaxAllocated=sysSubMemoryMaxAllocated,
    sysConnPoolStatMaxSize=sysConnPoolStatMaxSize,
    sysClusterMinUpMbrsEnable=sysClusterMinUpMbrsEnable,
    sysIfxStatResetStats=sysIfxStatResetStats,
    sysClusterNumber=sysClusterNumber,
    sysSystemName=sysSystemName,
    sysInterfaceTable=sysInterfaceTable,
    sysInterfaceStpEnable=sysInterfaceStpEnable,
    wa4500=wa4500,
    sysChassisTempIndex=sysChassisTempIndex,
    sysArpStaticEntryGroup=sysArpStaticEntryGroup,
    sysStpInterfaceTreeStatState=sysStpInterfaceTreeStatState,
    sysProxyExclusionVlangroupName=sysProxyExclusionVlangroupName,
    sysArpStaticEntryIpAddrType=sysArpStaticEntryIpAddrType,
    sysModuleAllocationName=sysModuleAllocationName,
    sysTrunkStat=sysTrunkStat,
    sysStatServerCurConns5s=sysStatServerCurConns5s,
    sysTmmStatTmIdleCycles=sysTmmStatTmIdleCycles,
    sysPacketFilterAction=sysPacketFilterAction,
    sysChassisFanSpeed=sysChassisFanSpeed,
    sysArpStaticEntry=sysArpStaticEntry,
    sysFastL4StatTxerrors=sysFastL4StatTxerrors,
    sysMultiHostCpuHostId=sysMultiHostCpuHostId,
    sysGeneral=sysGeneral,
    bigipPb100=bigipPb100,
    sysTcpStatFinWait=sysTcpStatFinWait,
    sysClusterLastPriSlotId=sysClusterLastPriSlotId,
    sysAuthStatGroup=sysAuthStatGroup,
    sysInterfaceMacAddr=sysInterfaceMacAddr,
    sysHostDiskTable=sysHostDiskTable,
    sysArpStaticEntryIpAddr=sysArpStaticEntryIpAddr,
    sysClientsslStatTotNativeConns=sysClientsslStatTotNativeConns,
    sysServersslStatSessCacheHits=sysServersslStatSessCacheHits,
    sysHttpStatRamcacheSize=sysHttpStatRamcacheSize,
    sysMultiHostCpuIdle5s=sysMultiHostCpuIdle5s,
    sysCpu=sysCpu,
    sysFastL4StatRxbadpkt=sysFastL4StatRxbadpkt,
    sysPacketFilterTable=sysPacketFilterTable,
    sysModuleAllocationNumber=sysModuleAllocationNumber,
    sysGlobalTmmStatTmSleepCycles=sysGlobalTmmStatTmSleepCycles,
    sysVlanGroup=sysVlanGroup,
    sysFastHttpStatV9Reqs=sysFastHttpStatV9Reqs,
    sysIcmp6StatForward=sysIcmp6StatForward,
    sysIpStatTxFragDropped=sysIpStatTxFragDropped,
    sysHostDiskBlockSize=sysHostDiskBlockSize,
    sysTrunkCfgMemberName=sysTrunkCfgMemberName,
    sysMultiHostCpuSystem5s=sysMultiHostCpuSystem5s,
    sysAttrFailoverStandbyLinkDownTime=sysAttrFailoverStandbyLinkDownTime,
    sysIcmp6StatErrProto=sysIcmp6StatErrProto,
    sysModuleAllocationGroup=sysModuleAllocationGroup,
    sysSctpStatResetStats=sysSctpStatResetStats,
    sysSwImageChksum=sysSwImageChksum,
    sysHttpStatSgmlPostcompressBytes=sysHttpStatSgmlPostcompressBytes,
    sysGlobalClientSslStat=sysGlobalClientSslStat,
    sysStpBridgeTreeStat=sysStpBridgeTreeStat,
    sysIfxStatAlias=sysIfxStatAlias,
    sysAttrFailoverUnitId=sysAttrFailoverUnitId,
    sysTcpStatExpires=sysTcpStatExpires,
    sysIfxStatOutMulticastPkts=sysIfxStatOutMulticastPkts,
    sysStatServerPktsOut1m=sysStatServerPktsOut1m,
    sysServersslStatDhRsaKeyxchg=sysServersslStatDhRsaKeyxchg,
    sysSystemStat=sysSystemStat,
    sysPacketFilterMacNumber=sysPacketFilterMacNumber,
    sysCpuNumber=sysCpuNumber,
    sysServersslStatDecryptedBytesIn=sysServersslStatDecryptedBytesIn,
    sysClusterEntry=sysClusterEntry,
    sysStatPvaServerBytesIn1m=sysStatPvaServerBytesIn1m,
    sysIpStatTx=sysIpStatTx,
    sysStatPvaClientPktsIn5m=sysStatPvaClientPktsIn5m,
    sysIfxStatNumber=sysIfxStatNumber,
    sysPvaStatClientBytesOut=sysPvaStatClientBytesOut,
    sysGlobalTmmStatTmUsageRatio1m=sysGlobalTmmStatTmUsageRatio1m,
    sysStatServerPktsOut=sysStatServerPktsOut,
    sysFastHttpStatGetReqs=sysFastHttpStatGetReqs,
    sysGlobalHostCpuSystem=sysGlobalHostCpuSystem,
    sysVlanGroupMbr=sysVlanGroupMbr,
    sysAdminIpNetmaskType=sysAdminIpNetmaskType,
    sysDot1dbaseStat=sysDot1dbaseStat,
    sysMultiHostCpuTable=sysMultiHostCpuTable,
    sysStatClientTotConns=sysStatClientTotConns,
    sysServersslStatIdeaBulk=sysServersslStatIdeaBulk,
    sysSwVolumeNumber=sysSwVolumeNumber,
    sysTcpStatResetStats=sysTcpStatResetStats,
    sysStatClientPktsIn5m=sysStatClientPktsIn5m,
    sysSelfPortDefault=sysSelfPortDefault,
    sysAdminIpAddrType=sysAdminIpAddrType,
    sysGlobalTmmStatGroup=sysGlobalTmmStatGroup,
    sysDot3StatSingleCollisionFrames=sysDot3StatSingleCollisionFrames,
    sysTcpStatConnects=sysTcpStatConnects,
    sysAdminIpNetmask=sysAdminIpNetmask,
    sysTrunkAggAddr=sysTrunkAggAddr,
    sysDot1dbaseStatPortDelayExceededDiscards=sysDot1dbaseStatPortDelayExceededDiscards,
    sysStatAuthWantcredentialResults=sysStatAuthWantcredentialResults,
    sysSelfPortAddr=sysSelfPortAddr,
    sysHttpStatXmlPrecompressBytes=sysHttpStatXmlPrecompressBytes,
    sysClientsslStatNonHwAcceleratedConns=sysClientsslStatNonHwAcceleratedConns,
    sysProxyExclusionIp=sysProxyExclusionIp,
    bigip8800=bigip8800,
    sysStpBridgeTreeStatLastTc=sysStpBridgeTreeStatLastTc,
    sysIpStatRx=sysIpStatRx,
    sysClientsslStatRsaKeyxchg=sysClientsslStatRsaKeyxchg,
    sysClientsslStatShaDigest=sysClientsslStatShaDigest,
    sysPacketFilterLog=sysPacketFilterLog,
    sysFastHttpStatResp4xxCnt=sysFastHttpStatResp4xxCnt,
    sysClusterAvailabilityState=sysClusterAvailabilityState,
    sysStpBridgeStatGroup=sysStpBridgeStatGroup,
    sysTmmStatConnectionMemoryErrors=sysTmmStatConnectionMemoryErrors,
    sysIcmpStatGroup=sysIcmpStatGroup,
    sysGlobalHostCpuUsageRatio1m=sysGlobalHostCpuUsageRatio1m,
)
