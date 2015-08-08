.. code:: robotframework

    **** Settings ****
    Resource    Global${/}GlobalResource.tsv
    
    *** Variables ***
    ${inputText}         Logigear
    
    
    *** Test Cases ****
    User should able to perform a search on home page
        Launch Home Page
        Search                ${inputText}
    
    *** Keywords ***
    Launch Home Page
        Open Browser      ${HOMEPAGE_URL}
        Maximize Browser Window
        Log               ${DATEFORMAT}
        Log               ${TIMEFORMAT}
        Log               ${USER}
        Log               ${CURRENT_TIME}
        Log               ${UNIQUESTRING}
        Log               ${AFTERNOON}
        Log               ${AREA1}
        
        
    Search
        [Arguments]    ${text}
        Input Text     lst-ib    ${text}
        Click Button    btnG
        Sleep          10    Wait for Page Load
        Wait Until Element Is Visible    partial link=${text}    10
        Element Should Be Visible    partial link=${text}    ${text} doesn't exist on the page    
        