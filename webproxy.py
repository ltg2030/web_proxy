import socket
import hashlib

BUF_SIZE = 10000

def A(Host, Port):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((Host, Port))
    s.listen(5)

    
    while True:
        conn, addr = s.accept()
        data = conn.recv(BUF_SIZE)
        split_data = data.split('\r\n')

        print '-----------------------------------------------------------------------------------------------------------------------'
        print 'http request :'
        print data

        if data == '':
            continue;
        
        host_domain = ''
        for msg in split_data:
            if 'Host: ' in msg:
                host_domain = msg[6:]
        print 'Host Domain : ' + host_domain

        if ':443' in data :
            conn.close()
        elif host_domain != '':
            print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print 'send request to real domain...'
            print 'Loading...'
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s2.connect((host_domain, 80))
            s2.send(data)
            while True:
                msg = s2.recv(BUF_SIZE)
                if len(msg)==0:
                    break
                print 'get response!!'
                print 'http response :'
                print msg
                conn.send(msg)
            print '-----------------------------------------------------------------------------------------------------------------------\n'
            s2.close()
            conn.close()
        else:
            conn.close()

            
def B1(Host, Port): # same length

    f = open('data_change_list.txt', 'rb')
    data_change = []

    while True:
        msg = f.readline()
        if len(msg)==0:
            break
        
        origin = msg.split()[0]
        change = msg.split()[1]
        if len(origin) == len(change):
            data_change.append((origin,change))

    f.close()

    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((Host, Port))
    s.listen(5)

    
    while True:
        conn, addr = s.accept()
        data = conn.recv(BUF_SIZE)
        split_data = data.split('\r\n')

        print '-----------------------------------------------------------------------------------------------------------------------'
        print 'http request :'
        print data

        if data == '':
            continue;
        
        host_domain = ''
        for msg in split_data:
            if 'Host: ' in msg:
                host_domain = msg[6:]
        print 'Host Domain : ' + host_domain

        if ':443' in data :
            conn.close()
        elif host_domain != '':
            print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print 'send request to real domain...'
            print 'Loading...'
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s2.connect((host_domain, 80))

            # for data changing, delete gzip in Accept-encoding on request packet
            data = data.replace('gzip', '    ')
            
            s2.send(data)
            while True:
                msg = s2.recv(BUF_SIZE)
                if len(msg)==0:
                    break
                print 'get response!!'
                print 'http response :'
                
                for iterator in data_change:
                    if iterator[0] in msg:
                        print iterator[0] + ' is founded !!'
                        msg=msg.replace(iterator[0], iterator[1])
                print msg
                
                conn.send(msg)
            print '-----------------------------------------------------------------------------------------------------------------------\n'
            s2.close()
            conn.close()
        else:
            conn.close()



def B2(Host, Port): # can change to different length

    f = open('data_change_list2.txt', 'rb')
    data_change = []

    while True:
        msg = f.readline()
        if len(msg)==0:
            break
        
        origin = msg.split()[0]
        change = msg.split()[1]
        data_change.append((origin,change))

    f.close()

    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((Host, Port))
    s.listen(5)

    
    while True:
        conn, addr = s.accept()
        data = conn.recv(BUF_SIZE)
        split_data = data.split('\r\n')

        print '-----------------------------------------------------------------------------------------------------------------------'
        print 'http request :'
        print data

        if data == '':
            continue;
        
        host_domain = ''
        for iter_data in split_data:
            if 'Host: ' in iter_data:
                host_domain = iter_data[6:]
        print 'Host Domain : ' + host_domain

        if ':443' in data :
            conn.close()
        elif host_domain != '':
            print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print 'send request to real domain...'
            print 'Loading...'
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s2.connect((host_domain, 80))

            # for data changing, delete gzip in Accept-encoding on request packet
            data = data.replace('gzip', '    ')
            
            s2.send(data)
            while True:
                msg = s2.recv(BUF_SIZE)
                if len(msg)==0:
                    break
                print 'get response!!'
                print 'http response :'
                
                # change only response including Content-Length header
                if 'Content-Length' in msg :
                    content_length_msg = ''
                    origin_content_length=0
                    split_msg = msg.split('\r\n')
                    for iter_msg in split_msg:
                        if 'Content-Length' in iter_msg:
                            origin_content_length_msg = iter_msg
                            origin_content_length = int(iter_msg[15:],10)
                            
                    origin_packet_length = len(msg)
                    
                    for iterator in data_change:
                        if iterator[0] in msg:
                            print iterator[0] + ' is founded !!'
                            msg=msg.replace(iterator[0], iterator[1])

                    changed_packet_length = len(msg)
                    changed_content_length = origin_content_length + (changed_packet_length - origin_packet_length)
                    changed_content_length_msg = "Content-Length: "+str(changed_content_length)

                    print "Content-Length Changed!!!"
                    print origin_content_length_msg,
                    print " -------> ",
                    print changed_content_length_msg
                    msg = msg.replace(origin_content_length_msg, changed_content_length_msg)
                    
                print msg
                
                conn.send(msg)
            print '-----------------------------------------------------------------------------------------------------------------------\n'
            s2.close()
            conn.close()
        else:
            conn.close()


def C1(Host, Port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((Host, Port))
    s.listen(5)

    cache_List = {}

    
    while True:
        conn, addr = s.accept()
        data = conn.recv(BUF_SIZE)
        split_data = data.split('\r\n')

        print '-----------------------------------------------------------------------------------------------------------------------'
        print 'http request :'
        print data

        if data == '':
            continue;
        
        host_domain = ''
        for msg in split_data:
            if 'Host: ' in msg:
                host_domain = msg[6:]
        print 'Host Domain : ' + host_domain
        
        check_get = split_data[0].split()[0]=='GET'
        url = split_data[0].split()[1]

        if url in cache_List.keys():
            print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print 'cached URL...'
            print 'Loading...'
            for iter_cache in cache_List[url]:
                print iter_cache
                conn.send(iter_cache)
            conn.close()
            print '-----------------------------------------------------------------------------------------------------------------------\n'
            continue
            
        if ':443' in data :
            conn.close()
        elif host_domain != '':
            print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print 'send request to real domain...'
            print 'Loading...'
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s2.connect((host_domain, 80))
            s2.send(data)

            cache_flag = True
            body_list = []
            
            while True:
                msg = s2.recv(BUF_SIZE)
                if len(msg)==0:
                    break
                
                print 'get response!!'
                print 'http response :'
                print msg

                if 'no-store' in msg:
                    cache_flag = False
                if 'no-cache' in msg:
                    cache_flag = False
                if 'must-revalidate' in msg:
                    cache_flag = False

                body_list.append(msg)
                conn.send(msg)

            if cache_flag and check_get:
                print 'this reponse is Cached !!!'
                cache_List[url] = body_list

            print '-----------------------------------------------------------------------------------------------------------------------\n'
            s2.close()
            conn.close()
        else:
            conn.close()

            
def C2(Host, Port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((Host, Port))
    s.listen(5)

    cache_List = []

    
    while True:
        conn, addr = s.accept()
        data = conn.recv(BUF_SIZE)
        split_data = data.split('\r\n')

        print '-----------------------------------------------------------------------------------------------------------------------'
        print 'http request :'
        print data

        if data == '':
            continue;

        host_domain = ''
        for msg in split_data:
            if 'Host: ' in msg:
                host_domain = msg[6:]
        print 'Host Domain : ' + host_domain
        
        check_get = split_data[0].split()[0]=='GET'
        url = split_data[0].split()[1]

        if hashlib.md5(url) in cache_List:
            print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print 'cached file...'
            print 'Loading...'

            # file send problem
            
            conn.close()
            print '-----------------------------------------------------------------------------------------------------------------------\n'
            continue
            
        if ':443' in data :
            conn.close()
        elif host_domain != '':
            print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            print 'send request to real domain...'
            print 'Loading...'
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s2.connect((host_domain, 80))
            s2.send(data)

            cache_flag = True
            check_zip = False
            file_data = ""
            
            while True:
                msg = s2.recv(BUF_SIZE)
                
                if len(msg)==0:
                    break
                
                if 'Content-Type: application/zip' in msg:
                    check_zip=True
                
                print 'get response!!'
                print 'http response :'
                print msg

                if 'no-store' in msg:
                    cache_flag = False
                if 'no-cache' in msg:
                    cache_flag = False
                if 'must-revalidate' in msg:
                    cache_flag = False

                file_data += msg
                conn.send(msg)

            
            if cache_flag and check_get and check_zip:
                print 'this file is Cached !!!'
                cache_List.append(hashlib.md5(url))
                file_data = file_data.split('\r\n\r\n')[1]
                fd = open(hashlib.md5(url).hexdigest()+'.tmp', 'wb')
                fd.write(file_data)
                fd.close()
                

            print '-----------------------------------------------------------------------------------------------------------------------\n'
            s2.close()
            conn.close()
        else:
            conn.close()
            


C2('127.0.0.1', 8080)
