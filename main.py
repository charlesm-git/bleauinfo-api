from scipy.sparse import load_npz

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import RECOMMENDATION_MATRICES
from routers import (
    boulders,
    areas,
    regions,
    users,
    stats,
    search,
    recommendation,
)


@asynccontextmanager
async def matrix_load(app: FastAPI):
    RECOMMENDATION_MATRICES["ascents"] = load_npz("./similarity_ascent.npz")
    RECOMMENDATION_MATRICES["style"] = load_npz("./similarity_style.npz")
    RECOMMENDATION_MATRICES["grade"] = load_npz("./similarity_grade.npz")
    print("             Recommendation matrices loaded successfully.")
    yield
    RECOMMENDATION_MATRICES.clear()
    print("             Recommendation matrices memory cleared.")


app = FastAPI(lifespan=matrix_load)

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
