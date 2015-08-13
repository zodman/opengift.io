*** Settings ***
Documentation    Suites Resources
Library     Selenium2Library
Library     libs/PManager/Settings.py

*** Variables ***
${browser}      Firefox
${user}         gvammer
${password}     r00tk1t#


*** Keywords ***

Setup variables
    ${root url}=     get root url
    ${root dir}=     get project root
    ${maildump url}=     get maildumper url
    set global variable  ${root url}
    set global variable  ${root dir}
    set global variable  ${maildump url}

Start the webserver
    Setup variables
    # todo: clean database, start the webserver?
    #       should this be the case, or leave it external
    create webdriver    ${browser}
    Register Keyword To Run On Failure      Capture Page Screenshot

Stop the webserver
#    terminate process   ${django process}
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
