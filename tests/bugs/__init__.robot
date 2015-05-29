*** Settings ***
Library          Selenium2Library
Library          Process
Resource         ../gl_resource.robot
Suite Setup      Authorized user has project
Suite Teardown   Logout user

*** Keywords ***
Authorized user has project
    start the webserver
    create webdriver    ${browser}
    go to   ${root url}/login/
    page should contain     Система ведения проектов, специально разработанная для IT-команд
    page should contain element     name=username
    input text  name=username   ${user}
    input password  name=password   ${password}
    submit form     name=authform
    page should contain link    partial link=Выход

Logout user
    click link  partial link=Выход
    close all browsers
    stop the webserver