# Sudoku Solver:v1

To run the plain vanilla Django version simply clone using: ```git clone https://github.com/psymbio/sudoku-solver-v1.git``` then cd to the project directory: ```cd sudoku-solver-v1``` and to run the program type: ```python3 manage.py runserver```

For requirements run: ```pip install -r requirements.txt```

To run the Docker container make sure you have Docker installed then build the Dockerfile: ```docker build -t sudokusolver:v1 .``` and run it using ```docker run -it -p 8080:8080 sudokusolver:v1```.