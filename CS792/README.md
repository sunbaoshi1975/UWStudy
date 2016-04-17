# Smart Medical Searching Engine
![Smart Medical Searching](https://github.com/sunbaoshi1975/UWStudy/blob/master/CS792/screenshot/query_ui.png)

Smart Medical Searching Engine (SMSE) is an internet resource searching engine with front-end.

This project tries to leverage expert knowledge in a specific and specialized discipline of medicine, to refine and recalibrate the search results. It allows for the fusion of domain expertise and raw page-ranking computation to come up with dependable and professionally authentic results for user queries. One study (JH, 2016) has detected 58% accuracy in diagnosis using Google as a search engine. We plan to improve this figure based on two major optimizations.

## Technical Approach & Software Framework
* Frontend: Bootstrap, AngularJS, jQuery
* Backend: Python/Flask
* Server: Nginx, uWSGI, Postfix  

## Development Tools & Packages
* [GoogleScraper](https://github.com/NikolaiT/GoogleScraper)
* SNOMED/ICD-10
* [Flarum](https://github.com/flarum/flarum)
* Feedparser (RSS)
* GoogleMapAPI

## Usage
To be added...  

## Site Map
![Site Map](https://github.com/sunbaoshi1975/UWStudy/blob/master/CS792/screenshot/sitemap.png)

## Project Structure
run.py - main program
config.py - program configuration
config.ini - uwsgi configuration
output.json - sample output of GoogleScraper
\app\__init__.py - initialization and interfaces
\app\expertise.py - expert opinion
\app\googleScraper.py - call Google in the background
\app\index.py - Flask router
\app\medicalkeywords.py - Medical words lib
\app\pageranker.py - Page Ranker
\app\querygenerator.py - Query Generator 
\static\ - pages, css, img, js, etc.
\templates\ - Web frond-end templates
\terminology\icd10_diseases_and_injuries.py - ICD diseases and injuries terminology
\terminology\mesh.py - MeSH 2016 terminology
\terminology\nlm.py - NLM 2015 terminology
\terminology\snomed.py - SNOMED CT terminology

## License
Licensed under the MIT license.
