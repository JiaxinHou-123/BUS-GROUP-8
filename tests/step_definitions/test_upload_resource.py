#This is the Admin only function and is the same as upload file in accesssibility section
import io
import os
import pytest
from flask_login import login_user
from pytest_bdd import scenarios, given, when, then, parsers
from app import app as flask_app, db,User
from werkzeug.security import generate_password_hash

scenarios("../features/upload_resource.feature")

client_fixture = None
response = None

@pytest.fixture
def client(app):
    return app.test_client()

@given("an admin user is logged in", target_fixture="admin_logged_in")
def login_admin(client, app):
    with app.app_context():
        user = User.query.filter_by(username="amy").first()
        if not user:
            user = User(username="amy", role="admin", password_hash=generate_password_hash("amy.pw"))
            db.session.add(user)
            db.session.commit()

    res = client.post("/login", data={"username": "amy", "password": "amy.pw","remember_me": "y"}, follow_redirects=True)
    assert res.status_code == 200
    global client_fixture
    client_fixture = client
    return client

@when(parsers.parse('admin uploads a file named "{filename}"'))
def upload_file(filename):
    global response
    content = b"Fake content"
    data = {
        'resource_file': (io.BytesIO(content), filename)
    }
    response = client_fixture.post("/upload_resource", data=data, content_type='multipart/form-data', follow_redirects=True)

@then("system should confirm the file has been uploaded")
def upload_positive():
    assert response.status_code == 200
    assert "has been uploaded" in response.get_data(as_text=True)

@then("system should warn about unsupported file format")
def upload_negative():
    assert response.status_code == 200
    assert "Upload failed" in response.get_data(as_text=True)
