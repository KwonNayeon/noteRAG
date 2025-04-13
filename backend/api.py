from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import PyPDFLoader
from backend.rag_pipeline import generate_langchain_summary
import tempfile, os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # dev only; lock down in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/simplify_pdf")
async def simplify_pdf(file: UploadFile = File(...)):
    # 1) Read the uploaded PDF
    contents = await file.read()

    # 2) Write to a temp file so PyPDFLoader can read it
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # 3) Extract text from PDF
        loader = PyPDFLoader(tmp_path)
        docs = loader.load_and_split()
        text = "\n".join(doc.page_content for doc in docs)

        # 4) Generate summary (stubbed or real)
        try:
            summary_data = generate_langchain_summary(text)
        except Exception as e:
            print("Error in generate_langchain_summary:", e)
            raise HTTPException(
                status_code=503,
                detail="AI service unavailable. Please try again later."
            )

        # 5) Build one Summary object matching your Swift struct
        summary_obj = {
            "id":        1,
            "title":     summary_data["high_level"][0] if summary_data["high_level"] else "",
            "topic":     None,
            "keywords":  ["summary",
        "visual representation",
        "attention",
        "working memory",
        "cognitive load"],
            "lines":     summary_data["high_level"],
            "expanded":  summary_data["expanded"]
        }

        return {"summaries": [summary_obj]}

    finally:
        # 6) Clean up the temp file
        os.remove(tmp_path)
