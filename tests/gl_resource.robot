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

*** Keywords ***
Start the webserver
    # run process     database should be clean slate w only user
#    ${django process}=  start process   python  manage.py     runserver   localhost:${port}
#    set global variable  ${django process}
    log     "test s;elrkslker"

Stop the webserver
#    terminate process   ${django process}
#    close all browsers
    log     "test s;elrkslker"

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
