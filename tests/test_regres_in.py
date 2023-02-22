import requests
from pytest_voluptuous import S

from config import settings
from schemas.user_schemas import new_user_schema, user_update_schema, user_login_schema


def test_create_user(regres):
    payload = {
        "name": "test_kudaev",
        "job": "qa"
    }

    response = regres.post('/api/users', data=payload)

    assert response.status_code == 201, f"Incorrect status code: {response.status_code}"
    assert response.json()["name"] == "test_kudaev", f"Incorrect name: {response.json()['name']}"
    assert response.json()["job"] == "qa", f"Incorrect job: {response.json()['job']}"
    assert response.json() == S(new_user_schema)


def test_update_user(regres):
    payload = {
        "name": "test_kudaev_updated",
        "job": "zion resident"
    }

    response = regres.put('/api/users/2', data=payload)

    assert response.status_code == 200, f"Incorrect status code: {response.status_code}"
    assert response.json()["name"] == "test_kudaev_updated", f"Incorrect name: {response.json()['name']}"
    assert response.json()["job"] == "zion resident", f"Incorrect job: {response.json()['job']}"
    assert response.json() == S(user_update_schema)


def test_register_user_unsuccessful(regres):
    payload = {
        "email": "test@example.com"
    }

    response = regres.post('/api/register', data=payload)

    assert response.status_code == 400, f"Incorrect status code: {response.status_code}"
    assert response.json()["error"] == "Missing password", f"Incorrect error: {response.json()['error']}"


def test_login_user(regres):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    response = regres.post(url='/api/login', data=payload)

    assert response.status_code == 200, f"Incorrect status code: {response.status_code}"
    assert len(response.json()['token']) == 17, f"Error in the token: {response.json()['token']}"
    assert response.json() == S(user_login_schema)


def test_delete_user(regres):
    response = regres.delete(url='/api/users/2')

    assert response.status_code == 204, f"Incorrect status code: {response.status_code}"
