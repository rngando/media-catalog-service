
import uvicorn, os
from fastapi import FastAPI
from api.v1.router import router as movie_router



app = FastAPI(
    version="1.0",
    title="API de Filmes e Series",
    description="API REST de Catálogo de Filmes/Séries (com autenticação)"
)

app.include_router(movie_router)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    uvicorn.run(app, host="0.0.0.0", port=8000)
# find . -type d -name "__pycache__" -exec rm -rf {} +
# media-catalog-service
