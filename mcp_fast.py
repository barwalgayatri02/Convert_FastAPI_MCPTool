from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP


# -------------------- FASTAPI --------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

'''
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your actual origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
'''

@app.get("/add")
def add(a: int, b: int):
    return a + b


@app.get("/subtract")
def subtract(a: int, b: int):
    return a - b


@app.get("/multiply")
def multiply(a: int, b: int):
    return a * b


@app.get("/divide")
def divide(a: int, b: int):
    return a / b


# -------------------- MCP (EXPOSE FASTAPI ROUTES) --------------------

mcp = FastMCP("math-mcp")

# expose ONLY selected FastAPI routes as MCP tools
mcp.mount(
    app,
    include=[
        "/add",
        "/subtract",
    ],
)

# mount MCP server on same FastAPI app
app.mount("/mcp", mcp.app)
