*** Settings ***
Resource    resource.robot

*** Test Cases ***
Testaa Etusivu
    Open And Configure Browser
    

User can see main page
    Open And Configure Browser
    Go To    ${HOME_URL}
    Page Should Contain  AI Project Portfolio Visualization Tool

