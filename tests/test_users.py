import pytest
from fastapi import FastAPI, HTTPException, Response, status


def user_payload(uid=1, name="Subhan", email="subhan@atu.ie", age=24, student_id="S1234567"):
    return {
        "user_id" : uid,
        "name" : name,
        "email": email,
        "age" : age,
        "student_id" : student_id
    }

def test_create_user_returns_201(client):
    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1

@pytest.mark.parametrize(
    "bad_student_id",
    ["123456", "s1234567", "s123", "S12345678"],
)
def test_bad_student_return_422(client, bad_student_id):
    response = client.post("/api/users", json=user_payload(uid=3, student_id=bad_student_id),)
    assert response.status_code == 422

    response = client.post("/api/users", json=user_payload())
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["name"] == "Subhan"
    assert data["email"] == "subhan@atu.ie"
    