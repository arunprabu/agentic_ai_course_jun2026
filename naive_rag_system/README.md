Vector DB: Pgvector
Database Name: hr_rag_db
Credentials:
username: postgres
password: Pass@123

File to Ingest: data/HR_Support_Desk_KnowledgeBase.pdf

Chunking Strategy:
Chunk Size: 1000 characters (upto 1000 chars)
Chunk overlap: 200 characters (upto 200 chars)
Vector dimensions: default (1536)

Embedding Model: text-embedding-3-small from OpenAI
OpenAI Api key: in .env

===

python -m venv .venv
.venv\Scripts\activate.bat (win)

uv add python-dotenv

=====

# Missed

    1. fastapi endpoints
    2. create_agent of langchain

=====

## vectorization is not recommended for the following file types directly

===
.xls, .xlsx, .csv, .json, .html

for the above files preprocessing required.

- either enrich the files content to be plain text or clean up noise
