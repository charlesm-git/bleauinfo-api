from fastapi import FastAPI
from routers import areas, boulders, regions, users

app = FastAPI()

app.include_router(boulders.router)
app.include_router(areas.router)
app.include_router(regions.router)
app.include_router(users.router)