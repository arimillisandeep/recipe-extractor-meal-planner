from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, engine, Base
from .models import Recipe
from .schemas import URLInput
from .scraper import scrape_recipe
from .llm import run_llm


# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# ✅ CORS middleware (very important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database dependency
def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ------------------------
# Extract Recipe API
# ------------------------

@app.post("/extract")
def extract_recipe(
    input: URLInput,
    db: Session = Depends(get_db)
):

    url = input.url

    # Scrape text
    text = scrape_recipe(url)

    # Run LLM
    data = run_llm(text)

    title = data.get("title", "Unknown")
    cuisine = data.get("cuisine", "Unknown")
    difficulty = data.get("difficulty", "Unknown")

    # Save to database
    recipe = Recipe(
        url=url,
        title=title,
        cuisine=cuisine,
        difficulty=difficulty,
        data_json=data
    )

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return data


# ------------------------
# Get History
# ------------------------

@app.get("/history")
def get_history(
    db: Session = Depends(get_db)
):

    recipes = db.query(
        Recipe
    ).all()

    return recipes


# ------------------------
# Get Recipe by ID
# ------------------------

@app.get("/recipe/{id}")
def get_recipe(
    id: int,
    db: Session = Depends(get_db)
):

    recipe = db.query(
        Recipe
    ).filter(
        Recipe.id == id
    ).first()

    return recipe