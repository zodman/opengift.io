*** Settings ***
Documentation    This suite is for mail delivery system testing
Library          Selenium2Library
Library          Process
Library          ../libs/MailDump/Mails.py
Resource         ../gl_resource.robot
Suite Setup      Mail dump up
Suite Teardown   Mail dump down

*** Keywords ***
Mail dump up
    ${settings}=   Mails.configuration
    log     ${settings}
    ${maildump process}=        start process     maildump
    log     ${maildump process}
    process_should_be_running   ${maildump process}
    set global variable     ${maildump process}


Mail dump down
    terminate process   ${maildump process}