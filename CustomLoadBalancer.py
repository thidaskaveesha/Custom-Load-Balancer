import socket
import threading

# Initialize your backend server address with actice connection as 0
servers = [
    {"address": ("127.0.0.1", 8081), "connections": 0},
    {"address": ("127.0.0.1", 8082), "connections": 0},
    {"address": ("127.0.0.1", 8083), "connections": 0},
]

# Lock for thread-safe updates to server connections
# Prevents race conditions when updating the 'connections' count
lock = threading.Lock()

# Round Robin index
# Keeps track of the current server index for Round Robin distribution
round_robin_index = 0

def round_robin():
    global round_robin_index
    with lock:
        # Select the server at the current index
        server = servers[round_robin_index]
        # Move to the next server
        round_robin_index = (round_robin_index + 1) % len(servers)
    return server

def least_connection():
    with lock:
        # Select the server with the minimum connections
        server = min(servers, key=lambda s: s["connections"])
    return server

def handle_client(client_socket):
    # Select a server using load balancing algorithm
    """
       If you want to use Round robin comment this and Call Round Robin 
       function here
    """ 
    server = least_connection()

    with lock:
        # Safely update the server's connection count
        server["connections"] += 1

    # Forward the client's request to the selected server
    try:
        # Create a new socket for backend communication
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the selected backend server
        backend_socket.connect(server["address"])
        # Start threads to forward data between the client and the backend server
        threading.Thread(target=forward, args=(client_socket, backend_socket)).start()
        threading.Thread(target=forward, args=(backend_socket, client_socket)).start()
    except Exception as e:
        print(f"Error connecting to server {server['address']}: {e}")
        client_socket.close()
        with lock:
            server["connections"] -= 1
    finally:
        with lock:
            server["connections"] -= 1

def forward(source, destination):
    try:
       # Read data from the source socket
        while data := source.recv(4096):
            destination.sendall(data)
    except:
        pass
    finally:
        source.close()
        destination.close()

def start_load_balancer():
    balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to all network interfaces on port 8000
    balancer_socket.bind(("0.0.0.0", 8000))
    balancer_socket.listen(5)
    print("Load Balancer is running on port 8000...")

    while True:
        client_socket, _ = balancer_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_load_balancer()
