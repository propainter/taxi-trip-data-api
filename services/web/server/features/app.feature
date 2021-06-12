Feature: User should be able to get application health-check
    Scenario: hit a health-check endpoint
        Given health-check endpoint setup
            When hit health-check endpoint url
            Then check if its http status OK