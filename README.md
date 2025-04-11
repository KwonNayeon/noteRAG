# noteRAG

```
noterag/
├── backend/                  # FastAPI server + RAG processing
│   ├── api.py                # API routes
│   ├── rag_pipeline.py       # LangChain / RAG complete flow
│   └── utils.py              # chunking, embedding, etc.
│
├── frontend/                 # Streamlit or mobile (optional)
│   └── app.py or SwiftCode/  # UI code or iOS code collection
│
├── notebooks/
│   └── langchain_rag_template.ipynb  # Practice/test notebook
│
├── data/                     # Sample documents
│   └── sample.pdf
│
├── prompts/                  # Prompt templates
│   └── table_prompt.txt, etc
│
├── README.md
└── requirements.txt
```
