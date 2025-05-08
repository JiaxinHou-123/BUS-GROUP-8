@cost-of-living

Feature: Calculate Your Budget
  Tests for calculating budget from selecting your information

  @positive
  Scenario: User completes all selections normally
    Given user is on the budget calculation page
    When user submits accommodation "Dormitory", dormitory "elgar", food "cook", transport "walk", supplies "low"
    Then system should return monthly budget

  @negative
  Scenario: User forgets to choose dormitory and chooses other selections
    Given user is on the budget calculation page
    When user submits accommodation "None", dormitory "None", food "cook", transport "walk", supplies "low"
    Then system should reject submission due to miss choose accommodation
