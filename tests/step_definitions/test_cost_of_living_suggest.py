import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/cost_of_living_suggest.feature")

client_fixture = None
response = None

@pytest.fixture
def client(app):
    return app.test_client()

@given("user is on the budget suggestion page", target_fixture="client_ready")
def user_on_page(client):
    global client_fixture
    client_fixture = client
    return client

@when(parsers.parse('user inputs valid expression "{expression}" and choose other options'))
def submit_valid_expression(expression):
    global response
    response = client_fixture.post('/suggest', data={
        'budget_expression': expression,
        'time_unit': 'weekly',
        'prefer_dormitory': 'elgar',
        'prefer_food': 'cook',
        'prefer_supplies': 'low',
        'prefer_transport_ways': 'walk'
    }, follow_redirects=True)

@when(parsers.parse('user inputs invalid expression "{expression}"and choose other options'))
def submit_invalid_expression(expression):
    global response
    response = client_fixture.post('/suggest', data={
        'budget_expression': expression,
        'time_unit': 'monthly',
        'prefer_dormitory': 'maple',
        'prefer_food': 'eatout',
        'prefer_supplies': 'high',
        'prefer_transport_ways': 'bus'
    }, follow_redirects=True)

@then("system should return a budget plan suggestion")
def suggestion_positive():
    assert response.status_code == 200
    assert b"Here is your Budget plan suggestion!" in response.data
    assert b"Accommodation" in response.data or b"Food" in response.data

@then("system should return an error message for invalid expression")
def suggestion_negative():
    assert response.status_code == 200
    assert "Here is your Budget plan suggestion!" not in response.get_data(as_text=True)

