from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define models here
class Exercise(db.Model):
  __tablename__ = 'exercises'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  category = db.Column(db.String)
  equipment_needed = db.Column(db.Boolean)

  workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise')

  # ensure name exists and is at least 2 characters
  @validates('name')
  def validate_name(self, key, value):
    if not value or len(value.strip()) < 2:
      raise ValueError("Exercise name must be at least 2 characters")
    return value

class Workout(db.Model):
  __tablename__ = 'workouts'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  duration_minutes = db.Column(db.Integer)
  notes = db.Column(db.Text)

  workout_exercises = db.relationship('WorkoutExercises', back_populates='workout')

  # workout duration must be positive
  __table_args__ = (
      db.CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

class WorkoutExercises(db.Model):
  __tablename__ = 'workout_exercises'

  id = db.Column(db.Integer, primary_key=True)
  reps = db.Column(db.Integer)
  sets = db.Column(db.Integer)
  duration_seconds = db.Column(db.Integer)

  workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

  workout = db.relationship('Workout', back_populates='workout_exercises')
  exercise = db.relationship('Exercise', back_populates='workout_exercises')

  # ensure reps, sets, and duration are present and positive numbers 
  @validates('reps', 'sets', 'duration_seconds')
  def validate_values(self, key, value):
    if value is not None and value < 0:
      raise ValueError(f"{key} must be non-negative")

    # check presence AFTER assignment logic
    temp_reps = value if key == 'reps' else self.reps
    temp_sets = value if key == 'sets' else self.sets
    temp_duration = value if key == 'duration_seconds' else self.duration_seconds

    if not any([temp_reps, temp_sets, temp_duration]):
      raise ValueError("At least one of reps, sets, or duration must be provided")

    return value
  
  # table constraints

  # ensure only positive numbers are taken in and require sets if reps exists
  __table_args__ = (
    db.CheckConstraint('reps >= 0', name='check_reps_positive'),
    db.CheckConstraint('sets >= 0', name='check_sets_positive'),
    db.CheckConstraint('duration_seconds >= 0', name='check_duration_positive'),
    db.CheckConstraint('(reps IS NULL OR sets IS NOT NULL)', name='check_reps_require_sets'),
)