Feature: 9-Day Weather Forecast
  As a user
  I want to view the 9-day weather forecast
  So I can plan my activities accordingly

  Scenario: Verify 9th day forecast is displayed
    Given the MyObservatory app is launched
    When I navigate to the 9-Day Forecast screen
    Then I should see the weather forecast for the 9th day
