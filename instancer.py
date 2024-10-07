import socket
import threading
from utils import *
import os
from config import *



# Handle client connection
def handle_client(conn):
    try:

        conn.sendall(b"Welcome to the docker compose as a service.\n")
        if check_max_challenges():
            conn.sendall(b"Maximum number of challenges reached. Please try again after some time.\n")
            return
        
        # Generate PoW challenge
        challenge = generate_challenge()
        conn.sendall(f"POW Challenge: {challenge}\n".encode())
        
        # Receive the solution from the client
        conn.sendall(b"Please solve the PoW by providing a solution (nonce).\n")
        conn.sendall(b"Solution sha256(challenge + solution) should start with" + str(DIFFICULTY).encode() + b" zeros.\n")
        solution = conn.recv(1024).decode().strip()
        # Validate the PoW
        if validate_pow(challenge, solution, DIFFICULTY):
            conn.sendall(b"PoW validated successfully.\n")

            # Display the available challenges in the format: 1. Challenge_1 and ask the user to select one
            conn.sendall(b"Available challenges:\n")
            for i, chall_name in enumerate(CHALLS.keys()):
                conn.sendall(f"{i+1}. {chall_name}\n".encode())
            conn.sendall(b"Select a challenge by entering the number: ")
            chall_index = int(conn.recv(1024).decode().strip()) - 1
            chall_name = list(CHALLS.keys())[chall_index]
            
            # Get a random port and update Docker Compose
            random_ports = [get_random_port() for _ in range(len(CHALLS[chall_name]["services"]))]
            chall_dir = update_docker_compose(chall_name,random_ports.copy())
            start_challenge(chall_dir)

            timer = threading.Timer(TIMEOUT, stop_challenge, args=(chall_dir,))
            timer.start()

            
            # Send the service URL back to the client
            service_url = '\n'.join(f"{CHALL_HOST}:{port}" for port in random_ports)
            conn.sendall(f"Services available at: {service_url}\n".encode())
        
        else:
            conn.sendall(b"PoW validation failed. Goodbye.\n")
    
    except Exception as e:
        conn.sendall(f"Error: {str(e)}\n".encode())
    finally:
        conn.close()

# TCP Socket Server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    # check if challs is not empty
    if not CHALLS:
        print("No challenges found. Exiting.")
        exit(1)
    start_server()
