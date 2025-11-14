import pytest
import tkinter as tk
from app.ACEest_Fitness_V1_3 import FitnessTrackerApp

@pytest.fixture
def app_instance():
    """Create a real Tk instance (works in Jenkins with Xvfb)."""
    root = tk.Tk()
    root.withdraw()  # hide GUI window in headless mode
    app = FitnessTrackerApp(root)
    yield app
    root.destroy()


def test_bmi_bmr_calculation(app_instance):
    app = app_instance
    app.name_entry.insert(0, "Monisha")
    app.regn_entry.insert(0, "R001")
    app.age_entry.insert(0, "25")
    app.gender_entry.insert(0, "F")
    app.height_entry.insert(0, "165")
    app.weight_entry.insert(0, "60")

    app.save_user_info()

    assert "bmi" in app.user_info
    assert round(app.user_info["bmi"], 1) == pytest.approx(22.0, 0.1)
    assert app.user_info["bmr"] > 1000  # sanity check


def test_add_workout_entry(app_instance):
    app = app_instance
    app.user_info = {"weight": 60}
    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Running")
    app.duration_entry.insert(0, "30")

    app.add_workout()

    assert len(app.workouts["Workout"]) == 1
    entry = app.workouts["Workout"][0]
    assert entry["exercise"] == "Running"
    assert entry["duration"] == 30
    assert entry["calories"] > 0
