import hashlib
import subprocess
import yaml
import os
import random
import string
import socket
import shutil
from config import *

def copy_files(source_dir, destination_dir):
    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)
    
    # Iterate through each file in the source directory
    for filename in os.listdir(source_dir):
        # Create full file path
        source_file = os.path.join(source_dir, filename)
        
        # Check if it's a file (ignore directories)
        if os.path.isfile(source_file):
            # Copy file to the destination directory
            shutil.copy(source_file, destination_dir)
            print(f"Copied: {source_file} to {destination_dir}")


def generate_challenge(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Proof of Work validation
def validate_pow(challenge, solution, difficulty):
    combined = challenge + solution
    hash_result = hashlib.sha256(combined.encode()).hexdigest()
    return hash_result.startswith('0' * difficulty)

# Get a random available port within the specified range from the config
def get_random_port():
    # Get a random port within the specified range, using while loop to ensure it's available
    while True:
        port = random.randint(PORT_RANGE[0], PORT_RANGE[1])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((HOST, port)) != 0:
                return port
            
# Function to check if maxium number of challenges reached
def check_max_challenges():
    return len(os.listdir(COMPOSE_DIR)) >= MAX_CHALLENGES

def create_unique_compose_dir():
    unique_dir = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    compose_dir = f'{COMPOSE_DIR}/{unique_dir}'
    os.makedirs(compose_dir, exist_ok=True)
    return compose_dir

# Update docker-compose.yml with the selected port
def update_docker_compose(chall_name, ports):
    # take source and port from CHALLS
    chall_path = CHALLS[chall_name]["source"]
    services = CHALLS[chall_name]["services"]
    
    # create a new directory for the challenge and storing the docker-compose.yml
    compose_dir = create_unique_compose_dir()
    copy_files(chall_path, compose_dir)
    with open(f'{compose_dir}/docker-compose.yml', 'r+') as file:
        compose_content = yaml.safe_load(file)
        for s in services:
            service = s['name']
            chall_port = s['port']
            port = ports.pop()
            compose_content['services'][service]['ports'] = [f"{port}:{chall_port}"]
        file.seek(0)
        yaml.dump(compose_content, file)
        file.truncate()
    
    return compose_dir

# Start Docker Compose
def start_challenge(chall_dir):
    subprocess.Popen(['docker-compose', 'up'], cwd=chall_dir)

def stop_challenge(chall_dir):
    # Run the docker-compose down command and wait for it to complete
    subprocess.run(['docker-compose', 'down'], cwd=chall_dir, check=True)
    
    # Remove the directory after docker-compose stops
    shutil.rmtree(chall_dir)  # Use rmtree to remove a directory and its contents
    print(f"Removed: {chall_dir}")
    


