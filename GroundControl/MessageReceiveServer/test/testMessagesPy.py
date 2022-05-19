import urequests


def main() -> None:
   addr = '127.0.0.1'
   fullAddress = getFullAddress(addr, 'debug/status')
   print(fullAddress)
   data = {'stateID': 1, 'message':'test'}
   r = urequests.request('POST',fullAddress,data )
  # print(r.json())
    #   return r.json()

def getFullAddress(addr: str, api: str) -> str:
    return 'http://{}:4000/{}'.format(addr, api)

main()




