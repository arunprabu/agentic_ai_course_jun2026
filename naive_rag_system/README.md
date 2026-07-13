Vector DB: Pgvector
Database Name: hr_rag_db
Credentials:
username: postgres
password: Pass@123

File to Ingest: data/HR_Support_Desk_KnowledgeBase.pdf

Chunking Strategy:
Chunk Size: 1000 characters
Chunk overlap: 200 characters
Vector dimensions: default (1536)

Embedding Model: text-embedding-3-small from OpenAI
OpenAI Api key: in .env

===

python -m venv .venv
.venv\Scripts\activate.bat (win)

uv add python-dotenv
