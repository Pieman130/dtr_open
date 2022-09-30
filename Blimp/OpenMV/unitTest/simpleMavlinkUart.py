UART_BAUDRATE = 115200
UART_TIMEOUT = 1000
HW_UART = 3
import pyb
uart = pyb.UART(HW_UART)
uart.init(UART_BAUDRATE, timeout=UART_TIMEOUT, bits=8, parity=None, stop=1, flow=0) #, read_buf_len=64)
while(True):
    r = uart.readline()
    print(r)
