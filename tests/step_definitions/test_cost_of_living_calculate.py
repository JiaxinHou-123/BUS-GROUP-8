import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/cost_of_living_calculate.feature")

client_fixture = None
response = None

@pytest.fixture
def client(app):
    return app.test_client()

@given("user is on the cost-of-living calculation page", target_fixture="client_ready")
def user_on_page(client):
    global client_fixture
    client_fixture = client
    return client

@when(parsers.re(
    r'user submits rent "(?P<rent>.*)", groceries "(?P<groceries>.*)", transportation "(?P<transportation>.*)", entertainment "(?P<entertainment>.*)"'
))
def submit_calculateForm(rent, groceries, transportation, entertainment):
    global response
    try:
        response = client_fixture.post("/cost_of_living", data={
        'rent': rent,
        'groceries': groceries,
        'transportation': transportation,
        'entertainment': entertainment
    }, follow_redirects=True)
    except ValueError as e:
         print("Caught expected ValueError:", e)
         response = None
   

@then("system should return a total cost calculation")
def calculate_positive():
    assert response.status_code == 200
    assert "Total" in response.get_data(as_text=True) or "£" in response.get_data(as_text=True)

    
@then("system should reject the input and not display the total")
def calculate_negative():
    if response is None:
        assert True
    else:
        assert "Total" not in response.get_data(as_text=True)
