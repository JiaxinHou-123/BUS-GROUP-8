import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from app import get_AIModel

scenarios("../features/chatAI.feature")

tokenizer = None
model = None
chat_history = []
response = None

@given("AI model is loaded")
def load_ai_model():
    global tokenizer, model, chat_history
    tokenizer, model = get_AIModel()
    chat_history = []

@when(parsers.parse(r'user sends a question "{input}"'))
def send_question(input):
    global response
    if input == "empty":
        input = ""
    response, _ = model.chat(tokenizer, input, chat_history)
    print("AI Response:", response)

@then("AI model should respond with useful answer")
def chatAI_positive():
    assert isinstance(response, str)
    assert "enroll" in response.lower() or "birmingham" in response.lower() or len(response.strip()) > 20

@then("AI model should still respond")
def chatAI_negative():
    assert isinstance(response, str)
    assert len(response.strip()) > 0
