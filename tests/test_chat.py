# Conduct positive and negative cases for AI section

import pytest

def test_chat_positive(client):
    from app import get_AIModel
    tokenizer, model = get_AIModel()

    input = "Hello, could you give me steps on how students enroll in courses at the University of Birmingham?"
    chat = []
    response, updated = model.chat(tokenizer, input, chat)

    print("AI Response:", response) #Show the real feedback of AI response

    assert isinstance(response, str)
    assert "enroll" in response.lower() or "birmingham" in response.lower() or len(response) > 20 


def test_chat_negative(client):
    
    #import AI model
    from app import get_AIModel
    tokenizer, model = get_AIModel()

    input = ""
    chat = []

    try:
        
        response, updated = model.chat(tokenizer, input, chat)
        
        print("AI Response:", response)
        
        assert isinstance(response, str)
        assert len(response.strip()) > 0
        
    except Exception as e:
        
        pytest.fail(f"Model failed on empty input: {e}")



