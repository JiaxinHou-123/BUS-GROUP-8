@cost-of-living
Feature: Monthly Cost Calculation
  Tests related to calculate month total cost of living

  @positive
  Scenario: User submits valid numeric inputs
    Given user is on the cost-of-living calculation page
    When user submits rent "600", groceries "200", transportation "100", entertainment "150"
    Then system should return a total cost calculation

  @negative
  Scenario: User submits with empty rent input
    Given user is on the cost-of-living calculation page
    When user submits rent "", groceries "200", transportation "100", entertainment "150"
    Then system should reject the input and not display the total