# Sudoku Solver:v1

To run the plain vanilla Django version:
1. ```$ git clone https://github.com/psymbio/sudoku-solver-v1.git``` 
2. ```$ cd sudoku-solver-v1```
3. ```$ pip install -r requirements.txt```
4. ```$ python3 manage.py runserver```

To run the Docker container make sure you have Docker installed.
1. Rename Dockerfile to DeploymentDockerfile and ProductionDockerfile to Dockerfile.
2. ```$ docker build -t sudokusolver:v1 .```
3. ```$ docker run -it -p 8080:8080 sudokusolver:v1```