from asyncio.subprocess import STDOUT
import subprocess
import socket
import os
import mimetypes
import threading
 



class HTTPServer:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        print("HTTP server instance created")
        print("host:" + self.host)
        print("port:", self.port)  


    def urlspliting(self,x):
        y=x.split(" ")
        recevied_url=y[1]
        k=recevied_url.split("/")
        # print("k[-1]",k[-1])
        return k[-1]



    def getpath(self,info):
        path11=os.getcwd()
        x1=(os.listdir(path11))[0]
        path1=os.path.join(path11,x1)
        # print("Path1",path1)
        filepath_of_www=os.path.join(path1,"www")
        files_in_www=os.listdir(filepath_of_www)
        # print("wwwfiles",files_in_www)
        filepath_of_bin=os.path.join(path1,"bin")
        files_in_bin=os.listdir(filepath_of_bin)
        # print("filesinbin",files_in_bin)
        if (info=="www") or (info in files_in_www):
            # print("return",[filepath_of_www,files_in_www])
            return [filepath_of_www,files_in_www,"www"]
        if (info=="bin") or (info in files_in_bin):
            # print("return", [filepath_of_bin ,files_in_bin])
            return [filepath_of_bin ,files_in_bin,"bin"]
        else:
            return ["404"]


    def testt(self,pathreq,c):
        process=subprocess.Popen(pathreq, shell=True, stdout=subprocess.PIPE)
        comm = process.communicate()[0]
        d=comm.decode()
        data= "HTTP/1.1 200 OK\nContent-Type: text/plain \n Content-Length: 1024\nConnection: Closed\n\n"
        data=data
        res=data+d
        ree=res.encode() 
        return c.sendall(ree) 



    def ls(self,c):
        res = os.popen('dir')
        read=res.read()
        data= "HTTP/1.1 200 OK\nContent-Type: text/plain \n Content-Length: 1024\nConnection: Closed\n\n"
        data=data
        res=data+read
        re=res.encode()
        return c.sendall(re)

    def du(self,c):
        res = os.popen('diskusage/?')
        read=res.read()
        data= "HTTP/1.1 200 OK\nContent-Type: text/plain \n Content-Length: 1024\nConnection: Closed\n\n"
        data=data
        res=data+read
        re=res.encode()
        return c.sendall(re)
    


    def displayingfilesindir(self,info,filename,c):
        head ='HTTP/1.1 200 OK \n Content-Type:text/html \n Content-Length:1024 \n Connection: close\n\n'
        for file in filename:
                    # print(file)
                    # print(os.path.join(info,file))
            head+=f'<a href= "{(os.path.join(info,file))}">{file}</a><br>'
        data=head.encode()
        return c.sendall(data)


    def to_access_files_in_www(self,complete_url,info,c):
        f=open(complete_url,'rb')
        result=f.read()
        f.close()
        res=f'HTTP/1.1 200 ok \n Content-Type={mimetypes.MimeTypes().guess_type(info)[0]}\n Content-Length:{len(str(result))}\n Connection:close\n\n'
        res=res.encode()
        res+=result
        return c.send(res)


    def gvn_url_isempty(self,c):
        data="<h1>Tiny Webserver under consturction</h1>"
        newLine='\n'
        message = "HTTP/1.1 200 OK"+newLine
        message+= "Content-Type: text/html"+newLine
        message+="Content-Lenght: " + str(len(data))+newLine
        message+="Connection: close"+newLine
        message+=newLine
        message+=data
        res=message.encode()
        return c.sendall(res)




    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host,self.port)
        print('starting up on %s port %s' %server_address)
        sock.bind(server_address)
        sock.listen(16)
        while True :
            print("Waiting for a connection")
            c, client_address = sock.accept()
            #print("connection from",client_address)
            process=threading.Thread(target=self.rResponse,args=(c,))
            process.start()
            process.join()
    


    def rResponse(self,c):

            data=c.recv(1024)
            x=data.decode()
            #print("initialdata",x)
            given_url=self.urlspliting(x)
            #print("info",given_url)

            if  (given_url==""):
                respns=self.gvn_url_isempty(c)
                c.close()

            path_fileslist=self.getpath(given_url)
           

            if (len(path_fileslist)<1) or path_fileslist[0]=="404":
                c.send("HTTP/1.1 404 not found".encode())
                c.close()

            path=path_fileslist[0]
            files_in_path=path_fileslist[1]
            filedirname=path_fileslist[2]

            
            if   (given_url in files_in_path) and (filedirname=="www") :
                complete_url=os.path.join(path,given_url)
                #print("completeurl",complete_url)
                os.path.isfile(complete_url)
                re=self.to_access_files_in_www(complete_url,given_url,c)
               

            elif (given_url in files_in_path) and (filedirname=="bin"):
                complete_url=os.path.join(path,given_url)
                os.path.isfile(complete_url)

                if (given_url=="ls"):
                    ress=self.ls(c)
                               
                if (given_url=="test.py"):
                    res=self.testt(complete_url,c)
                if (given_url=="du"):
                    ress=self.du(c)
 
            elif  (given_url=="bin") or (given_url=="www"):                
                  data=self.displayingfilesindir(given_url,files_in_path,c)
                                 
           
def main():
    server = HTTPServer('127.0.0.1', 8888)
    x=server.run()
if __name__ == "__main__":
    main()