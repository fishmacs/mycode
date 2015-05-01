from socket import socket


def smtp_test(server, msg):
    sock = socket()
    # sock.connect((server_info[:cpos], int(server_info[cpos+1:])))
    sock.connect((server, 25))
    print sock.recv(256)
    sock.send("HELO yuhua.palmtao.com\n")
    print sock.recv(256)
    sock.send("MAIL from: wzhao@yuhua.palmtao.com\n")
    print sock.recv(256)
    sock.send("RCPT to: wzhao@palmtao.com\n")
    print sock.recv(256)
    sock.send("DATA\n")
    print sock.recv(256)
    sock.send(msg + "\n")
    sock.send(".\n")
    print sock.recv(256)
    sock.send("quit\n")
    sock.close
        

if __name__ == '__main__':
    smtp_test('172.17.42.1', 'test')
    