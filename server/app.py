from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define routes here

# workout routes
@app.route('/workouts')
def get_workouts():
  workouts = Workout.query.all()
  schema = WorkoutSchema(many=True)

  return make_response(schema.dump(workouts), 200)

@app.route('/workouts/<int:id>')
def get_workout_by_id(id):
  workout = Workout.query.get(id)

  if not workout:
    return make_response({"error": "Workout not found"}, 404)

  schema = WorkoutSchema()

  return make_response(schema.dump(workout), 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
  try:
    schema = WorkoutSchema()
    data = schema.load(request.json)

    new_workout = Workout(**data)

    db.session.add(new_workout)
    db.session.commit()

    return make_response(schema.dump(new_workout), 201)

  except Exception as e:
    return make_response({"error": str(e)}, 400)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
  workout = Workout.query.get(id)

  if not workout:
    return make_response({"error": "Not found"}, 404)

  db.session.delete(workout)
  db.session.commit()

  return make_response({}, 204)

# exercise routes
@app.route('/exercises')
def get_exercises():
  exercises = Exercise.query.all()
  schema = ExerciseSchema(many=True)

  return make_response(schema.dump(exercises), 200)

@app.route('/exercises/<int:id>')
def get_exercise_by_id(id):
  exercise = Exercise.query.get(id)

  if not exercise:
    return make_response({"error": "Exercise not found"}, 404)

  schema = ExerciseSchema()

  return make_response(schema.dump(exercise), 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
  try:
    schema = ExerciseSchema()
    data = schema.load(request.json)

    new_exercise = Exercise(**data)

    db.session.add(new_exercise)
    db.session.commit()

    return make_response(schema.dump(new_exercise), 201)

  except Exception as e:
    return make_response({"error": str(e)}, 400)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
  exercise = Exercise.query.get(id)

  if not exercise:
    return make_response({"error": "Not found"}, 404)

  db.session.delete(exercise)
  db.session.commit()

  return make_response({}, 204)

# join table route
# add an exercise to a workout
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_workout_exercise(workout_id, exercise_id):
  try:
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
      return make_response({"error": "Workout or Exercise not found"}, 404)

    schema = WorkoutExercisesSchema()

    data = schema.load(request.json)

    new_entry = WorkoutExercises(
      workout=workout,
      exercise=exercise,
      **data
    )

    db.session.add(new_entry)
    db.session.commit()

    return make_response(schema.dump(new_entry), 201)

  except Exception as e:
    return make_response({"error": str(e)}, 400)


if __name__ == '__main__':
  app.run(port=5555, debug=True)