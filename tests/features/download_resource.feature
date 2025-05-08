@cost-of-living
Feature: Download uploaded resources
  Tests for downloading existing resources

  @positive
  Scenario: User downloads an exist file
    Given resource file "Average_Living_costs.jpg" exists in the resource folder
    When user requests to download "Average_Living_costs.jpg"
    Then system should return the file as a downloadable attachment

  @negative
  Scenario: User tries to download a non-existing resource
    Given resource file "Average_Living_costs.pdf" does not exist
    When user requests to download "Average_Living_costs.pdf"
    Then system should redirect and flash file not found message
