import asyncio
import json
import socket

from uuid import uuid4
from fastapi import FastAPI, Depends, BackgroundTasks, Response

COOLDOWN: bool = False
MIN_CLIENTS: int = 3
MAX_CLIENTS: int = 4
MAX_THREADS: int = 5

LONG_TASK_DURATION: int = 10

HOSTNAME: str = socket.gethostname()

app = FastAPI()
clients: set[str] = set()


@app.get("/")
async def root() -> dict[str, str | int]:
    return {
        "clients": len(clients),
        "hostname": HOSTNAME,
    }


async def register_client(background_tasks: BackgroundTasks) -> str:
    """
    Register a client to the clients set and
    schedule the client to be unregistered after the request is done
    """
    client_id: str = str(uuid4())
    clients.add(client_id)

    background_tasks.add_task(unregister_client, client_id)

    return client_id


async def unregister_client(client_id: str) -> None:
    clients.remove(client_id)


@app.get("/long_task")
async def long_task(client_id: str = Depends(register_client)) -> dict[str, str]:
    """
    This endpoint is used to simulate a long task
    """
    await asyncio.sleep(LONG_TASK_DURATION)

    return {"client": client_id}


@app.get("/health")
async def health() -> Response:
    return Response(status_code=200)


@app.get("/ready")
async def ready() -> Response:
    """
    Check if the server is ready to accept requests
    if COOLDOWN is enabled, the server needs to wait for clients to go back to less than MIN_CLIENTS
    else the server is ready to accept requests until MAX_CLIENTS are connected then it will be in COOLDOWN mode
    """
    global COOLDOWN

    data: str = json.dumps(
        {
            "hostname": HOSTNAME,
            "clients": len(clients),
            "cooldown_mode": COOLDOWN,
            "MIN_CLIENTS": MIN_CLIENTS,
            "MAX_CLIENTS": MAX_CLIENTS,
        }
    )

    if COOLDOWN:
        if len(clients) >= MIN_CLIENTS:
            return Response(data, status_code=503)

        COOLDOWN = False
        return Response(data, status_code=200)

    if len(clients) >= MAX_CLIENTS:
        COOLDOWN = True
        return Response(data, status_code=503)

    return Response(data, status_code=200)
