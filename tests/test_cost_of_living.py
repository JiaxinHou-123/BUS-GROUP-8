#Conduct positive and negative cases for cost-of-living section,function of budget suggestions

def test_suggest_positive(client):
    
    # The mock real input parameters
    response = client.post('/suggest', data={
        'budget_expression': '500 + 100',
        'time_unit': 'weekly',
        'prefer_dormitory': 'elgar',
        'prefer_food': 'cook',
        'prefer_supplies': 'low',
        'prefer_transport_ways': 'walk'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Here is your Budget plan suggestion!" in response.data
    assert b"Accommodation" in response.data or b"Food" in response.data


def test_suggest_negative(client):

    # The negative case for buddget_expression error input
    response = client.post('/suggest', data={
        'budget_expression': '500 + ABC~!',
        'time_unit': 'monthly',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid characters in the budget expression" in response.data


