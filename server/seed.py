#!/usr/bin/end python3

from app import app
from models import *
from datetime import date

with app.app_context():
  # reset data and add new example data committing to db

    WorkoutExercises.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # seed exercises
    pushups = Exercise(
        name="Push Ups",
        category="Strength",
        equipment_needed=False
    )
    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )
    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )
    db.session.add_all([pushups, running, squats])
    db.session.commit()

    # seed workouts
    workout1 = Workout(
        date=date(2026, 4, 25),
        duration_minutes=45,
        notes="Morning workout"
    )
    workout2 = Workout(
        date=date(2026, 4, 26),
        duration_minutes=30,
        notes="Quick cardio session"
    )
    db.session.add_all([workout1, workout2])
    db.session.commit()

    # link exercises to workouts
    we1 = WorkoutExercises(
        workout=workout1,
        exercise=pushups,
        reps=15,
        sets=3
    )
    we2 = WorkoutExercises(
        workout=workout1,
        exercise=squats,
        reps=12,
        sets=3
    )
    we3 = WorkoutExercises(
        workout=workout2,
        exercise=running,
        duration_seconds=1800
    )
    db.session.add_all([we1, we2, we3])
    db.session.commit()