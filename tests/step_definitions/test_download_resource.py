# Download resource is the same as accessibility download function
import os
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from app import app as flask_app

scenarios("../features/download_resource.feature")

client_fixture = None
response = None
test_filename = None

@pytest.fixture
def client(app):
    return app.test_client()

@given(parsers.parse('resource file "{filename}" exists in the resource folder'))
def create_test_file(filename):
    global test_filename
    folder = flask_app.config['UPLOAD_RESOURCE_FOLDER']
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w') as f:
        f.write("Test content.")
    test_filename = filename

@given(parsers.parse('resource file "{filename}" does not exist'))
def ensure_file_absent(filename):
    global test_filename
    folder = flask_app.config['UPLOAD_RESOURCE_FOLDER']
    file_path = os.path.join(folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    test_filename = filename

@when(parsers.parse('user requests to download "{filename}"'))
def download_resource(filename, client):
    global client_fixture, response
    client_fixture = client
    response = client.get(f"/download_resource/{filename}", follow_redirects=True)

@then("system should return the file as a downloadable attachment")
def download_positive():
    assert response.status_code == 200
    assert 'attachment' in response.headers.get('Content-Disposition', '')

@then("system should redirect and flash file not found message")
def download_negative():
    assert response.status_code == 200 
    assert "File not found" in response.get_data(as_text=True)
