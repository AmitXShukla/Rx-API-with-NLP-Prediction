# Rx API with NLP Prediction
Display active studies, featured Clinical Trial opportunities, drugs & medical encyclopedia from ClinicalTrials.gov, NLM, Medline, CDC API/database based on disease terms, drugs or medical terms.

Rest API features an active NLP AI which search and display search results from authorized trusted sources. API further classify studies based using on-premise pre-trained NLP Predictive Analytics and predicts active research clinical trials opportunities.

**Sources:** ClinicalTrails.gov, NIH, NLM(National Library of Medicine), Medline Medical encyclopedia, CDC, wikipedia

**Author:** Amit Shukla

**Contact:** info@elishconsulting.com

**Releases schedule**
```
    Mar-31-2022 - v0.10 - Active RestAPI
    May-31-2022 - v0.20 - Predictive Analytics AI
```

---
## about Rx Clinical Trial API
Clinical Trials.gov is extremely rich source of information for active Clinical studies.
This REST API calls Clinical Trail API and pull results based on active results from ClinicalTrails.gov database.

Also, We developed a ML model based on spacy.io NLP (Natural Language Processing), which takes on-premise studies or any open text in on-premise research documents and find a match from ClinicalTrials.gov. ML Models helps users located appropriate research and grants opportunities in specified interested domains.

Further, this AI/Spacy.io NLP Model can be used to predict disease terms, active similar studies with fuzzy matching title from other online resources like NIH.gov and CDC databases. Rest API also uses, other sources like NLM, CDC and wikipedia to display and train ML models based on medical encyclopedia / literature.

Using this Rx Clinical Trials API, Researchers have complete visibility and operation intelligence information readily available to make quick, effective and informed decisions.
# how does it work

    user login to Healthcare OLTP / ERP or Web Application
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
    REST API/Sources: https://www.clinicaltrials.gov/api/gui
            https://www.nih.gov/
            https://www.nlm.nih.gov/
            https://www.cdc.gov/
    Cloud: any (** Oracle OCI | Microsoft Azure | AWS)
    Database: any (**Oracle | MYSQL | Firebase | MongoDB)
    AI: JuliaLang & FluxML.ai | Python & Pytorch

# Application Process
![Application Process](/assets/images/app_process.png)

# System Process
![Application Process](/assets/images/Application_Process.png)
# License Agreement
https://github.com/AmitXShukla/Rx-API-with-NLP-Prediction/blob/main/LICENSE

# Privacy Policy
https://github.com/AmitXShukla/Rx-API-with-NLP-Prediction/blob/main/LICENSE
