from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.rag import build_or_load_index, grounded_answer

app = FastAPI(title="Resume QA Bot", version="1.0.0")

# Allow CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Load / Build Index on Startup ----
RESUME_PATH = "data/resume.pdf"
index = build_or_load_index(RESUME_PATH, force_rebuild=False)

# ---- Request Schema ----
class QueryRequest(BaseModel):
    query: str

# ---- Endpoint ----
@app.post("/ask")
async def ask_question(request: QueryRequest):
    user_query = request.query
    answer = grounded_answer(index, user_query)
    return {"query": user_query, "response": answer}
