import socket
import threading
import sys
import time

# A dictionary to hold the network addresses of all other nodes
NODES = {
    'node1': ('node1', 10000),
    'node2': ('node2', 10000),
    'node3': ('node3', 10000),
}

# This function will run in a separate thread to listen for incoming messages
def listen_for_messages(my_hostname, my_port):
    """
    Creates a server socket to listen for messages from other nodes.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind to all interfaces to avoid hostname resolution/bind issues inside containers
        s.bind(("0.0.0.0", my_port))
        s.listen()
        print(f"[{my_hostname}] Listening for connections on port {my_port}")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    print(f"\n[{my_hostname}] Message received: {data.decode()}\n> ", end="")

# This is the main function where the user can send messages
def main():
    if len(sys.argv) < 2:
        print("Usage: python node.py <node_name>")
        sys.exit(1)
        
    my_name = sys.argv[1]
    if my_name not in NODES:
        print(f"Error: Node name '{my_name}' not recognized.")
        sys.exit(1)

    my_host, my_port = NODES[my_name]

    # Start the listening thread
    listener_thread = threading.Thread(target=listen_for_messages, args=(my_host, my_port), daemon=True)
    listener_thread.start()

    print(f"--- Welcome to {my_name} ---")
    print("Commands: send <node_name> <message>")
    print("Example: send node2 Hello there!")
    
    # Give the server thread a moment to start up
    time.sleep(1)

    # Main loop for sending messages
    while True:
        try:
            command = input("> ")
            parts = command.split()
            
            if len(parts) >= 3 and parts[0] == 'send':
                dest_name = parts[1]
                message = " ".join(parts[2:])
                
                if dest_name in NODES:
                    dest_host, dest_port = NODES[dest_name]
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((dest_host, dest_port))
                            s.sendall(message.encode())
                        print(f"[{my_name}] Message sent to {dest_name}.")
                    except ConnectionRefusedError:
                        print(f"[{my_name}] Error: Connection to {dest_name} was refused.")
                else:
                    print(f"[{my_name}] Error: Node '{dest_name}' not found.")
            else:
                print(f"[{my_name}] Invalid command. Format: send <node_name> <message>")

        except KeyboardInterrupt:
            print(f"\nShutting down {my_name}...")
            break

if __name__ == "__main__":
    main()