# Rx API with NLP Prediction
Display active studies, featured Clinical Trial oppurtnities, drugs & medical encyclopedia from ClinicalTrials.gov, NLM, Medline, CDC API/database based on disease terms, drugs or medical terms.

Rest API features an active NLP AI which searched results in different sources and display search results from authorized trusted sources. API further classify studies based using on-premise pre-trained NLP Predictive Analytics and predicts active research clinical trials oppurtunities.

**Sources:** ClinicalTrails.gov, NLM(National Library of Medicine), Medline Medical encyclopedia, CDC, wikipedia

**Author:** Amit Shukla

**Contact:** info@elishconsulting.com

**Releases schedule**
```
    Mar-31-2022 - v0.10 - Active RestAPI
    May-31-2022 - v0.20 - Active Rest API with Predictive Analytics AI
```

---
## about Rx Clinical Trial API
Clinical Trials.gov is extremely rich source of information for active Clinical studies.
This Olive Loop simply access Clinical Trail API and pull results based on active results from ClinicalTrails.gov database.

Also, We developed a ML model based on spacy.io NLP (Natural Language Processing), which takes on-premise studies or any open text in on-premise research documents and find a match from ClinicalTrials.gov.

For example, Organization has on-premise database for active research studies and they want to see "similar" active studies done by other research groups from Clinical Trials database.

Further, this AI/Spacy.io NLP Model can be used to predict disease terms, active similar studies with fuzzy matching title from other online resources like NIH.gov and CDC databases.

This helps, Researchers have complete visibility and operation intelligence information readily available to make quick, effective and informed decisions.


It acts as an AI assistant to help user make quick informed decision. As user input, search for active studies on ClinicalTrial.gov API, it also fetches live data & predictive analytics based on pre-trained AI Spacy.io NLP models on historical transactions stored in system.

# how does it work

    user login to Healthcare OLTP / ERP Application
    user input
    for example, disease terms like | << heart attack >> (use these string for **demo)

    -> Olive Helps Aptitudes / Sensor
        -> Elastic search
            -> Active Study
                
            -> Matching Studies in local on-premise database (non ClinicalTrial)
    
    ** in demo environment, use input such as - << heart attack >> || << stroke >>
    ** in production, backend AI build a unique index tables for elastic search and acknowledge and classify user input search accordingly.

# Technology stack
    Front end: Olive Helps
    Middleware: Olive Loop
    REST API: https://www.clinicaltrials.gov/api/gui
              JuliaLang | NodeJS | Spacy.io NLP Model
    Cloud: any (** Oracle OCI | Microsoft Azure | AWS)
    Database: any (**Oracle | MYSQL | Firebase | MongoDB)
    AI: JuliaLang & FluxML.ai | Python & Pytorch

# Application Process
![Application Process](/assets/images/Application_Process.png)

# System Process
![Application Process](/assets/images/ERD.png)

# License Agreement
https://github.com/AmitXShukla/ClinicalTrials.gov_API_Loop_AI/blob/main/LICENSE

# Privacy Policy
https://github.com/AmitXShukla/SCM_Rx_Inventory_OLIVEai/blob/main/LICENSE

# Aptitudes used
    clipboardListener
    keyboardListener
    networkExample
    searchListener


# how Loop/Author uses the user’s information

    CT_OliveAI loop reads clipboard/ user input text and access/search database / AI Prediction analytics through REST API and renders results.

    This loop does NOT store any user input information anywhere in application and it does NOT alter/update any back-end information based on Olive Helps loop user input.

# Declare where your loop is sending users’ information, including the subdomain level
    loop does NOT send/store any user information, except search strings are used to access API and pull data from database/API.
    
    These search text string are NOT stored anywhere in API/Target system.

# Test your Loop for crashes and bugs
    This loop passed active UAT test.

    Loop is tested for crashed and bugs on-premise data.

# Enable backend services so that they’re live and accessible during review

    https://github.com/AmitXShukla/ClinicalTrials.gov_API_Loop_AI

# Provide documentation and/or source code of how data transmitted from Olive Helps is being consumed and/or persisted

    ClinicalTrials.gov_API_Loop_AI loop reads clipboard/ user input text and access/search database / AI Prediction analytics through REST API and renders results.

    This loop does NOT store any user input information anywhere in application and it does NOT alter/update any back-end information based on Olive Helps loop user input.
    Please refer to Application process above for more details.

# Confirm all servers associated with your loops, transmitted, and/or persisted data are hosted in the US

    All servers associated with loops, transmitted and/or persisted data are hosted in US.

# Confirm no data will be transmitted outside of the US

    No data will be transmitted outside of the US

# how to trigger each type of Whisper or workflow within the Loop
    user login to Healthcare OLTP / ERP Application
    user input
    for example, disease terms like | << heart attack >> (use these string for **demo)

    -> Olive Helps Aptitudes / Sensor
        -> Elastic search
            -> Active Study
                
            -> Matching Studies in local on-premise database (non ClinicalTrial)
    
    ** in demo environment, use input such as - << heart attack >> || << stroke >>
    ** in production, backend AI build a unique index tables for elastic search and acknowledge and classify user input search accordingly.


# Submit detailed explanations of any non-obvious features, including supporting documentation where appropriate
    this loop also used a pre-trained spacy.io NLP model

    please see ML_Models folder in GitHub repository.

# loop is utilizing the loopOpenHandler to initiate loop's start whisper upon selection from search dropdown
    tested