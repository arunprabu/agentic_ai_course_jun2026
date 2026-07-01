mkdir langchain_examples
cd langchain_examples

uv init

python -m venv .venv
source .venv/bin/activate (mac)
.venv\Scripts\activate.bat (win)

uv add python-dotenv langchain langchain-openai

======
keep the openai api key in .env
====

# load the .env in your example
