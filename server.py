import asyncio as c  
import socket 



async def handle_client(conn: socket , loop : c.AbstractEventLoop , clients: list):
    while data := await loop.sock_recv(conn , 1024):
        [await loop.sock_sendall(client , data) for i in range (60000)  for client in clients if client != conn]
        
# telnet 127.0.0.1 8888
async def listen_for_new_connection(server_socket , loop : c.AbstractEventLoop ):
    clients = []
    while True : 
        conn , addr = await loop.sock_accept(server_socket)
        conn.setblocking(False)
        print(f"[*] We got connection from {addr}")
        clients.append(conn)
        c.create_task(handle_client(conn , loop , clients))

async def main ():
    server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
    server_addr = ('127.0.0.1' , 8888)
    server_socket.setblocking(False)
    server_socket.bind(server_addr)
    print(f"[*] Start listening on port 8888")
    server_socket.listen()

    local_loop = c.get_event_loop()
    await listen_for_new_connection(server_socket, local_loop)


c.run(main())
