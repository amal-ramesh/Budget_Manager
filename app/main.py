from fastapi import FastAPI
from app.budget.budget_routes import budget_router
from app.auth.auth_routes import auth_router


app = FastAPI()

app.include_router(budget_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"Message":"Starting page of BUDGET MANAGEMENT APPLICATION"}
