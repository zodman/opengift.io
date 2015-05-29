*** Settings ***
Documentation    This suite is for testing moving task in another task
Library          Selenium2Library
Library          Process
Resource         ../gl_resource.robot

*** Test Cases ***
User can drag task inside another
    go to   ${root url}
    select project  ${test project}
    create task     task_1
    create task     sub_task_2
    drag item to    sub_task_2      task_1

*** Variables ***
${project select}=   .projects-list-select>select
${create task input}=   .task-create

*** Keywords ***
select project
    [Arguments]     ${project}
    element should be visible   css=${project select}
    select from list by label   css=${project select}   ${project}
    list selection should be    css=${project select}   ${project}
    element should be visible   css=${create task input}
    wait until element is visible   css=${create task input}
create task
    [Arguments]     ${task title}
    input text  css=input${create task input}   ${task title}
    click button    css=button${create task input}
