#
# PySNMP MIB module F5-BIGIP-COMMON-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/F5-BIGIP-COMMON-MIB
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
DisplayString, TextualConvention = mibBuilder.importSymbols(
    "SNMPv2-TC", "DisplayString", "TextualConvention"
)
f5 = ModuleIdentity((1, 3, 6, 1, 4, 1, 3375))
if mibBuilder.loadTexts:
    f5.setLastUpdated("200909141710Z")
if mibBuilder.loadTexts:
    f5.setOrganization("F5 Networks, Inc.")
bigipTrafficMgmt = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2))
bigipNotification = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 4))
bigipCompliance = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 5))
bigipNotifications = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0))
bigipNotifyObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 4, 1))
bigipCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 5, 1))
bigipGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2))
bigipNotificationGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 4))
bigipNotifyObjMsg = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 1, 1), DisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    bigipNotifyObjMsg.setStatus("current")
bigipNotifyObjNode = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 1, 2), DisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    bigipNotifyObjNode.setStatus("current")
bigipNotifyObjPort = MibScalar(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 1, 3), DisplayString()
).setMaxAccess("readonly")
if mibBuilder.loadTexts:
    bigipNotifyObjPort.setStatus("current")
bigipAgentStart = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 1))
if mibBuilder.loadTexts:
    bigipAgentStart.setStatus("current")
bigipAgentShutdown = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 2))
if mibBuilder.loadTexts:
    bigipAgentShutdown.setStatus("current")
bigipAgentRestart = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 3))
if mibBuilder.loadTexts:
    bigipAgentRestart.setStatus("current")
bigipCpuTempHigh = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 4)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipCpuTempHigh.setStatus("current")
bigipCpuFanSpeedLow = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 5)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipCpuFanSpeedLow.setStatus("current")
bigipCpuFanSpeedBad = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 6)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipCpuFanSpeedBad.setStatus("current")
bigipChassisTempHigh = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 7)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipChassisTempHigh.setStatus("current")
bigipChassisFanBad = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 8)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipChassisFanBad.setStatus("current")
bigipChassisPowerSupplyBad = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 9)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipChassisPowerSupplyBad.setStatus("current")
bigipServiceDown = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 10)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"),
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjNode"),
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjPort"),
)
if mibBuilder.loadTexts:
    bigipServiceDown.setStatus("current")
bigipServiceUp = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 11)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"),
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjNode"),
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjPort"),
)
if mibBuilder.loadTexts:
    bigipServiceUp.setStatus("current")
bigipNodeDown = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 12)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"),
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjNode"),
)
if mibBuilder.loadTexts:
    bigipNodeDown.setStatus("current")
bigipNodeUp = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 13)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"),
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjNode"),
)
if mibBuilder.loadTexts:
    bigipNodeUp.setStatus("current")
bigipStandby = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 14)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipStandby.setStatus("current")
bigipActive = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 15)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipActive.setStatus("current")
bigipActiveActive = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 16)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipActiveActive.setStatus("current")
bigipFeatureFailed = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 17)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipFeatureFailed.setStatus("current")
bigipFeatureOnline = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 18)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipFeatureOnline.setStatus("current")
bigipLicenseFailed = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 19)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipLicenseFailed.setStatus("current")
bigipLicenseExpired = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 20)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipLicenseExpired.setStatus("current")
bigipTamdAlert = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 21)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipTamdAlert.setStatus("current")
bigipAggrReaperStateChange = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 22)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipAggrReaperStateChange.setStatus("current")
bigipARPConflict = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 23)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipARPConflict.setStatus("current")
bigipNetLinkDown = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 24)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipNetLinkDown.setStatus("current")
bigipDiskPartitionWarn = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 25)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipDiskPartitionWarn.setStatus("current")
bigipDiskPartitionGrowth = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 26)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipDiskPartitionGrowth.setStatus("current")
bigipAuthFailed = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 27)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipAuthFailed.setStatus("current")
bigipConfigLoaded = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 28)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipConfigLoaded.setStatus("current")
bigipLogEmerg = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 29)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipLogEmerg.setStatus("current")
bigipLogAlert = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 30)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipLogAlert.setStatus("current")
bigipLogCrit = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 31)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipLogCrit.setStatus("current")
bigipLogErr = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 32)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipLogErr.setStatus("current")
bigipLogWarning = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 33)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipLogWarning.setStatus("current")
bigipPacketRejected = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 34)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipPacketRejected.setStatus("current")
bigipCompLimitExceeded = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 35)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipCompLimitExceeded.setStatus("current")
bigipSslLimitExceeded = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 36)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipSslLimitExceeded.setStatus("current")
bigipExternalLinkChange = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 37)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipExternalLinkChange.setStatus("current")
bigipAsmRequestBlocked = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 38)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipAsmRequestBlocked.setStatus("current")
bigipAsmRequestViolation = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 39)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipAsmRequestViolation.setStatus("current")
bigipGtmPoolAvail = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 40)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmPoolAvail.setStatus("current")
bigipGtmPoolNotAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 41)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmPoolNotAvail.setStatus("current")
bigipGtmPoolDisabled = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 42)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmPoolDisabled.setStatus("current")
bigipGtmPoolEnabled = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 43)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmPoolEnabled.setStatus("current")
bigipGtmLinkAvail = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 44)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmLinkAvail.setStatus("current")
bigipGtmLinkNotAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 45)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmLinkNotAvail.setStatus("current")
bigipGtmLinkDisabled = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 46)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmLinkDisabled.setStatus("current")
bigipGtmLinkEnabled = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 47)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmLinkEnabled.setStatus("current")
bigipGtmWideIpAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 48)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmWideIpAvail.setStatus("current")
bigipGtmWideIpNotAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 49)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmWideIpNotAvail.setStatus("current")
bigipGtmWideIpDisabled = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 50)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmWideIpDisabled.setStatus("current")
bigipGtmWideIpEnabled = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 51)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmWideIpEnabled.setStatus("current")
bigipGtmPoolMbrAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 52)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmPoolMbrAvail.setStatus("current")
bigipGtmPoolMbrNotAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 53)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmPoolMbrNotAvail.setStatus("current")
bigipGtmPoolMbrDisabled = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 54)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmPoolMbrDisabled.setStatus("current")
bigipGtmPoolMbrEnabled = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 55)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmPoolMbrEnabled.setStatus("current")
bigipGtmServerAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 56)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmServerAvail.setStatus("current")
bigipGtmServerNotAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 57)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmServerNotAvail.setStatus("current")
bigipGtmServerDisabled = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 58)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmServerDisabled.setStatus("current")
bigipGtmServerEnabled = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 59)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmServerEnabled.setStatus("current")
bigipGtmVsAvail = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 60)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmVsAvail.setStatus("current")
bigipGtmVsNotAvail = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 61)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmVsNotAvail.setStatus("current")
bigipGtmVsDisabled = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 62)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmVsDisabled.setStatus("current")
bigipGtmVsEnabled = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 63)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmVsEnabled.setStatus("current")
bigipGtmDcAvail = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 64)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmDcAvail.setStatus("current")
bigipGtmDcNotAvail = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 65)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmDcNotAvail.setStatus("current")
bigipGtmDcDisabled = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 66)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmDcDisabled.setStatus("current")
bigipGtmDcEnabled = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 67)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmDcEnabled.setStatus("current")
bigipHardDiskFailure = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 68)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipHardDiskFailure.setStatus("deprecated")
bigipGtmAppObjAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 69)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmAppObjAvail.setStatus("current")
bigipGtmAppObjNotAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 70)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmAppObjNotAvail.setStatus("current")
bigipGtmAppAvail = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 71)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmAppAvail.setStatus("current")
bigipGtmAppNotAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 72)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmAppNotAvail.setStatus("current")
bigipGtmJoinedGroup = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 73)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmJoinedGroup.setStatus("current")
bigipGtmLeftGroup = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 74)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmLeftGroup.setStatus("current")
bigipStandByFail = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 75)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipStandByFail.setStatus("current")
bigipInetPortExhaustion = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 76)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipInetPortExhaustion.setStatus("current")
bigipGtmBoxAvail = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 77)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipGtmBoxAvail.setStatus("current")
bigipGtmBoxNotAvail = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 78)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmBoxNotAvail.setStatus("current")
bigipAsmFtpRequestBlocked = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 79)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipAsmFtpRequestBlocked.setStatus("current")
bigipAsmFtpRequestViolation = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 80)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipAsmFtpRequestViolation.setStatus("current")
bigipGtmBig3dSslCertExpired = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 81)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmBig3dSslCertExpired.setStatus("current")
bigipGtmBig3dSslCertWillExpire = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 82)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmBig3dSslCertWillExpire.setStatus("current")
bigipGtmSslCertExpired = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 83)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmSslCertExpired.setStatus("current")
bigipGtmSslCertWillExpire = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 84)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmSslCertWillExpire.setStatus("current")
bigipAsmSmtpRequestBlocked = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 85)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipAsmSmtpRequestBlocked.setStatus("current")
bigipAsmSmtpRequestViolation = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 86)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipAsmSmtpRequestViolation.setStatus("current")
bigipBladeTempHigh = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 87)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipBladeTempHigh.setStatus("current")
bigipBladeNoPower = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 88)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipBladeNoPower.setStatus("current")
bigipClusterdNoResponse = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 89)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipClusterdNoResponse.setStatus("current")
bigipBladeOffline = NotificationType((1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 90)).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg")
)
if mibBuilder.loadTexts:
    bigipBladeOffline.setStatus("current")
bigipAsmDosAttackDetected = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 91)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipAsmDosAttackDetected.setStatus("current")
bigipAsmBruteForceAttackDetected = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 92)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipAsmBruteForceAttackDetected.setStatus("current")
bigipAomCpuTempTooHigh = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 93)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipAomCpuTempTooHigh.setStatus("current")
bigipGtmKeyGenerationRollover = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 94)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmKeyGenerationRollover.setStatus("current")
bigipGtmKeyGenerationExpiration = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 95)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipGtmKeyGenerationExpiration.setStatus("current")
bigipRaidDiskFailure = NotificationType(
    (1, 3, 6, 1, 4, 1, 3375, 2, 4, 0, 96)
).setObjects(("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"))
if mibBuilder.loadTexts:
    bigipRaidDiskFailure.setStatus("current")
bigipNotificationCompliance = ModuleCompliance(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 1, 4)
).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjectsGroup"),
    ("F5-BIGIP-COMMON-MIB", "bigipAgentNotifyGroup"),
)

if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    bigipNotificationCompliance = bigipNotificationCompliance.setStatus("current")
bigipNotifyObjectsGroup = ObjectGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 4, 1)
).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjMsg"),
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjNode"),
    ("F5-BIGIP-COMMON-MIB", "bigipNotifyObjPort"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    bigipNotifyObjectsGroup = bigipNotifyObjectsGroup.setStatus("current")
bigipAgentNotifyGroup = NotificationGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 4, 2)
).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipAgentStart"),
    ("F5-BIGIP-COMMON-MIB", "bigipAgentShutdown"),
    ("F5-BIGIP-COMMON-MIB", "bigipAgentRestart"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    bigipAgentNotifyGroup = bigipAgentNotifyGroup.setStatus("current")
bigipSystemNotifyGroup = NotificationGroup(
    (1, 3, 6, 1, 4, 1, 3375, 2, 5, 2, 4, 3)
).setObjects(
    ("F5-BIGIP-COMMON-MIB", "bigipCpuTempHigh"),
    ("F5-BIGIP-COMMON-MIB", "bigipCpuFanSpeedLow"),
    ("F5-BIGIP-COMMON-MIB", "bigipCpuFanSpeedBad"),
    ("F5-BIGIP-COMMON-MIB", "bigipChassisTempHigh"),
    ("F5-BIGIP-COMMON-MIB", "bigipChassisFanBad"),
    ("F5-BIGIP-COMMON-MIB", "bigipChassisPowerSupplyBad"),
    ("F5-BIGIP-COMMON-MIB", "bigipServiceDown"),
    ("F5-BIGIP-COMMON-MIB", "bigipServiceUp"),
    ("F5-BIGIP-COMMON-MIB", "bigipNodeDown"),
    ("F5-BIGIP-COMMON-MIB", "bigipNodeUp"),
    ("F5-BIGIP-COMMON-MIB", "bigipStandby"),
    ("F5-BIGIP-COMMON-MIB", "bigipActive"),
    ("F5-BIGIP-COMMON-MIB", "bigipActiveActive"),
    ("F5-BIGIP-COMMON-MIB", "bigipFeatureFailed"),
    ("F5-BIGIP-COMMON-MIB", "bigipFeatureOnline"),
    ("F5-BIGIP-COMMON-MIB", "bigipLicenseFailed"),
    ("F5-BIGIP-COMMON-MIB", "bigipLicenseExpired"),
    ("F5-BIGIP-COMMON-MIB", "bigipTamdAlert"),
    ("F5-BIGIP-COMMON-MIB", "bigipAggrReaperStateChange"),
    ("F5-BIGIP-COMMON-MIB", "bigipARPConflict"),
    ("F5-BIGIP-COMMON-MIB", "bigipNetLinkDown"),
    ("F5-BIGIP-COMMON-MIB", "bigipDiskPartitionWarn"),
    ("F5-BIGIP-COMMON-MIB", "bigipDiskPartitionGrowth"),
    ("F5-BIGIP-COMMON-MIB", "bigipAuthFailed"),
    ("F5-BIGIP-COMMON-MIB", "bigipConfigLoaded"),
    ("F5-BIGIP-COMMON-MIB", "bigipLogEmerg"),
    ("F5-BIGIP-COMMON-MIB", "bigipLogAlert"),
    ("F5-BIGIP-COMMON-MIB", "bigipLogCrit"),
    ("F5-BIGIP-COMMON-MIB", "bigipLogErr"),
    ("F5-BIGIP-COMMON-MIB", "bigipLogWarning"),
    ("F5-BIGIP-COMMON-MIB", "bigipPacketRejected"),
    ("F5-BIGIP-COMMON-MIB", "bigipCompLimitExceeded"),
    ("F5-BIGIP-COMMON-MIB", "bigipSslLimitExceeded"),
    ("F5-BIGIP-COMMON-MIB", "bigipExternalLinkChange"),
    ("F5-BIGIP-COMMON-MIB", "bigipAsmRequestBlocked"),
    ("F5-BIGIP-COMMON-MIB", "bigipAsmRequestViolation"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmPoolAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmPoolNotAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmPoolDisabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmPoolEnabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmLinkAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmLinkNotAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmLinkDisabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmLinkEnabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmWideIpAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmWideIpNotAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmWideIpDisabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmWideIpEnabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmPoolMbrAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmPoolMbrNotAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmPoolMbrDisabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmPoolMbrEnabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmServerAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmServerNotAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmServerDisabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmServerEnabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmVsAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmVsNotAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmVsDisabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmVsEnabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmDcAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmDcNotAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmDcDisabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmDcEnabled"),
    ("F5-BIGIP-COMMON-MIB", "bigipHardDiskFailure"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmAppObjAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmAppObjNotAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmAppAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmAppNotAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmJoinedGroup"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmLeftGroup"),
    ("F5-BIGIP-COMMON-MIB", "bigipStandByFail"),
    ("F5-BIGIP-COMMON-MIB", "bigipInetPortExhaustion"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmBoxAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmBoxNotAvail"),
    ("F5-BIGIP-COMMON-MIB", "bigipAsmFtpRequestBlocked"),
    ("F5-BIGIP-COMMON-MIB", "bigipAsmFtpRequestViolation"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmBig3dSslCertExpired"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmBig3dSslCertWillExpire"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmSslCertExpired"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmSslCertWillExpire"),
    ("F5-BIGIP-COMMON-MIB", "bigipAsmSmtpRequestBlocked"),
    ("F5-BIGIP-COMMON-MIB", "bigipAsmSmtpRequestViolation"),
    ("F5-BIGIP-COMMON-MIB", "bigipBladeTempHigh"),
    ("F5-BIGIP-COMMON-MIB", "bigipBladeNoPower"),
    ("F5-BIGIP-COMMON-MIB", "bigipClusterdNoResponse"),
    ("F5-BIGIP-COMMON-MIB", "bigipBladeOffline"),
    ("F5-BIGIP-COMMON-MIB", "bigipAsmDosAttackDetected"),
    ("F5-BIGIP-COMMON-MIB", "bigipAsmBruteForceAttackDetected"),
    ("F5-BIGIP-COMMON-MIB", "bigipAomCpuTempTooHigh"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmKeyGenerationRollover"),
    ("F5-BIGIP-COMMON-MIB", "bigipGtmKeyGenerationExpiration"),
    ("F5-BIGIP-COMMON-MIB", "bigipRaidDiskFailure"),
)
if getattr(mibBuilder, "version", (0, 0, 0)) > (4, 4, 0):
    bigipSystemNotifyGroup = bigipSystemNotifyGroup.setStatus("current")


class LongDisplayString(TextualConvention, OctetString):
    status = "current"
    displayHint = "1024a"
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 1024)


mibBuilder.exportSymbols(
    "F5-BIGIP-COMMON-MIB",
    bigipGtmDcEnabled=bigipGtmDcEnabled,
    bigipStandByFail=bigipStandByFail,
    PYSNMP_MODULE_ID=f5,
    bigipStandby=bigipStandby,
    bigipRaidDiskFailure=bigipRaidDiskFailure,
    bigipARPConflict=bigipARPConflict,
    bigipAsmRequestBlocked=bigipAsmRequestBlocked,
    bigipGtmPoolEnabled=bigipGtmPoolEnabled,
    bigipAomCpuTempTooHigh=bigipAomCpuTempTooHigh,
    bigipGtmPoolMbrNotAvail=bigipGtmPoolMbrNotAvail,
    bigipGtmLeftGroup=bigipGtmLeftGroup,
    bigipPacketRejected=bigipPacketRejected,
    bigipGtmVsNotAvail=bigipGtmVsNotAvail,
    bigipAsmSmtpRequestBlocked=bigipAsmSmtpRequestBlocked,
    bigipGtmServerNotAvail=bigipGtmServerNotAvail,
    bigipGtmLinkAvail=bigipGtmLinkAvail,
    bigipTrafficMgmt=bigipTrafficMgmt,
    bigipExternalLinkChange=bigipExternalLinkChange,
    bigipTamdAlert=bigipTamdAlert,
    bigipGtmPoolNotAvail=bigipGtmPoolNotAvail,
    bigipNotifyObjects=bigipNotifyObjects,
    bigipNodeUp=bigipNodeUp,
    bigipCpuFanSpeedBad=bigipCpuFanSpeedBad,
    bigipAsmFtpRequestBlocked=bigipAsmFtpRequestBlocked,
    bigipGtmKeyGenerationRollover=bigipGtmKeyGenerationRollover,
    bigipChassisFanBad=bigipChassisFanBad,
    bigipGtmAppAvail=bigipGtmAppAvail,
    bigipGtmLinkEnabled=bigipGtmLinkEnabled,
    bigipGtmServerDisabled=bigipGtmServerDisabled,
    bigipLogWarning=bigipLogWarning,
    bigipLogErr=bigipLogErr,
    bigipLogAlert=bigipLogAlert,
    bigipNotificationGroups=bigipNotificationGroups,
    bigipDiskPartitionGrowth=bigipDiskPartitionGrowth,
    bigipSystemNotifyGroup=bigipSystemNotifyGroup,
    bigipCpuTempHigh=bigipCpuTempHigh,
    bigipAgentShutdown=bigipAgentShutdown,
    bigipGtmBoxNotAvail=bigipGtmBoxNotAvail,
    bigipAsmRequestViolation=bigipAsmRequestViolation,
    bigipGtmSslCertWillExpire=bigipGtmSslCertWillExpire,
    bigipHardDiskFailure=bigipHardDiskFailure,
    bigipGtmVsAvail=bigipGtmVsAvail,
    bigipGtmVsDisabled=bigipGtmVsDisabled,
    bigipBladeTempHigh=bigipBladeTempHigh,
    bigipGtmWideIpAvail=bigipGtmWideIpAvail,
    bigipNotifyObjMsg=bigipNotifyObjMsg,
    bigipCpuFanSpeedLow=bigipCpuFanSpeedLow,
    bigipLogCrit=bigipLogCrit,
    bigipGtmDcNotAvail=bigipGtmDcNotAvail,
    bigipGtmWideIpDisabled=bigipGtmWideIpDisabled,
    bigipLicenseExpired=bigipLicenseExpired,
    bigipCompliances=bigipCompliances,
    bigipGtmPoolAvail=bigipGtmPoolAvail,
    bigipServiceDown=bigipServiceDown,
    bigipGtmWideIpNotAvail=bigipGtmWideIpNotAvail,
    bigipCompliance=bigipCompliance,
    bigipGtmServerEnabled=bigipGtmServerEnabled,
    bigipChassisPowerSupplyBad=bigipChassisPowerSupplyBad,
    bigipNotificationCompliance=bigipNotificationCompliance,
    bigipAsmBruteForceAttackDetected=bigipAsmBruteForceAttackDetected,
    bigipClusterdNoResponse=bigipClusterdNoResponse,
    bigipGroups=bigipGroups,
    bigipGtmWideIpEnabled=bigipGtmWideIpEnabled,
    bigipServiceUp=bigipServiceUp,
    bigipNotifyObjectsGroup=bigipNotifyObjectsGroup,
    bigipAgentNotifyGroup=bigipAgentNotifyGroup,
    bigipActive=bigipActive,
    bigipGtmAppObjNotAvail=bigipGtmAppObjNotAvail,
    bigipGtmBig3dSslCertExpired=bigipGtmBig3dSslCertExpired,
    bigipBladeOffline=bigipBladeOffline,
    bigipActiveActive=bigipActiveActive,
    bigipGtmJoinedGroup=bigipGtmJoinedGroup,
    bigipNotifyObjPort=bigipNotifyObjPort,
    bigipInetPortExhaustion=bigipInetPortExhaustion,
    bigipGtmVsEnabled=bigipGtmVsEnabled,
    bigipGtmBoxAvail=bigipGtmBoxAvail,
    bigipGtmKeyGenerationExpiration=bigipGtmKeyGenerationExpiration,
    bigipConfigLoaded=bigipConfigLoaded,
    bigipGtmPoolMbrAvail=bigipGtmPoolMbrAvail,
    bigipGtmLinkDisabled=bigipGtmLinkDisabled,
    bigipNotification=bigipNotification,
    bigipGtmPoolMbrEnabled=bigipGtmPoolMbrEnabled,
    bigipLogEmerg=bigipLogEmerg,
    bigipAgentRestart=bigipAgentRestart,
    bigipGtmDcDisabled=bigipGtmDcDisabled,
    bigipChassisTempHigh=bigipChassisTempHigh,
    bigipGtmLinkNotAvail=bigipGtmLinkNotAvail,
    bigipBladeNoPower=bigipBladeNoPower,
    bigipFeatureFailed=bigipFeatureFailed,
    bigipGtmPoolDisabled=bigipGtmPoolDisabled,
    bigipAsmDosAttackDetected=bigipAsmDosAttackDetected,
    bigipGtmBig3dSslCertWillExpire=bigipGtmBig3dSslCertWillExpire,
    bigipNotifyObjNode=bigipNotifyObjNode,
    bigipNodeDown=bigipNodeDown,
    bigipCompLimitExceeded=bigipCompLimitExceeded,
    bigipAggrReaperStateChange=bigipAggrReaperStateChange,
    bigipGtmPoolMbrDisabled=bigipGtmPoolMbrDisabled,
    bigipGtmDcAvail=bigipGtmDcAvail,
    f5=f5,
    bigipAuthFailed=bigipAuthFailed,
    bigipAsmSmtpRequestViolation=bigipAsmSmtpRequestViolation,
    bigipNetLinkDown=bigipNetLinkDown,
    bigipAgentStart=bigipAgentStart,
    bigipAsmFtpRequestViolation=bigipAsmFtpRequestViolation,
    bigipNotifications=bigipNotifications,
    bigipGtmAppNotAvail=bigipGtmAppNotAvail,
    bigipGtmSslCertExpired=bigipGtmSslCertExpired,
    bigipDiskPartitionWarn=bigipDiskPartitionWarn,
    bigipGtmServerAvail=bigipGtmServerAvail,
    bigipSslLimitExceeded=bigipSslLimitExceeded,
    bigipLicenseFailed=bigipLicenseFailed,
    LongDisplayString=LongDisplayString,
    bigipFeatureOnline=bigipFeatureOnline,
    bigipGtmAppObjAvail=bigipGtmAppObjAvail,
)
