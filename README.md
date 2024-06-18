# Readiness Probe PoC

This project is a proof of concept for implementing a readiness probe in a FastAPI application.  
The core functionality revolves around managing client connections and determining the readiness of the server to accept new requests based on the current load and predefined thresholds.

## Overview

Thuis minimal application uses FastAPI to expose several endpoints, with the primary focus on the `/ready` endpoint implemented in the `ready()` method within the `main.py` file.  
This endpoint serves as a readiness probe, indicating whether the server is prepared to handle additional client requests or if traffic should be redirected to other instances.

## Ready Method

The `ready()` method in [main.py](main.py) checks the server's current state and decides if it can accept more requests.  
The decision is based on the number of connected clients and the predefined constants `MIN_CLIENTS` and `MAX_CLIENTS`.

- **COOLDOWN Mode**: When the number of connected clients reaches `MAX_CLIENTS`, the server enters `COOLDOWN` mode, where it stops accepting new requests until the number of clients drops below `MIN_CLIENTS`.
- **Readiness Check**: The endpoint evaluates the server's readiness to handle additional long tasks. If the server is not in `COOLDOWN` mode and has not reached `MAX_CLIENTS`, it is considered ready to accept more requests.
- **Response**: The method returns a JSON response that includes the hostname (to test at scale), current number of clients, `COOLDOWN` mode status, and the `MIN_CLIENTS` and `MAX_CLIENTS` thresholds.  
The HTTP status code of the response indicates the readiness state of the server:
  - 200 (OK): The server is ready to accept more requests.
  - 503 (Service Unavailable): The server is not ready to accept more requests due to being in `COOLDOWN` mode or having reached the maximum number of clients.

The predefined constants `MIN_CLIENTS` and `MAX_CLIENTS` in the ready() method of main.py are set to:

- MIN_CLIENTS: 3
- MAX_CLIENTS: 4

## Setup and Running

You can run the application directly using fastapi CLI or Uvicorn if you have the required Python dependencies installed:

```sh
fastapi run main:app

uvicorn main:app
```

Refer to the [.vscode/launch.json](.vscode/launch.json) file for configuration details if you're using Visual Studio Code for development.

## Testing

To test the application with long tasks and several clients, make several requests to the `/long_task` endpoint to observe how the application handles concurrent long-running tasks and manages client connections, especially in relation to the `COOLDOWN` mechanism.

You can use multiple parallel tabs in Firefox and navigate to the <http://localhost:8000/long_task> to simulate multiple clients accessing the endpoint simultaneously.

> <ins>**/!\\**</ins> Be careful Chrome stalls requests in duplicate tabs making the long tasks sequential instead of parallel.

In another window, you can monitor the server's readiness by making requests to the `/ready` endpoint.  
Monitor the server's response and the number of connected clients to observe the `COOLDOWN` mechanism in action as well as the HTTP response code used to indicate the server's state to the readiness probe.

## Dependencies

All Python package dependencies are listed in the [requirements.txt](requirements.txt) file. Install them using pip:

```sh
pip install -r requirements.txt
```

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for more information.
