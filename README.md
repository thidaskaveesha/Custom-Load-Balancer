# Custom Load Balancer

## Introduction
This project is a custom load balancer implemented in Python. It uses socket programming and threading to distribute client requests among multiple backend servers. The load balancer supports the **Least Connection Algorithm** for efficient load distribution and can be extended to support other algorithms like Round Robin.

---

## Features
- **Dynamic Load Balancing**: Uses the Least Connection Algorithm to allocate requests dynamically to the backend server with the fewest active connections.
- **Thread-Safe Design**: Implements thread-safe updates to server connection counts using locks.
- **Simple Configuration**: Easy to set up with configurable backend server addresses.
- **Extensibility**: Supports adding additional load balancing algorithms.
- **Lightweight**: No external libraries required, only Python’s standard library.

---

## Prerequisites
- Python 3.7 or above
- Backend servers running on the specified ports (e.g., Flask, Django, Node.js, etc.)

---

## Setup and Usage

### Step 1: Clone the Repository
```bash
git clone https://github.com/thidaskaveesha/Custom-Load-Balancer.git
cd Custom-Load-Balancer
```

### Step 2: Configure Backend Servers
Update the `servers` list in the script to include the IP addresses and ports of your backend servers:
```python
servers = [
    {"address": ("127.0.0.1", 8081), "connections": 0},
    {"address": ("127.0.0.1", 8082), "connections": 0},
    {"address": ("127.0.0.1", 8083), "connections": 0},
]
```
Make sure your backend servers are running on these addresses.

### Step 3: Run the Load Balancer
Run the load balancer script:
```bash
python CustomLoadBalancer.py
```
The load balancer will start listening on port 8000 and distribute incoming requests to the backend servers.

### Step 4: Test the Load Balancer
Send HTTP requests to the load balancer:
```bash
curl http://localhost:8000
```
The requests will be distributed to the backend servers based on the Least Connection Algorithm.

---

## Algorithms
### Least Connection Algorithm (Default)
- Assigns the request to the backend server with the fewest active connections.
- Dynamically balances load based on real-time server state.

To switch to **Round Robin**, modify the `handle_client` function:
```python
server = round_robin()
```

---

## How It Works
1. The load balancer listens for incoming client requests on port 8000.
2. Each client request is forwarded to a backend server using the Least Connection Algorithm.
3. A separate thread is created to handle communication between the client and the backend server.
4. Connection counts are updated in a thread-safe manner to ensure accurate load balancing.

---

## Code Highlights
- **Thread-Safe Connection Updates**: Ensures no race conditions when updating the server connection counts using `threading.Lock`.
- **Forwarding Functionality**: Bidirectional data forwarding between client and backend server using threads.
- **Extensible Design**: Easy to add new load balancing algorithms.

---

## Limitations
- Not suitable for production environments without additional optimizations (e.g., health checks, SSL support).
- Limited scalability compared to dedicated load balancing solutions like NGINX or HAProxy.

---

## Future Improvements
- Add health checks to monitor backend server availability.
- Implement SSL/TLS for secure communication.
- Introduce logging for better debugging and monitoring.
- Add support for weighted load balancing.

---

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve this project.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgments
Special thanks to the open-source community for inspiration and guidance!

