def test_root_redirects_to_static(client):
    response = client.get("/")

    assert response.status_code == 200
    assert str(response.url).endswith("/static/index.html")


def test_get_activities_returns_activity_listing(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_for_activity_succeeds_for_new_student(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activity_response = client.get("/activities")
    assert email in activity_response.json()[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_for_activity_rejects_unknown_activity(client):
    response = client.post("/activities/UnknownClub/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_succeeds(client):
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}

    activity_response = client.get("/activities")
    assert email not in activity_response.json()[activity_name]["participants"]


def test_remove_participant_rejects_missing_student(client):
    activity_name = "Programming Class"
    email = "nonexistent@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_participant_rejects_unknown_activity(client):
    response = client.delete("/activities/UnknownClub/participants", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
