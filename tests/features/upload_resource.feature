@cost-of-living

Feature: Upload Resources
  Tests for uploading valid and invalid resources

  @positive
  Scenario: Admin uploads a valid resource file
    Given an admin user is logged in
    When admin uploads a file named "test.pdf"
    Then system should confirm the file has been uploaded

  @negative
  Scenario: Admin uploads an unsupported file type
    Given an admin user is logged in
    When admin uploads a file named "test.exe"
    Then system should warn about unsupported file format
