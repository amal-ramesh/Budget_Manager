from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"Message":"Starting page of BUDGET MANAGEMENT APPLICATION"}
