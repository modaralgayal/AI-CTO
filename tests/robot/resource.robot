*** Settings ***
Library  SeleniumLibrary
Library  ../webdriver_manager_keywords.py

*** Variables ***
${BROWSER}    chrome
${SERVER}     127.0.0.1:5000
${DELAY}      0.1 seconds
${HOME_URL}   http://${SERVER}
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    ${driver_path}=  Get Chrome Driver
    Log    Using ChromeDriver at ${driver_path}
    Open Browser  ${HOME_URL}  ${BROWSER}  executable_path=${driver_path}

Close Browser
    Close All Browsers