import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from app import db,User
from werkzeug.security import generate_password_hash

scenarios("../features/accessibilityFeedback.feature")

client_fixture = None
response = None

@pytest.fixture
def client(app):
    return app.test_client()

@given("a logged-in student", target_fixture="client_logged_in")
def client_logged_in(client, app):
    global client_fixture
    client_fixture = client

    with app.app_context():
        # Create test student user:Tom
        user = User.query.filter_by(username="tom").first()
        if not user:
            user = User(
                username="tom",
                role="Student",
                password_hash=generate_password_hash("tom.pw")
            )
            db.session.add(user)
            db.session.commit()

    # Login user
    res = client.post("/login", data={
        "username": "tom",
        "password": "tom.pw",
        "remember_me": "y"
    }, follow_redirects=True)

    assert b"Invalid username" not in res.data
    return client

@when(parsers.parse('student submits feedback with content "{text}"'))
def submit_feedback(text):
    global response
    response = client_fixture.post("/accessibility", data={"feedback_text": text}, follow_redirects=True)

@then(parsers.parse('response should contain "{expected}"'))
def check_response_message(expected):
    assert expected in response.get_data(as_text=True)
