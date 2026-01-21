from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import yaml

app = FastAPI()

templates = Jinja2Templates(directory='templates')

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    procedure: str
    category: str

def slugify_dish_name(name: str) -> str:
    return "_".join(name.lower().split())

def clean_procedure(procedure: str):
    procedure_list = []
    for step in procedure.split("-"):
        print(step)
        procedure_list.append(step)
    print(procedure_list)

def create_recipe_file(recipe):
    recipe_name = slugify_dish_name(recipe.name) + '.yaml'
    recipe.procedure = clean_procedure(recipe.procedure)
    current_files_in_folder = len([l for l in os.scandir(recipe.category)])
    recipe_file = str(current_files_in_folder + 1) + '_' + recipe_name
    with open(recipe.category + "/" + recipe_file, "w") as file:
        yaml.dump(recipe.dict(), file, sort_keys=False)
        
@app.post("/recipe")
def save_recipe(recipe: Recipe):
    create_file = create_recipe_file(recipe)
    return {"status": "saved"}