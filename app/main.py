# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    # send HTTP/1.1 200 OK\r\n\r\n
    while True:
        data = conn.recv(1024)
        if not data:
            break
        lists = data.split(b"\r\n")[0].split(b" ")
        if lists[1] == b"/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        elif b"/echo" in lists[1]:
            content = lists[1].split(b"/echo/")[1]
            decoded = content.decode("utf-8")
            content_leng = f"Content-Length: {len(decoded)}\r\n\r\n".encode()
            conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n" + content_leng)
            conn.send(content)
            # conn.send(b"Content-Type: text/plain\r\n\r\n")
            # conn.send(content_leng.encode("utf-8"))
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        for i in lists:
            print(i.decode("utf-8"))
    conn.close()
        # print(data.split(b"\r\n").decode("utf-8"))
    # conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

# input      
# GET /echo/abc HTTP/1.1
# Host: localhost:4221
# User-Agent: curl/7.64.1

# output
# HTTP/1.1 200 OK
# Content-Type: text/plain
# Content-Length: 3

# abc

if __name__ == "__main__":
    main()
