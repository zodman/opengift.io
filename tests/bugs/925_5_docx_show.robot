*** Settings ***
Documentation    Docx show stopped working, this test ensures the problem is fixed
Library          Selenium2Library
Library          Process
Library          ../libs/PManager/Projects.py
Library          ../libs/PManager/Tasks.py
Library          ../libs/PManager/Messages.py
Library          ../libs/PManager/Tools.py
Resource         ../gl_resource.robot

*** Test Cases ***
User can see docx in fancybox
    Provided precondition
    ${file_name}=   default docx
    When post message with docx     ${file_name}
    And clicked on filename
    Then should see fancybox popup
    And popup should contain    Wqeqwe

User can see docx images
    Provided precondition
    ${file_name}=   default docx with images
    When post message with docx     ${file_name}
    And clicked on filename
    Then should see fancybox popup
    And popup should contain image

*** Keywords ***

Provided precondition
    select new project
    ${task}=    create task
    ${task_url}=    get task url    ${task}
    go to   ${task_url}
Post message with docx
    [Arguments]     ${file_name}
    Create message  testing docx    ${file_name}
    wait until page contains element    css=div.js-filesList    5 seconds
Clicked on filename
    click link      css=div.js-filesList > div > a.fnc_ajax

Should see fancybox popup
    wait until page contains element    css=.fancybox-opened     5 seconds
    page should not contain element     css=.fancybox-error
Popup should contain
    [Arguments]     ${text}
    element should contain     css=.fancybox-inner      ${text}
Popup should contain image
    element should be visible   css=.fancybox-inner>p>img
