
import uvicorn
from fastapi import FastAPI
from api.v1.router import router as movie_router



app = FastAPI(
    version="1.0",
    title="API de Filmes e Series",
    description="API REST de Catálogo de Filmes/Séries (com autenticação)"
)

app.include_router(movie_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
