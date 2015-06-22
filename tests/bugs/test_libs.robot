*** Settings ***
Documentation    Проверка подключения библиотек
Library          ../libs/TestLib/TestLib.py
Resource         ../gl_resource.robot

*** Test Cases ***
Test custom Lib
    This is log message
