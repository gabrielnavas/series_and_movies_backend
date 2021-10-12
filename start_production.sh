export ENV="prod"
gunicorn -w 3 -k uvicorn.workers.UvicornWorker main.main:app --reload
