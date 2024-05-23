from fastapi import FastAPI, Response, status, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schemas import Post
from app.database import set_up_database
import sqlite3


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

set_up_database()

@app.get("/")
def root():
    """Serve the index.html file."""
    return FileResponse('./static/index.html')


@app.get("/posts")
def get_posts():
    """Fetch and return all posts."""
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM posts").fetchall()
    posts = [{"id": row[0], "title": row[1], "content": row[2], "created_at": row[3]} for row in rows]
    cursor.close()
    conn.close()
    return {'data': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """Create a new post."""
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (post.title, post.content))
    conn.commit()
    cursor.close()
    conn.close()
    return {'Message': 'Post created successfully'}


@app.get("/posts/{id}")
def get_one_post(id: int, response: Response):
    """Fetch and return a post by ID."""
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    row = cursor.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    post = {"id": row[0], "title": row[1], "content": row[2], "created_at": row[3]}
    cursor.close()
    conn.close()
    return {"post_detail": post}


@app.patch("/posts/{id}")
def update_post(id: int, updated_post: Post):
    """Update a post by ID."""
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    row = cursor.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    cursor.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (updated_post.title, updated_post.content, id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"Message": "Post updated successfully"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """Delete a post by ID."""
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    row = cursor.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    row = cursor.execute('DELETE FROM posts WHERE id = ?', (id,)).fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)