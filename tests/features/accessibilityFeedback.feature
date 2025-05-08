@accessibility
Feature: Accessibility User Feedback Submission
         Tests related to accessibility user feedback submission
         
@positive
  Scenario: Student submit valid feedback 
    Given a logged-in student
    When student submits feedback with content "Thank you for your service"
    Then response should contain "Feedback submitted successfully."

@negative
  Scenario: Student submit empty feedback
    Given a logged-in student
    When student submits feedback with content "   "
    Then response should contain "Feedback submission failed"
