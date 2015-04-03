import ssh
import time
from telnetlib import Telnet
from ftplib import FTP

class TelnetLogin():
    def __init__(self):
        self.__telnet=None
        self.__loginip='192.168.1.1'
        self.__user='root'
        self.__password='root123'
        self.__logintype=='telnet' #telnet or ssh
        
    def telnet_login(self):
        self.__telnet=Telnet(self.__loginip)
        out =self.__telnet.read_until('login: ')
        self.__telnet.write(self.__user+'\n')
        out=self.__telnet.read_until('Password: ')
        self.__telnet.write(self.__password+'\n')
        # out=self.__telnet.read_all()
        # print out
        time.sleep(5)
        print 'log succ!'
        
    def get_daily_build_package(self,ip,user,pwd,port,dirctory,filemark):

        pkgname=""
        try:
            versionftp = FTP()
            # FTP连接
            welcome = versionftp.connect(ip,int(port))
            print welcome
            resp = versionftp.login(user,pwd) 
            # 连接后切换目录
            versionftp.cwd(dirctory)
            # 根据名字查找当天构建的版本
            files = versionftp.nlst()
            
            for filename in files:
                print filename
                if filename.find(".zip") > 0:
                    pkgname=filename
                    print pkgname
                    break

            versionftp.quit()
       
            #下载当天构建的版本
            self.telnet_login()
            vp=self.__versionpath
            #delete old packages
            self.execute_command("bash -lc 'cd "+vp+";rm -rf "+pkgname+"'")
            self.execute_command("bash -lc 'cd "+vp+";rm -rf version.ftp'")
            self.execute_command("bash -lc 'cd "+vp+";echo \"open "+ip +" "+ str(port)+"\" >version.ftp'")
            self.execute_command("bash -lc 'cd "+vp+";echo \"user "+user + " " + pwd +"\" >>version.ftp'")
            self.execute_command("bash -lc 'cd "+vp+";echo \"bin\" >>version.ftp'")
            self.execute_command("bash -lc 'cd "+vp+";echo \"cd "+ dirctory +"\" >>version.ftp'")
            self.execute_command("bash -lc 'cd "+vp+";echo \"bin\" >>version.ftp'")
            self.execute_command("bash -lc 'cd "+vp+";echo \"get "+ pkgname +"\" >>version.ftp'")
            self.execute_command("bash -lc 'cd "+vp+";echo \"bye\" >>version.ftp'")
            self.execute_command("bash -lc 'cd "+vp+";ftp -i -in<version.ftp'")

            #解压版本
            print "start unzip file!"
            self.execute_command("bash -lc 'cd "+vp+";rm -rf zxommr;unzip -o "+pkgname+"'")
            versionpath='ftp://'+user+':'+pwd+'@'+ip+':'+port+'/'+dirctory+'/'+pkgname

            return versionpath
        except:
            raise
            print 'download_file from version server exception'
            return False
        finally:
            pass
            
    def execute_command(self,command):
        if self.__logintype=='ssh':
            pass
            transport=self.__sshclient.get_transport()
            if transport.is_active() and transport.is_authenticated():
                pass
                self._stdin, self._stdout, self._stderr = self.__sshclient.exec_command(command, 1024)
                print self._stdout.readlines()
                print self._stderr.readlines()

                out = self._stdout.readlines()
                err = self._stderr.readlines()
                if out!='' and out!=None:


                    #print 'no out!'
                    if len(out) > 6000:
                        print out[len(out)-6000:len(out)]
                    else :
                        print out
                    return out

                if err!='' and err!=None:

                    #print 'no err!'
                    '''print out'''
                    print err
                    return err

                    #print command
                    pass
                # print "command end out no print!"
                return ''
            else:
                print "not login,or connection is timeout!" 
        elif self.__logintype=='telnet':
            self.__telnet.write(command+'\n')
            
            #out=self.__telnet.read_until("~]")
            
            time.sleep(5)
            print self.__telnet.read_very_eager()
