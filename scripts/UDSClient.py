from scapy.all import *
import time


def sendUDSPacketandPrint(msg):
    # Create a message
    p = Ether(dst='02:00:00:00:00:00', type=2048) / IP(ihl=5, src=srcaddress, dst=destaddress) / msg

    # Send the message
    if __name__ == '__main__':
        sendp(p, iface=eth, count=1)
    else:
        sendp(p, iface=eth, count=1, verbose=False)

    # Wait for response
    r = sniff(filter='host 192.168.0.10', iface=eth, count=1)

    # Format the response to be visible as hex value
    packet = r[0]
    raw = packet.lastlayer()
    if __name__ == '__main__':
        hexdump(raw)

    return bytes(raw)


def fprintTimefromHex(secs):
    s = secs % 60
    m = secs/60
    h = m/60

    print('{:02d}:{:02d}:{:02d}'.format(int(h), int(m), int(s)))


def printStopWatchTime(payload):
    print("Time: {0}:{1}:{2}:{3}".format(payload[StopWatchTimeOffset], payload[StopWatchTimeOffset+1],
                                         payload[StopWatchTimeOffset+2], payload[StopWatchTimeOffset+3]*10))


def int_from_bytes(input):
    return int.from_bytes(input[3:5], byteorder='big', signed=True)


def RCStopwatchStop(ID):
    return RoutineControlSID + StopWatchStop + StopWatchRoutine + StopWatchID[ID]


def RCStopwatchSend(ID):
    return RoutineControlSID + StopWatchSend + StopWatchRoutine + StopWatchID[ID]


# Addresses of microcontroller and PC
destaddress = '192.168.0.10'
srcaddress = '192.168.0.11'

# Name of network interface card
eth = 'Realtek PCIe GBE Family Controller'

# Service SIDs
TesterPresentSID = b'\x3E'
ECUResetSID = b'\x11'

ReadDataByIdentifierSID = b'\x22'
TimeFromStartupDID = b'\x01\x05'

RoutineControlSID = b'\x31'
StopWatchRoutine = b'\x13\x01'
StopWatchStart = b'\x01'
RCStopwatchStart = RoutineControlSID + StopWatchStart + StopWatchRoutine
StopWatchStop = b'\x02'
StopWatchSend = b'\x03'
StopWatchTimeOffset = 5
StopWatchID = [b'\x00', b'\x01', b'\x02', b'\x03',
               b'\x04', b'\x05', b'\x06', b'\x07',
               b'\x08', b'\x09', b'\x0A', b'\x0B',
               b'\x0C', b'\x0D', b'\x0E', b'\x0F', b'\x10']

# Other SIDs
DiagnosticSessionControlSID = b'\x10'
TesterPresentInvalidSID = b'\x3E\xFF\xFF'
ECUResetInvalidSID = b'\x11\x3E'
InvalidDID = b'\x01\x06'
InvalidRoutineSubfunc = b'\x04'
InvalidStopWatchID = b'\x11'

# Response SIDs
TesterPresentRPSID = b'\x7E\x3E'
DiagnosticSessionControlRPSID = b'\x7E\x50'
ECUResetRPSID = b'\x51\x11'
StopWatchStartRP = b'\x71\x01\x13\x01'
StopWatchStopRP = b'\x71\x02\x13\x01'
StopWatchSendRP = b'\x71\x03\x13\x01'

TesterPresentInvalidRPSID = b'\x7F\x3E\x13'
ECUResetInvalidRPSID = b'\x7F\x11\x13'
InvalidRPDID = b'\x7F\x22\x13'
RoutineControlIncMsgLenOrInvFormatRPSID = b'\x7F\x31\x13'
RoutineControlSeqErrorRPSID = b'\x7F\x31\x24'
RoutineControlSubfuncNotSupportedRPSID = b'\x7F\x31\x12'
RoutineControlServiceNotSupportedRPSID = b'\x7F\x31\x11'

# Test different SIDs
if __name__ == '__main__':
    sendUDSPacketandPrint(TesterPresentSID)
    sendUDSPacketandPrint(DiagnosticSessionControlSID)
    sendUDSPacketandPrint(TesterPresentInvalidSID)

    sendUDSPacketandPrint(ECUResetInvalidSID)
    sendUDSPacketandPrint(ECUResetSID)

    # Wait a few seconds after reset then use Tester Present service
    time.sleep(5)
    sendUDSPacketandPrint(TesterPresentSID)

    # Print formatted time
    fprintTimefromHex(int_from_bytes(sendUDSPacketandPrint(ReadDataByIdentifierSID + TimeFromStartupDID)))
    time.sleep(1)
    fprintTimefromHex(int_from_bytes(sendUDSPacketandPrint(ReadDataByIdentifierSID + TimeFromStartupDID)))
    sendUDSPacketandPrint(ReadDataByIdentifierSID + InvalidDID)

    for i in range(18):
        sendUDSPacketandPrint(RCStopwatchStart)

    sendUDSPacketandPrint(RCStopwatchStop(10))
    sendUDSPacketandPrint(RCStopwatchStop(1))
    sendUDSPacketandPrint(RCStopwatchSend(1))

    sendUDSPacketandPrint(RCStopwatchStart)
    sendUDSPacketandPrint(RCStopwatchStart)

