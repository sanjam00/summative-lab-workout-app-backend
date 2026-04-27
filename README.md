# Workout Application Backend


## Overview

This project is a Flask-based REST API for managing workouts and exercises. It allows users to create workouts and exercises, and track details such as reps, sets, and duration through a join table.


## Project Structure

server/ 
│── app.py          # Main application & routes 
│── models.py       # Database models 
│── schemas.py      # Marshmallow schemas 
│── seed.py         # Seed data script 
│── migrations/     # Database migrations 
│── app.db


## Setup

### Clone the repo

git clone <https://github.com/sanjam00/summative-lab-workout-app-backend/blob/main/server/models.py>
cd <project-folder>

### Create and activate a virtual environment, install dependencies

pip install pipenv
pipenv install
pipenv shell

pip install flask flask-sqlalchemy flask-migrate marshmallow

### Initialize the database

flask db init
flask db migrate -m "initial migration"
flask db upgrade head

### Seed the database

python seed.py

### Run the server

python app.py

Server runs on:
http://127.0.0.1:5555


## Features

- CRUD for workouts and exercises
- Many-to-many relationship via a join table
- Nested serialization using Marshmallow
- Layered validation (schema, model, database)

### API Endpoints

Workouts
GET	        /workouts	          List all workouts
GET	        /workouts/<id>	    Get a single workout
POST	      /workouts	          Create a workout
DELETE	    /workouts/<id>	    Delete a workout

Exercises
GET	        /exercises	        List all exercises
GET	        /exercises/<id>	    Get a single exercise
POST	      /exercises	        Create an exercise
DELETE	    /exercises/<id>	    Delete an exercise

WorkoutExercises (Join Table)
POST        /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises      Add an exercise to a workout


## Future Improvements

- Add update (PATCH) endpoints
- Add user authentication
- Implement more exercise attributes (e.g., weight, difficulty, etc)
- Flesh out error handling with specific exceptions


## Author

Sanaeya James
Junior Developer

Built as a part of the SWE course assignment.