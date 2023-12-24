# Uncomment this to pass the first stage
import socket
import socket
import threading
import argparse
import os
def handle_client(client_socket):
    data = client_socket.recv(1024)
    if not data:
        pass
    lists = data.split(b"\r\n")[0].split(b" ")
    method = ""
    path = ""
    user_agent = ""
    contentBody = data.split(b"\r\n\r\n")[1]
    
    for i in data.split(b"\r\n"):
        if b"User-Agent" in i:
            user_agent = i.split(b"User-Agent: ")[1]
        if b"GET" in i:
            path = i.split(b"GET ")[1].split(b" HTTP")[0]
            method = i.split(b" ")[0]
        if b"POST" in i:
            path = i.split(b"POST ")[1].split(b" HTTP")[0]
            method = i.split(b" ")[0]
    
    
        
        

    if path == b"/":
        client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
    elif b"/echo" in path:
        content = lists[1].split(b"/echo/")[1]
        decoded = content.decode("utf-8")
        content_leng = f"Content-Length: {len(decoded)}\r\n\r\n".encode()
        client_socket.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n" + content_leng)
        client_socket.send(content)

    elif path ==  b"/user-agent":
        content = user_agent
        decoded = content.decode("utf-8")
        content_leng = f"Content-Length: {len(decoded)}\r\n\r\n".encode()
        client_socket.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n" + content_leng)
        client_socket.send(content)
    
    elif b"/files" in path and method == b"GET":
        file = path.split(b"/files/")[1]
        # Create the argument parser
        parser = argparse.ArgumentParser(description="Process a directory path.")

        # Add the --directory argument
        parser.add_argument('--directory', type=str, required=False,
                            help='the path to the directory')

        # Parse arguments
        args = parser.parse_args()

        # Access the directory argument
        directory = args.directory + "/"
        filePath = directory + file.decode()
        # Check if directory exists
        if os.path.isdir(directory):
            print(f"The directory '{directory + file.decode()}'  exist.")
        else:
            print(f"The directory '{directory}' does not exist.")
        

        if os.path.isfile(filePath):
            with open(filePath, "rb") as f:
                content = f.read()
                content_leng = f"Content-Length: {len(content)}\r\n\r\n".encode()
                client_socket.send(b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\n" + content_leng)
                client_socket.send(content)
        else:
            client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")

    elif b"/files" in path and method == b"POST":
        file = path.split(b"/files/")[1]
        # Create the argument parser
        parser = argparse.ArgumentParser(description="Process a directory path.")

        # Add the --directory argument
        parser.add_argument('--directory', type=str, required=False,
                            help='the path to the directory')

        # Parse arguments
        args = parser.parse_args()

        # Access the directory argument
        directory = args.directory + "/"
        filePath = directory + file.decode()   
        print("content body ======" +contentBody.decode())

       
        with open(filePath, "wb") as f:
            f.write(contentBody)
            content_leng = f"Content-Length: {len(contentBody)}\r\n\r\n".encode()
            client_socket.send(b"HTTP/1.1 201 OK\r\nContent-Type: application/octet-stream\r\n" + content_leng)
            client_socket.send(contentBody)
        # if os.path.isfile(filePath):
        #     # read the data from the client

        #     content = f.read()
        #     content_leng = f"Content-Length: {len(content)}\r\n\r\n".encode()
        #     client_socket.send(b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\n" + content_leng)
        #     client_socket.send(content)
        # else:
        #     client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")

    else:
        client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
    # for i in lists:
    #     print(i.decode("utf-8"))
    print(data.split(b"\r\n"))
    client_socket.close()



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
 

    


    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(5)
    # send HTTP/1.1 200 OK\r\n\r\n
    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


# input      
# python app/main.py --directory <directory>
# GET /files/<filename>



# output
# content-type: application/octet-stream
# Contentes of the file

# curl/7.64.1

# abc

if __name__ == "__main__":
    main()
