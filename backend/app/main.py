from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from api import routes

app = FastAPI()

origins = [
    "http://localhost:5173",  # Adjust this to the URL of your frontend app
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(routes.router)
