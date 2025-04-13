from fastapi import FastAPI
from routers import areas, boulders, regions

app = FastAPI()

app.include_router(boulders.router)
app.include_router(areas.router)
app.include_router(regions.router)
