### Run Llama.cpp server (run on zeppelin)
## Lệnh xem các thông số:** *python -m llama_cpp.server --help*
from llama_cpp.server.app import create_app
import uvicorn
import nest_asyncio
import os
import asyncio

from llama_cpp.server.app import create_app
os.environ["MODEL"] = "models/Llama-3.1-MedPalm2-imitate-8B-Instruct.Q8_0.gguf"
os.environ["N_CTX"] = "16384"

app = create_app()

# Apply nest_asyncio to allow running async functions in an existing loop
nest_asyncio.apply()

# Running uvicorn inside an existing event loop
async def start_server():
    uvicorn.run(
        app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 7500)), log_config = None
    )

asyncio.run(start_server())