*** Settings ***
Documentation    Все файлы должны загружаться в папку проекта с upload.
Library          Selenium2Library
Library          Projects
Library          Process
Resource         ../gl_resource.robot

*** Test Cases ***
Can access files page
    go to   ${root url}/files
    page should contain     Файлы проекта
Can upload files
    maximize browser window
    select new project
    go to   ${root url}/files
    click element  css=h3.file_upload_button > input
    Capture Page Screenshot     filename=is_form_open



