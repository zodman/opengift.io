*** Settings ***
Library          Selenium2Library
Library          Process
Resource         ../gl_resource.robot
Suite Setup      Authorized user has project
Suite Teardown   Logout user
