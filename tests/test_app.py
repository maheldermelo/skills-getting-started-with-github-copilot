import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def reset_activity_data():
    """Helper to get initial activity data"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Tennis Team": {
            "description": "Competitive tennis training and matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Basketball practice and game participation",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu", "tyler@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater productions and acting workshops",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["jessica@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["ryan@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore STEM concepts through hands-on experiments",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 22,
            "participants": ["hannah@mergington.edu", "noah@mergington.edu"]
        }
    }


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before and after each test"""
    initial = reset_activity_data()
    activities.clear()
    activities.update(copy.deepcopy(initial))
    yield
    activities.clear()
    activities.update(copy.deepcopy(initial))


def test_get_activities_returns_all_activities():
    """AAA: Get activities endpoint returns all activities"""
    # Arrange
    expected = {
        "Chess Club", "Programming Class", "Gym Class", "Tennis Team",
        "Basketball Team", "Drama Club", "Art Studio", "Debate Team",
        "Science Club"
    }
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected


def test_signup_for_activity_success():
    """AAA: Successfully sign up for an activity"""
    # Arrange
    activity = "Chess Club"
    email = "test@mergington.edu"
    initial_count = len(activities[activity]["participants"])
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial_count + 1


def test_signup_for_activity_already_signed_up():
    """AAA: Signup fails when student already signed up"""
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    """AAA: Signup fails for non-existent activity"""
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant_success():
    """AAA: Successfully remove a participant from an activity"""
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    initial_count = len(activities[activity]["participants"])
    
    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial_count - 1


def test_remove_participant_not_found():
    """AAA: Remove fails when participant not in activity"""
    # Arrange
    activity = "Chess Club"
    email = "missing@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_remove_participant_activity_not_found():
    """AAA: Remove fails for non-existent activity"""
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
