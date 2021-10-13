#!/bin/bash

run_dev() {
  export ENV="dev"
  uvicorn --port 5000 --host 127.0.0.1 main.main:app --reload
}

run_production() {
  export ENV="prod"
  gunicorn -w 3 -k uvicorn.workers.UvicornWorker main.main:app --reload
}

run_server_test() {
  export ENV="test"
  uvicorn --port 5000 --host 127.0.0.1 main.main:app --reload
}

run_tests() {
  export ENV="test"
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
  --run_server_test   init server to manual tests
  --run_tests         run automatic tests\n
"  ;;
esac
