#!/bin/bash

run_dev() {
  # sudo systemctl start docker && sudo docker-compose up -d
  export ENV="dev"
  export CREATE_LOG_DATABASE=true
  export LOG_ERROR_ON_CONSOLE=true
  uvicorn --port 5000 --host 127.0.0.1 main.main:app --reload
}

run_production() {
  export ENV="prod"
  export CREATE_LOG_DATABASE=true
  export LOG_ERROR_ON_CONSOLE=false
  gunicorn -w 3 -k uvicorn.workers.UvicornWorker main.main:app --reload
}

run_tests() {
  export ENV="test"
  export CREATE_LOG_DATABASE=true
  export LOG_ERROR_ON_CONSOLE=true
  export PYTHONPATH=. pytest
  clear && pytest
}


case $1 in
"--run_dev") run_dev ;;
"--run_production")  run_production ;;
"--run_server_test") run_server_test ;;
"--run_tests") run_tests ;;
*) printf "\n
  --help, -h          display this help and exit
  --run_dev           init development server 
  --run_production    init production server
  --run_tests         run automatic tests\n
"  ;;
esac
