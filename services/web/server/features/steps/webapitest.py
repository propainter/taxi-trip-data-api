
from behave import *
from controller import views

'''
Feature: User should be able to get application health-check
    Scenario: hit a health-check endpoint
        Given health-check endpoint setup
            When hit health-check endpoint url
            Then check if its http status OK
'''

@given('health-check endpoint setup')
def step_impl(context):
    pass
@when('hit health-check endpoint url')
def step_impl(context):
    data = views.home()
@then('check if its http status OK')
def step_impl(context):
    assert context.failed is False