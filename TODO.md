### Must do
Read and work through the ideas: https://pmbaumgartner.github.io/streamlitopedia/front/introduction.html

1. De-couple data loading from data showing
    - https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources
    - start a new project that:
        - reads data needed (the spreadsheet, csv)
        - writes data to parquet/csv files on Deta
        - runs on a schedule to update said files (i.e. every 15 mins)
            - use github workflows
    - update this project to read from the Deta servers


1. Flight Tracker 
    - re-write flight tracking to account for:
        - no flight info
            - different status i.e. 'no flight info', 'landed', 'scheduled', 'en-route'
        - account for multiple flights on one day
        - check for delays and post message on dashboard
    - Tracking map - set lat, lon bounds to be the route distance? 
        - try showing the whole earth as an option

2. Create a flight tracker that gives an option to track a flight by flight number rather than track automatically

2. BUG - 
        THERE IS A BUG IN THE WAY TIME IS PRESENTED (fn_data_prep.py)
        Column EVENT START, EVENT END have not formatted correctly

3. Old school departure board 
    - convert text to image and then load image into gui
        - https://stackoverflow.com/questions/17856242/how-to-convert-a-string-to-an-image


4. Work on layout - can it be better (CSS grid, NAV bar, create your own html and insert using components)


5. What colour scheme do I want for the:
    - https://coolors.co/2364aa-3da5d9-73bfb8-fec601-ea7317 or
    - http://colormind.io/
    - site 
    - graphs/charts


7. Check/test and/or workout how to implement timezones with the data from the spreadsheet so that the times are updated for whoever is looking at the app from whatever timezone they are in.

8. make the globe rotate automatically?
    - https://community.plotly.com/t/animate-rotating-orthographic-map-in-python-plotly/28812/4
    - or a simple animation
        - https://12ft.io/proxy?q=https%3A%2F%2Ftowardsdatascience.com%2Fhow-to-create-an-animated-choropleth-map-with-less-than-15-lines-of-code-2ff04921c60b

8a. Worth updating tracking map with the following 
    - https://stackoverflow.com/questions/66373226/rotate-plotly-figure-to-lat-long

Idea: Create an html page and use streamlits html or iframe component to insert the html in