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
        path = ""
        user_agent = ""
        for i in data.split(b"\r\n"):
            if b"User-Agent" in i:
                user_agent = i.split(b"User-Agent: ")[1]
            if b"GET" in i:
                path = i.split(b"GET ")[1].split(b" HTTP")[0]

        if path == b"/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        elif b"/echo" in path:
            content = lists[1].split(b"/echo/")[1]
            decoded = content.decode("utf-8")
            content_leng = f"Content-Length: {len(decoded)}\r\n\r\n".encode()
            conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n" + content_leng)
            conn.send(content)
            # conn.send(b"Content-Type: text/plain\r\n\r\n")
            # conn.send(content_leng.encode("utf-8"))
        elif path ==  b"/user-agent":
            content = user_agent
            decoded = content.decode("utf-8")
            content_leng = f"Content-Length: {len(decoded)}\r\n\r\n".encode()
            conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n" + content_leng)
            conn.send(content)
           
            # content = 
            # decoded = content.decode("utf-8")
            # content_leng = f"Content-Length: {len(decoded)}\r\n\r\n".encode()
            # conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n" + content_leng)
            # conn.send(content)

        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        # for i in lists:
        #     print(i.decode("utf-8"))
        print(data.split(b"\r\n"))
    conn.close()
        # print(data.split(b"\r\n").decode("utf-8"))
    # conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

# input      
# GET /user-agent HTTP/1.1
# Host: localhost:4221
# User-Agent: curl/7.64.1

# output
# HTTP/1.1 200 OK
# Content-Type: text/plain
# Content-Length: 11

# curl/7.64.1

# abc

if __name__ == "__main__":
    main()
