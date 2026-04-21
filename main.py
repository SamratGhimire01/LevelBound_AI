from fastapi import FastAPI
from auth.router import auth_router

app = FastAPI(description="Welcome to LevelBound AI.")
@app.get('/')
async def root():
    return {"message": "Welcome to LevelBound AI. Please use the /auth endpoint for authentication."}
app.include_router(auth_router,prefix='/auth')