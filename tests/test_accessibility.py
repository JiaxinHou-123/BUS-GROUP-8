# User login required before function test

def login_test(client, username, password):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)


def test_accessibilityFeedback_positive(client):

    # The student user in the system database
    login_test(client, "tom", "tom.pw") 
    
    response = client.post('/accessibility', data={'feedback_text': 'Thank you for your service'}, follow_redirects=True)
    
    assert response.status_code == 200
    assert "Feedback submitted successfully." in response.get_data(as_text=True)

def test_accessibilityFeedback_negative(client):# With no feedback submission
    
    login_test(client, "tom", "tom.pw")
    
    response = client.post('/accessibility', data={'feedback_text': '   '}, follow_redirects=True)
    
    assert "Feedback submission failed" in response.get_data(as_text=True)
