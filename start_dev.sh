export ENV="dev"
uvicorn --port 5000 --host 127.0.0.1 main.main:app --reload