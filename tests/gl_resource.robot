*** Settings ***
Documentation    Suites Resources
Library     Selenium2Library

*** Variables ***
${port}     8081
${host}     heliard.dev:${port}
${root url}     http://${host}
${browser}      Firefox
${user}         gvammer
${password}     qweqweqwe
${root dir}     /home/rayleigh/projects/heliard
${test project}     Heliard
${maildump url}     127.0.0.1:1080

*** Keywords ***
Start the webserver
    # run process     database should be clean slate w only user
    ${django process}=  start process   python  manage.py     runserver   localhost:${port}
    set global variable  ${django process}
    create webdriver    ${browser}

Stop the webserver
    terminate process   ${django process}
    close all browsers

Authorized user has project
    Login       ${user}     ${password}

Logout user
    click link  partial link=Выход

Login
    [Arguments]     ${login user}     ${login password}
    go to   ${root url}/login/
    page should contain     Система ведения проектов, специально разработанная для IT-команд
    page should contain element     name=username
    input text  name=username   ${login user}
    input password  name=password   ${login password}
    submit form     name=authform
    page should contain link    partial link=Выход
