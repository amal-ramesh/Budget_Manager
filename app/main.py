from fastapi import FastAPI
from app.budget.budget_routes import budget_router


app = FastAPI()

app.include_router(budget_router)

@app.get("/")
async def root():
    return {"Message":"Starting page of BUDGET MANAGEMENT APPLICATION"}
