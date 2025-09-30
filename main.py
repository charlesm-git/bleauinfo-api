from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    boulders,
    areas,
    regions,
    users,
    stats,
    search,
    recommendation,
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(boulders.router)
app.include_router(areas.router)
app.include_router(regions.router)
app.include_router(users.router)
app.include_router(stats.router)
app.include_router(search.router)
app.include_router(recommendation.router)
