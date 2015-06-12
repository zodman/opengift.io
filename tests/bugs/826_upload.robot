*** Settings ***
Documentation    Все файлы должны загружаться в папку проекта с upload.
Library          Selenium2Library
Library          Process
Library          ../libs/PManager/Projects.py
Library          ../libs/PManager/Tasks.py
Library          ../libs/PManager/Tools.py
Resource         ../gl_resource.robot

*** Test Cases ***
#Can access files page
#    go to   ${root url}/files
#    page should contain     Файлы проекта
Can upload files
    maximize browser window
    select new project
    click link      partial link=Файлы
    ${picture}=     default picture
    set suite variable      ${picture}
    choose file  css=h3.file_upload_button > input      ${picture}
    wait until keyword succeeds     5 seconds       1 second    file uploaded
*** Keywords ***

File uploaded
    ${base name}=   get basename    ${picture}
    element should be visible   xpath=//a[contains(@class, 'file-name')][contains(text(), '${base name}')]




