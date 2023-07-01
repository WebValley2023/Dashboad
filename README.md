# CS3

WebValley 2023 Computer Science #3 Challenge :bar_chart:
---
**:pushpin: Our goals**
- Creating a dashboard for visualizating data from appa and FBK sensors

**:man: Team members**
- SHOWBIK SHOWMMA
- CHILIANO ARCARESE
- MURILO HADAD
- FRANCESCO PELOSI
- LEONARDO CASAROTTO


**:pager: Concepts & missions**
- Raw data
- Data visualization system
- Data analysis
- make data understandable

**:loop: Skills**
- Programming (Python, Html, CSS, JavaScript)
- Visualization
- Interaction with other groups
- Keep track of progress
- Time dep. analysis
- Tech - writing (DOCS)


:shipit:

## How to run

Local deployment (~15s to start):
```sh
cd plotly-app
DEBUG=True python app.py
```

Server deployment (~15s to start):
```sh
cd plotly-app
gunicorn -b 0.0.0.0:8051 app:server
```
