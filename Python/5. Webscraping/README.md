# Web-Scraping-challenge
This repository contains a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

### Step 1 - Scraping
Used Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter. Scraped the following sites:
  - [NASA Mars News Site](https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest)
  - Mars images from [Jet Propulsion Laboratory](https://www.jpl.nasa.gov/about/)
  - Mars Weather from [Twitter](https://twitter.com/marswxreport?lang=en)
  - Mars Facts from [Space Facts](https://space-facts.com/mars/)
  - High resolution images for each of Mar's hemisphere from [USGS Astrogeology](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
  
### Step 2 - MongoDB and Flask Application
Used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the websites above. Used Jupyter Notebook to aide in testing the Python script.