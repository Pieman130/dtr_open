import ftplib
import os
import supportDirectory
import time

server = '192.168.1.2'
username = ''
password = ''

s = supportDirectory.SupportDirectory()
myPath = s.getPath()
#myPath = 'c:\\Users\\timothy.woodbridge\\Desktop\\sillyTest\\'


myFTP = ftplib.FTP(server) #, username, password)

def uploadThis(path):
    files = os.listdir(path)
    os.chdir(path)


    for f in files:
        print(" files loop")
        if os.path.isfile(path + r'\{}'.format(f)):
            print("sending file:" + f)
            fh = open(f, 'rb')

            try:
                myFTP.storbinary('STOR %s' % f, fh)
                print("success. " + f)
            except Exception as err:                
                print("error. closing file:" + f)
                print(err)
            finally:
                fh.close()
        elif os.path.isdir(path + r'\{}'.format(f)):            
            if(f != '__pycache__'):
                print("sending directory")
                myFTP.mkd(f)
                myFTP.cwd(f)
                uploadThis(path + r'\{}'.format(f))
                myFTP.cwd('..')
                os.chdir('..')

uploadThis(myPath) # now call the recursive function 
time.sleep(3)
myFTP.quit()