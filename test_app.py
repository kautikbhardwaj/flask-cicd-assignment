from types import SimpleNamespace

import pytest
from bson.objectid import ObjectId

import app as app_module


class InMemoryStudents:
    def __init__(self):
        self.records = {}

    def find(self):
        return list(self.records.values())

    def find_one(self, query):
        return self.records.get(query["_id"])

    def insert_one(self, document):
        record = document.copy()
        record.setdefault("_id", ObjectId())
        self.records[record["_id"]] = record
        return SimpleNamespace(inserted_id=record["_id"])

    def update_one(self, query, update):
        record = self.records.get(query["_id"])
        if record:
            record.update(update.get("$set", {}))

    def delete_one(self, query):
        self.records.pop(query["_id"], None)

    def delete_many(self, _query):
        self.records.clear()


@pytest.fixture
def client(monkeypatch):
    students = InMemoryStudents()
    fake_mongo = SimpleNamespace(db=SimpleNamespace(students=students))
    monkeypatch.setattr(app_module, "mongo", fake_mongo)

    app_module.app.config["TESTING"] = True

    students.insert_one(
        {
            "_id": ObjectId("66fddff25f4b5f6a0a123456"),
            "name": "Test Student",
            "email": "test@student.com",
            "course": "Flask",
        }
    )

    yield app_module.app.test_client()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Test Student" in response.data


def test_add_student(client):
    data = {"name": "New User", "email": "new@user.com", "course": "Python"}
    response = client.post("/add", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"New User" in response.data


def test_update_student(client):
    student_id = "66fddff25f4b5f6a0a123456"
    data = {
        "name": "Updated Name",
        "email": "updated@student.com",
        "course": "Updated Course",
    }
    response = client.post(f"/update/{student_id}", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Updated Name" in response.data


def test_delete_student(client):
    with app_module.app.app_context():
        student_id = app_module.mongo.db.students.insert_one(
            {
                "name": "Temp User",
                "email": "temp@user.com",
                "course": "Temp Course",
            }
        ).inserted_id

    response = client.get(f"/delete/{student_id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Temp User" not in response.data
