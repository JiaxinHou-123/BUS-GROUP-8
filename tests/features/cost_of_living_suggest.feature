@cost_of_living
Feature: Budget Suggestion 
  Tests related to the cost-of-living section suggestion

  @positive
  Scenario: User submits a valid budget request
    Given user is on the budget suggestion page
    When user inputs valid expression "500 + 100" and choose other options
    Then system should return a budget plan suggestion

  @negative
  Scenario: User submits a budget request with an invalid expression
    Given user is on the budget suggestion page
    When user inputs invalid expression "500 + ABC~!"and choose other options
    Then system should return an error message for invalid expression
