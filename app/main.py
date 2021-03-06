# -- SELECT * FROM products WHERE price > 40 ORDER BY created_at DESC LIMIT 4 OFFSET 2;
# -- INSERT INTO products (name, price, inventory) VALUES ('Ball', 30, 20), ('Computer', 1000, 40) returning id;
# -- SELECT * FROM products;
# -- DELETE FROM products WHERE id = 10 RETURNING *;
# -- SELECT * FROM products where id = 2;
# -- UPDATE products SET name = 'DVD players' WHERE id = 2 RETURNING *;

# uvicorn main:app --reload
# select posts.title, posts.id as post_id, COUNT(votes.post_id) as votes_count from posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id;

#JWT:
# Server creates a signature based on Server-API-password, header, and payload
# User will not be able to recreate a proper signature because he doesn't have
# the Server-API-password. The server can easily check if a signature is valid

# Don't run any alembic *revisions* on the prod server
# Only run them on the dev server, and then push them using git when they're done,
# Then run alembi

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .passwords.main import get_password
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# this creates a 'posts' table in postgres is none exists

# the line below creates the tables for you in case they aren't there
# however, this is limited, and will not change an already existing table
# even though it may have been updated. We use alembic for this. If we're using
# alembic, there is no need for this line and we can comment it out

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# origins = ["httpdds://www.google.com"]
origins = ["*"] # for any domain to be able to reach the API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# password = get_password("app/passwords/key.key",
#                         "app/passwords/encrypted_pass.txt")

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World!!"}


# 00:00:10 Intro
# 00:06:33 Project overview
# 00:11:23 Setting up (Venv at 00:22:20)
# 00:34:17 FastAPI basics (Postman at 00:54:00)
# 02:24:10 Databases and SQL (psycopg at 03:58:21, ORM at 04:31:18)
# 05:50:08 Adding usersddd
# 06:32:50 Authentication
# 07:42:44 Postman environments
# 07:50:33 Linking users to posts
# 08:38:30 Query parameters
# 08:53:53 Environment variables
# 09:21:20 Post voting framework
# 10:30:18 Alembic
# 11:14:28 CORS
# 11:23:38 Git
# 11:34:38 Deploying to Heroku
# 12:05:04 Deploying to a server (DigitalOcean)
# 13:04:42 SSL
# 13:20:05 Firewall
# 13:23:46 Push changes manually
# 13:26:08 Docker
# 14:14:49 Test framework
# 17:34:13 Automated CI/CD