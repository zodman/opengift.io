*** Settings ***
Documentation    This suite is for testing moving task in another task
Library          Selenium2Library
Library          Process
Library          ../libs/PManager/Projects.py
Library          ../libs/PManager/Tasks.py
Resource         ../gl_resource.robot

*** Test Cases ***
User should be able to drag one task into another
    select new project
    go to                       ${root url}
    ${task}=                    create task
    ${sub_task}=                create task
    drag item to                ${task}             ${sub_task}
    should be subtask           ${task}             ${sub_task}

*** Keywords ***
drag item to
    [Arguments]         ${task}      ${sub}
    reload page
    ${sub task id}=     get task id     ${sub}
    ${task id}=         get task id     ${task}
    set selenium speed  5 seconds
    mouse down          css=#${task id}>div>.js-drag-task
    mouse up            css=#${sub task id}
    capture page screenshot


should be subtask
    [Arguments]     ${task}      ${sub}
