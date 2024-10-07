## Configuration ##

HOST = '0.0.0.0'            # Listen on all interfaces
PORT = 65432                # Port for the TCP server
PORT_RANGE = (49152, 65535) # Range of ports to select from
COMPOSE_DIR = "challenges"  # Directory to store the docker-compose.yml files
DIFFICULTY = 4              # Difficulty for PoW (number of leading zeros in hash)
CHALL_HOST = "localhost"    # Host for the challenge service                            
CHALLS = {                  # store the challenges and their path to source code where the docker compose is present
    "challenge1": {
        "source" : "PATH_TO_CHALLENGE1", 
        "services": [
                        { 
                            "name":"kafka-ui",
                            "port": 8080
                        },
                    ]
        },
}

TIMEOUT = 60                # Timeout for the challenge
MAX_CHALLENGES = 5          # Maximum number of challenges that can be started at a time