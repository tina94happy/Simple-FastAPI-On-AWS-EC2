from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import boto3 
import json 


app = FastAPI()


s3 = boto3.resource("s3") # the object that will help you read data from S3 5 

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"message": "Welcome to this fantastic app!"}

@app.get("/users")
def get_users(request: Request):
    obj = s3.Object("put-your-bucket-name-here", "put-your-folder-and-data-here") # gets the file contents 
    body = obj.get()['Body'].read() # reads the file contents as a string 
    users_data = json.loads(body) # converts string into json 
    users = [
        {
            "name": user["name"],
            "phone": user["phone"],
            "fave_color": user["fave_color"],
        }
        for user in users_data.get("users", [])
    ]

    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/movies")
def get_movies(request: Request):
    """
    Fetch movies from movie_data.json and render an HTML page displaying titles, posters, and release dates.
    """
    obj = s3.Object("put-your-bucket-name-here", "put-your-folder-and-data-here")
    body = obj.get()['Body'].read() # reads the file contents as a string
    movies_data = json.loads(body) 
    # Parse the movie data
    movies = [
        {
            "title": movie["title"],
            "poster_url": f"https://image.tmdb.org/t/p/original{movie['poster_path']}",
            "release_date": movie.get("release_date", "N/A"),
        }
        for movie in movies_data.get("results", [])
        if movie.get("poster_path")  # Ensure a poster path exists
    ]

    return templates.TemplateResponse("index.html", {"request": request, "movies": movies})

