#
# Small ftp server for ESP8266 ans ESP32 Micropython
#
# from: https://github.com/robert-hh/FTP-Server-for-ESP8266-ESP32-and-PYBD/blob/master/ftp.py
# Based on the work of chrisgp - Christopher Popp and pfalcon - Paul Sokolovsky
#
# The server accepts passive mode only.
# It runs in foreground and quits, when it receives a quit command
# Start the server with:
#
# import ftp
#
# Copyright (c) 2016 Christopher Popp (initial ftp server framework)
# Copyright (c) 2016 Robert Hammelrath (putting the pieces together
# and a few extensions)
# Distributed under MIT License
#
import socket
import network
import uos
import gc


def send_list_data(path, dataclient, full):
    try:  # whether path is a directory name
        for fname in sorted(uos.listdir(path), key=str.lower):
            dataclient.send(make_description(path, fname, full))
    except:  # path may be a file name or pattern
        pattern = path.split("/")[-1]
        path = path[:-(len(pattern) + 1)]
        if path == "":
            path = "/"
        for fname in sorted(uos.listdir(path), key=str.lower):
            if fncmp(fname, pattern):
                dataclient.send(make_description(path, fname, full))


def make_description(path, fname, full):
    if full:
        stat = uos.stat(get_absolute_path(path, fname))
        file_permissions = ("drwxr-xr-x"
                            if (stat[0] & 0o170000 == 0o040000)
                            else "-rw-r--r--")
        file_size = stat[6]
        description = "{}    1 owner group {:>10} Jan 1 2000 {}\r\n".format(
                file_permissions, file_size, fname)
    else:
        description = fname + "\r\n"
    return description


def send_file_data(path, dataclient):
    with open(path, "rb") as file:
        chunk = file.read(512)
        while len(chunk) > 0:
            dataclient.send(chunk)
            chunk = file.read(512)


def save_file_data(path, dataclient):
    print('in save_file_data')
    with open(path, "wb") as file:
        print(path + " opened successfully.")
        keepGoing = 1
        chunk = 'test'
        while(keepGoing):
            try:
                chunk = dataclient.recv(1)
                #if(len(chunk)>0):
                 #   file.write(chunk)
            except:
                print("no more data")


       # chunk = dataclient.recv(512)
       # chunk = 'stuff'
       # print(chunk)
      #  totalBytes = 0        
      #  chunkLen = len(chunk)
      #  print('chunkLen: ' + str(chunkLen))
       # while (len(chunk) > 0 ):            
        #    print("in save file data while loop")
            #file.write(chunk) # no actual writing to file
         #   print("saved file data")
          #  totalBytes = totalBytes + len(chunk)            
          #  print("file write chunk succeeded")
           # try:
             #   chunk = dataclient.recv(512)     
             #   print("read chunk succeeded")
            #    print('chunkLen: ' + str(chunkLen))
            #except:        
             #   print("no more data to read")

            
        
        print("save file done") # + str(totalBytes))

        


def get_absolute_path(cwd, payload):
    # Just a few special cases "..", "." and ""
    # If payload start's with /, set cwd to /
    # and consider the remainder a relative path
    if payload.startswith('/'):
        cwd = "/"
    for token in payload.split("/"):
        if token == '..':
            if cwd != '/':
                cwd = '/'.join(cwd.split('/')[:-1])
                if cwd == '':
                    cwd = '/'
        elif token != '.' and token != '':
            if cwd == '/':
                cwd += token
            else:
                cwd = cwd + '/' + token
    return cwd


# compare fname against pattern. Pattern may contain
# wildcards ? and *.
def fncmp(fname, pattern):
    pi = 0
    si = 0
    while pi < len(pattern) and si < len(fname):
        if (fname[si] == pattern[pi]) or (pattern[pi] == '?'):
            si += 1
            pi += 1
        else:
            if pattern[pi] == '*':  # recurse
                if (pi + 1) == len(pattern):
                    return True
                while si < len(fname):
                    if fncmp(fname[si:], pattern[pi+1:]):
                        return True
                    else:
                        si += 1
                return False
            else:
                return False
    if pi == len(pattern.rstrip("*")) and si == len(fname):
        return True
    else:
        return False

def printCurrDir():
    test = uos.listdir(uos.getcwd())
    print("files in current dir:")
    for x in test:
        print(x)
def ftpserver(port=21, timeout=None,wlan=None):

    DATA_PORT = 13333

    ftpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    datasocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ftpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    datasocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ftpsocket.bind(socket.getaddrinfo("0.0.0.0", port)[0][4])
    datasocket.bind(socket.getaddrinfo("0.0.0.0", DATA_PORT)[0][4])

    ftpsocket.listen(1)
    ftpsocket.settimeout(timeout)
    datasocket.listen(1)
    datasocket.settimeout(None)

    msg_250_OK = '250 OK\r\n'
    msg_550_fail = '550 Failed\r\n'
    # check for an active interface, STA first
    #wlan = network.WLAN(network.STA_IF)
    if wlan.active():
        addr = wlan.ifconfig()[0]
    else:
        wlan = network.WLAN(network.AP_IF)
        if wlan.active():
            addr = wlan.ifconfig()[0]
        else:
            print("No active connection")
            return

    print("FTP Server started on ", addr)
    try:
        dataclient = None
        fromname = None
        do_run = True
        while do_run:
            print("do run!")
            cl, remote_addr = ftpsocket.accept()
            cl.settimeout(300)
            cwd = '/'
            try:
                # print("FTP connection from:", remote_addr)
                cl.send("220 Hello, this is the ESP8266/ESP32.\r\n")
                while True:
                    gc.collect()
                    data = cl.readline().decode("utf-8").rstrip("\r\n")
                    if len(data) <= 0:
                        print("Client disappeared")
                        do_run = False
                        break

                    command = data.split(" ")[0].upper()
                    payload = data[len(command):].lstrip()
                    
                    path = get_absolute_path(cwd, payload)                   


                    print("Command={}, Payload={}".format(command, payload))

                    if command == "USER":
                        cl.send("230 Logged in.\r\n")
                    elif command == "SYST":
                        cl.send("215 UNIX Type: L8\r\n")
                    elif command == "NOOP":
                        cl.send("200 OK\r\n")
                    elif command == "FEAT":
                        cl.send("211 no-features\r\n")
                    elif command == "PWD" or command == "XPWD":
                        cl.send('257 "{}"\r\n'.format(cwd))
                    elif command == "CWD" or command == "XCWD":
                        try:
                            files = uos.listdir(path)
                            cwd = path
                            cl.send(msg_250_OK)
                        except:
                            cl.send(msg_550_fail)
                    elif command == "CDUP":
                        cwd = get_absolute_path(cwd, "..")
                        cl.send(msg_250_OK)
                    elif command == "TYPE":
                        # probably should switch between binary and not
                        cl.send('200 Transfer mode set\r\n')
                    elif command == "SIZE":
                        try:
                            size = uos.stat(path)[6]
                            cl.send('213 {}\r\n'.format(size))
                        except:
                            cl.send(msg_550_fail)
                    elif command == "QUIT":
                        cl.send('221 Bye.\r\n')
                        do_run = False
                        break
                    elif command == "PASV":
                        cl.send('227 Entering Passive Mode ({},{},{}).\r\n'.
                                   format(addr.replace('.', ','), DATA_PORT >> 8,
                                          DATA_PORT % 256))
                        dataclient, data_addr = datasocket.accept()
                        print("FTP Data connection from:", data_addr)
                        DATA_PORT = 13333
                        active = False
                    elif command == "PORT":
                        items = payload.split(",")
                        if len(items) >= 6:
                            data_addr = '.'.join(items[:4])
                            # replace by command session addr
                            if data_addr == "127.0.1.1":
                                data_addr = remote_addr
                            DATA_PORT = int(items[4]) * 256 + int(items[5])
                            dataclient = socket.socket(socket.AF_INET,
                                                       socket.SOCK_STREAM)
                            dataclient.settimeout(10)
                            dataclient.connect((data_addr, DATA_PORT))
                            print("FTP Data connection with:", data_addr)
                            cl.send('200 OK\r\n')
                            active = True
                        else:
                            cl.send('504 Fail\r\n')
                    elif command == "LIST" or command == "NLST":
                        if not payload.startswith("-"):
                            place = path
                        else:
                            place = cwd
                        try:
                            cl.send("150 Here comes the directory listing.\r\n")
                            send_list_data(place, dataclient,
                                           command == "LIST" or payload == "-l")
                            cl.send("226 Listed.\r\n")
                        except:
                            cl.send(msg_550_fail)
                        if dataclient is not None:
                            dataclient.close()
                            dataclient = None
                    elif command == "RETR":
                        try:
                            cl.send("150 Opening data connection.\r\n")
                            send_file_data(path, dataclient)
                            cl.send("226 Transfer complete.\r\n")
                        except:
                            cl.send(msg_550_fail)
                        if dataclient is not None:
                            dataclient.close()
                            dataclient = None
                    elif command == "STOR":
                        try:
                            cl.send("150 Ok to send data.\r\n")
                            print("ready to save file to path: " + path)                                                
                            save_file_data(path, dataclient)
                            cl.send("226 Transfer complete.\r\n")
                            print("226 transfer complete.")                        
                        except Exception as err:
                            print('EXCEPTION 0')
                            print(err)
                            cl.send(msg_550_fail)
                        if dataclient is not None:                            
                            dataclient.close()
                            dataclient = None
                            print('STOR client finished without errors.')
                    elif command == "DELE":
                        try:
                            uos.remove(path)
                            cl.send(msg_250_OK)
                        except:
                            cl.send(msg_550_fail)
                    elif command == "RMD" or command == "XRMD":
                        try:
                            uos.rmdir(path)
                            cl.send(msg_250_OK)
                        except:
                            cl.send(msg_550_fail)
                    elif command == "MKD" or command == "XMKD":
                        try:
                            uos.mkdir(path)
                            cl.send(msg_250_OK)
                        except:
                            cl.send(msg_550_fail)
                    elif command == "RNFR":
                            fromname = path
                            cl.send("350 Rename from\r\n")
                    elif command == "RNTO":
                            if fromname is not None:
                                try:
                                    uos.rename(fromname, path)
                                    cl.send(msg_250_OK)
                                except:
                                    cl.send(msg_550_fail)
                            else:
                                cl.send(msg_550_fail)
                            fromname = None
                    elif command == "MDTM":
                        try:
                            tm=localtime(uos.stat(path)[8])
                            cl.send('213 {:04d}{:02d}{:02d}{:02d}{:02d}{:02d}\r\n'.format(*tm[0:6]))
                        except:
                            cl.send('550 Fail\r\n')
                    elif command == "STAT":
                        if payload == "":
                            cl.send("211-Connected to ({})\r\n"
                                       "    Data address ({})\r\n"
                                       "211 TYPE: Binary STRU: File MODE:"
                                       " Stream\r\n".format(
                                           remote_addr[0], addr))
                        else:
                            cl.send("213-Directory listing:\r\n")
                            send_list_data(path, cl, True)
                            cl.send("213 Done.\r\n")
                    else:
                        cl.send("502 Unsupported command.\r\n")
                        print("Unsupported command {} with payload {}".format(
                            command, payload))

            except Exception as err:
                print('EXCEPTION 1')
                print(err)
                printCurrDir()

            finally:
                cl.close()
                cl = None
    except Exception as e:
        print('EXCEPTION 2')
        print(e)
    finally:
        print('last finally')
        datasocket.close()
        ftpsocket.close()
        if dataclient is not None:
            print('close data client')
            dataclient.close()


# ftpserver()