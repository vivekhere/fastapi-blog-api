from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from . import models
# from .database import engine
from .routes import user, post, auth, vote

# models.Base.metadata.create_all(bind=engine)
# We don't need it when we have alembic setup

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return "Blog API"
