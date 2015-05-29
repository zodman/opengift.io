*** Settings ***
Documentation    Suites Resources
Library     Selenium2Library
*** Variables ***
${port}     8080
${host}     heliard.dev:${port}
${root url}     http://${host}
${browser}      PhantomJS
${user}         gvammer
${password}     qweqweqwe
${root dir}     /home/rayleigh/projects/heliard
${test project}     Heliard
*** Keywords ***
Start the webserver
    ${django process}=  start process   python  manage.py   runserver   localhost:${port}
    set global variable  ${django process}

Stop the webserver
    terminate process   ${django process}
    close all browsers