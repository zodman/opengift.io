*** Settings ***
Documentation    This suite check the whole process of user registration
Library          Selenium2Library
Library          ../libs/MailDump/Mails.py
Resource         ../gl_resource.robot

*** Test Cases ***
Register from landing
    register
    receive email
    login       ${login}    ${password}

*** Keywords ***
register
    go to   ${root url}
    ${email}=       get random email
    set suite variable      ${email}
    input text      css=#subscriber-email       ${email}
    click button    css=#subscribe-button
    wait until element is visible   css=.popup-alert    4 seconds
    element should contain      css=.popup-alert>h3.title       Спасибо за регистрацию!
    element should contain      css=.popup-alert>.content       В ближайшее время вам на почту придет ссылка на ваш проект.
    element should contain      css=.popup-alert>.content       Обратите внимание: письмо может попасть в спам.

receive email
    go to   ${maildump url}
    find email      ${email}
    wait until keyword succeeds     5 seconds   1 second    message recieved
    select frame    css=iframe#message-body
    ${password}=    get password
    set suite variable      ${password}
    log     ${password}
    ${login}=       get login
    set suite variable      ${login}
    log     ${login}

message recieved
    frame should contain      css=iframe#message-body     Давайте знакомиться!