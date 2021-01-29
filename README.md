# Sudoku Solver:v1

To run the plain vanilla Django version:
```$ git clone https://github.com/psymbio/sudoku-solver-v1.git``` 
```$ cd sudoku-solver-v1```
```$ pip install -r requirements.txt```
```$ python3 manage.py runserver```

To run the Docker container make sure you have Docker installed
```$ docker build -t sudokusolver:v1 .```
```$ docker run -it -p 8080:8080 sudokusolver:v1```