import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/cost_of_living_budget.feature")

client_fixture = None
response = None

@pytest.fixture
def client(app):
    return app.test_client()

@given("user is on the budget calculation page", target_fixture="client_ready")
def user_on_page(client):
    global client_fixture
    client_fixture = client
    return client

@when(parsers.parse(
    'user submits accommodation "{accommodation}", dormitory "{dormitory}", food "{food}", transport "{transport}", supplies "{supplies}"'
))
def submit_budgetForm(accommodation, dormitory, food, transport, supplies):
    global response
    response = client_fixture.post("/calculate", data={
        'accommodation': accommodation,
        'dormitory': dormitory,
        'food': food,
        'transport_way': transport,
        'supplies': supplies
    }, follow_redirects=True)

@then("system should return monthly budget")
def budget_positive():
    assert response.status_code == 200
    assert "£" in response.get_data(as_text=True) or "Total Monthly Budget" in response.get_data(as_text=True)

@then("system should reject submission due to miss choose accommodation")
def budget_negative():
    assert response.status_code == 200
    assert "Total Monthly Budget" not in response.get_data(as_text=True)
