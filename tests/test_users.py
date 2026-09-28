def user_payload(uid=1 name="Subhan", email="subhan@atu.ie", age 24, student_id="S1234567"):
    return {
        "user_id" : uid,
        "name" : name,
        "email" email,
        "age" : age,
        "student_id" : student_id
    }

def test_create_user_returns_201(client):
    responce = client.post("/api/users", json=)

    assert response.status_code == 201