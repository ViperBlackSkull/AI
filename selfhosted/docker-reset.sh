#!/bin/bash

# Stop and remove containers from docker-compose
docker-compose down --remove-orphans 2>/dev/null

# Remove volumes created by docker-compose
docker-compose down -v 2>/dev/null

# Remove images used by docker-compose services
docker-compose down --rmi all 2>/dev/null

# Remove the custom network created by docker-compose
docker network rm selfhosted_webui_network 2>/dev/null

# Clean up any dangling resources
docker system prune -f