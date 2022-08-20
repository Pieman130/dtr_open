def parse_mavlink(ser_msg):
    '''
    0th B = preamble (254)
    1st B = payload length
    2nd B = seq #
    3rd B = sys id
    4th B = Comp id
    5th B = Msg id (message type)
    6th - n B = payload
    n-2 = 1st byte chksum
    n-1 = 2nd byte chksum
    '''
    header = []
    try:
        for i in range(6):
            header.append(ser_msg[i])
        if ser_msg[0] != 254: #if inital byte not 254, it is misaligned message, ignore
            return None
        else:
            if ser_msg[5] == 132:
                payload = ser_msg[6:-2]
                dist = int.from_bytes(payload[8:10], "little")
                print("Range: ", dist)
                return (dist)
            else:
                return None
    except IndexError:
        return None


if __name__ == "__main__":
    msg = uart.readline()
        if a != None:
            dist = parse_mavlink(msg)
