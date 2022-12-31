# <img src="/images/favicon.png" title="Titan up!">  Titans Focused NFL Data Analysis
Repository for code persistence and page hosting. Click the link below to visit page.

>## [Check me out!](https://nbpub.github.io/TitanUp)


## Contents
- [Motivation](#motivation)
- [Data Sources](#data-sources)
- [Feedback](#feedback)
- [Code Notes](#code)
- [Future?](#future)

## Motivation
Utilize sources of NFL data to practice processing, graphing, and interpreting large datasets. 

## Data Sources
 - **[nflverse](https://github.com/nflverse/nflverse-data/releases/tag/pbp)** NFL play-by-play datasets
 - **[nflfastR](https://www.nflfastr.com/articles/field_descriptions.html)** play-by-play field descriptions
 - **[Puntalytics](https://github.com/Puntalytics/puntr/blob/master/R/processing.R)** punt data processing guidance
 - **[Pro-Football-Reference](https://www.pro-football-reference.com/teams/oti/career-av.htm)** Oilers/Titans career AV table, and general reference

## Feedback
**[Submit](https://github.com/NBPub/TitanUp/issues/new/choose)** an issue to comment on the analysis or code. 

## Code Notes
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
<img src="https://raw.githubusercontent.com/mwaskom/seaborn/master/doc/_static/logo-wide-lightbg.svg" style="height:30px;width:auto;">
<img src="https://matplotlib.org/stable/_images/sphx_glr_logos2_003.png" style="height:30px;width:auto;">
<img src="https://repository-images.githubusercontent.com/5171600/28cb0300-7e53-11ea-86e8-ba321370c31a" style="height:30px;width:auto;">
![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black) 
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

The primary purpose of this repository is to host the HTML page containing my analysis. 
I have uploaded code samples for my future self. They should emulate the processes used to populate the 
analysis page, but are not meant to be "deployed". For example, various files are referenced by 
raw strings and Path objects, and these have no relevance to the repository structure.

### [Graphing Functions](https://github.com/NBPub/TitanUp/tree/main/code/graphing/)
The files are organized by the section of the page to which they relate. 
One file loads, processes, and sends data to another, which generates and saves plots.

### [Data Functions](https://github.com/NBPub/TitanUp/tree/main/code/data/)
 - play-by-play (PBP) processing for punting and bonus punter data
 - table creation from processed PBP data
 - Career AV table processing
 - *other data processing is contained in other scripts, such as preparing data for plots*

### [Image Processing](https://github.com/NBPub/TitanUp/tree/main/code/image_processing/)
Pillow functions used to modify images created by the graphing functions:
 - **Crop:** crops image based on background color, used for graphs that couldn't save with a `tight bbox`
 - **Invert:** inverts image, used for aesthetics

