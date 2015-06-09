*** Settings ***
Documentation    Check if maildump is running
Library          Selenium2Library
Library          ../libs/MailDump/Mails.py
Resource         ../gl_resource.robot

*** Test Cases ***
Check maildump url
    go to   http://127.0.0.1:1080
    wait until keyword succeeds     5 seconds   0.5 second    Maildump loaded

*** Keywords ***
Maildump loaded
    reload page
    page should contain     MailDump

