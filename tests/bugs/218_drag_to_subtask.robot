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
    go to                           ${root url}
    ${task}=                        create task
    ${sub task}=                    create task
    drag item to                    ${task}             ${sub task}
    wait until keyword succeeds     5 seconds   1 second        task should not be present      ${sub task}
    task should be present          ${task}
    should be subtask               ${task}             ${sub task}

*** Keywords ***
drag item to
    [Arguments]         ${task}      ${sub}
    reload page
    ${sub task id}=     get task id     ${sub}
    ${task id}=         get task id     ${task}
    drag and drop       css=#${sub task id}>.js-drag-task       css=#${task id}
    confirm action


should be subtask
    [Arguments]     ${task}      ${sub}
    click link      partial link=${task}
    task should be present       ${sub}