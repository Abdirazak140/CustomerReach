# Backend Setup

## Run a service:
DBService for example:
```bash
cd path/to/project
source venv/bin/activate
cd backend/
python3 ./DBService/main.py
```
## Run rabbitmq locally:

### Ubuntu:
```bash
sudo apt-get update
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server
```
See server status:
```bash
sudo systemctl status rabbitmq-server
```

### Windows:
1. Install Erlang from Erlang's official website.
2. Download and install RabbitMQ from RabbitMQ's official website.

```bash
rabbitmq-server.bat
```

