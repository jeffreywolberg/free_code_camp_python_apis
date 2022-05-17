from os import stat
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from cryptography.fernet import Fernet
from .passwords.main import get_password

# -- SELECT * FROM products WHERE price > 40 ORDER BY created_at DESC LIMIT 4 OFFSET 2;
# -- INSERT INTO products (name, price, inventory) VALUES ('Ball', 30, 20), ('Computer', 1000, 40) returning id;
# -- SELECT * FROM products;
# -- DELETE FROM products WHERE id = 10 RETURNING *;
# -- SELECT * FROM products where id = 2;
# -- UPDATE products SET name = 'DVD players' WHERE id = 2 RETURNING *;

# uvicorn main:app --reload

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # optional with default value
    rating: Optional[int] = None  # optional without default value


password = get_password("app/passwords/key.key",
                        "app/passwords/encrypted_pass.txt")

try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                            password=password, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful!")
except Exception as error:
    print("Connecting to database failed")
    print("Error: " + error)
    exit()


my_posts = [{"title": "T", "content": "C", "id": 1}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello Wold"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return {"Post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id, ))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} could not be deleted")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.patch("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    sql_cmd = "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *"
    cursor.execute(sql_cmd, (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} could not be updated")
    conn.commit()
    return {"Data": post}

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