# Docker Compose on Demand

This is a tcp service to spwan docker compose instance on demand. It is mostly used for ctf purposes

## Requirements
- python3
- docker and docker compose 
- nodejs/bunjs(for solving pow)

## Configuration 

You can edit the configuration in config.py files to add the challenges, port range, host, etc

## usage

### Run 

Run the instancer using the : `python3 instancer.py`

### connect

Connect to the instancer using : `nc HOST PORT`
where `HOST` and   `PORT`  are specified in the config file

You will be promted to solve a PoW, using pow.js provided to solve.

Next you can select the challenges from the avialable challenges.


