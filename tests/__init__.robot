*** Settings ***
Resource    gl_resource.robot
Library     Selenium2Library
Library     Process
Suite Setup     Start the webserver
Suite Teardown  Stop the webserver