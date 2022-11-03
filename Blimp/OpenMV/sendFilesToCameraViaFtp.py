import ftplib
import os
import supportDirectory

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
            print("sending file")
            fh = open(f, 'rb')
            myFTP.storbinary('STOR %s' % f, fh)
            fh.close()
        elif os.path.isdir(path + r'\{}'.format(f)):
            print("sending directory")
            myFTP.mkd(f)
            myFTP.cwd(f)
            uploadThis(path + r'\{}'.format(f))
            myFTP.cwd('..')
            os.chdir('..')

uploadThis(myPath) # now call the recursive function 
myFTP.quit()