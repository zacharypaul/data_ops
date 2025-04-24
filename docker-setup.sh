#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Operations Dashboard Docker Setup${NC}\n"

# Function to check if docker is installed
check_docker() {
  if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker could not be found. Please install Docker first.${NC}"
    exit 1
  fi

  if ! command -v docker compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose could not be found. Please install Docker Compose first.${NC}"
    exit 1
  fi
}

# Function to build and start containers
start_app() {
  echo -e "${GREEN}Building and starting containers...${NC}"
  docker compose up --build -d
  echo -e "\n${GREEN}Application is now running!${NC}"
  echo -e "Frontend: http://localhost"
  echo -e "Backend API: http://localhost:8000"
  echo -e "API Documentation: http://localhost:8000/docs"
}

# Function to stop containers
stop_app() {
  echo -e "${GREEN}Stopping containers...${NC}"
  docker compose down
  echo -e "\n${GREEN}Application has been stopped.${NC}"
}

# Function to view logs
view_logs() {
  echo -e "${GREEN}Viewing logs (press Ctrl+C to exit)...${NC}\n"
  docker compose logs -f
}

# Function to restart containers
restart_app() {
  echo -e "${GREEN}Restarting containers...${NC}"
  docker compose restart
  echo -e "\n${GREEN}Application has been restarted.${NC}"
}

# Check if Docker is installed
check_docker

# Process command line arguments
case "$1" in
  start)
    start_app
    ;;
  stop)
    stop_app
    ;;
  restart)
    restart_app
    ;;
  logs)
    view_logs
    ;;
  *)
    echo -e "Usage: $0 {start|stop|restart|logs}"
    echo -e "  start    - Build and start the application"
    echo -e "  stop     - Stop the application"
    echo -e "  restart  - Restart the application"
    echo -e "  logs     - View application logs"
    exit 1
    ;;
esac

exit 0 