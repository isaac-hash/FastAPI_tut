from fastapi import FastAPI, Request, HTTPException,status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app =FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



posts: list[dict] = [
    {
        "id": 1,
        "author": "Alice Johnson",
        "title": "Getting Started with FastAPI",
        "content": "FastAPI is a modern, fast web framework for building APIs with Python.",
        "date_posted": "April 21, 2009",
    },
    {
        "id": 2,
        "author": "Bob Smith",
        "title": "Understanding Python Type Hints",
        "content": "Type hints help with autocompletion and data validation using Pydantic.",
        "date_posted": "April 10, 2008",
    },
    {
        "id": 3,
        "author": "Charlie Davis",
        "title": "Deploying Modern APIs",
        "content": "Learn how to containerize and deploy your web services effortlessly.",
        "date_posted": "April 16, 2007",
    },
]


# @app.get("/", response_class=HTMLResponse, include_in_schema=False)
# @app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    # return {"message": "Hello world"}
    # return f"<h1>{posts[0]['title']}</h1>"
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})


@app.get("/posts/{post_id}", include_in_schema=False, name="post_page")
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]  # Limit title to 50 characters
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/api/posts")
def get_posts():
    return posts

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")