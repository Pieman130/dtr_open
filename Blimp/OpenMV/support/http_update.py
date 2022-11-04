import http_get

def http_update():

    http_get.http_get("192.168.1.13","/","timer_test.py")
    http_get.http_get("192.168.1.13","/","http_dont.py")
