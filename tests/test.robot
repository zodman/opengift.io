*** Settings ***
Documentation   This is general robotframework test suite to test running
Library     Selenium2Library
Library     Process
Resource    gl_resource.robot


*** Test Cases ***
Test title
    Create Webdriver    ${browser}
    Go To   ${root url}
    page should contain     Heliard
    title should be     Heliard - система ведения командной работы