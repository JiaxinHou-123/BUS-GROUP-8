@AI
Feature: AI Chatbot 
  Tests related to AI Model response

  @positive
  Scenario: User sends a valid question to the AI Model
    Given AI model is loaded
    When user sends a question "Hello, could you give me steps on how students enroll in courses at the University of Birmingham?"
    Then AI model should respond with useful answer

  @negative
  Scenario: User sends an empty question to the AI Model
    Given AI model is loaded 
    When user sends a question "empty" 
    Then AI model should still respond
