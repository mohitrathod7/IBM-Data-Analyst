# %% [markdown]
# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork900-2022-01-01" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
#     </a>
# </p>
# 

# %% [markdown]
# <h1>Extracting and Visualizing Stock Data</h1>
# <h2>Description</h2>
# 

# %% [markdown]
# Extracting essential data from a dataset and displaying it is a necessary part of data science; therefore individuals can make correct decisions based on the data. In this assignment, you will extract some stock data, you will then display this data in a graph.
# 

# %% [markdown]
# <h2>Table of Contents</h2>
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     <ul>
#         <li>Define a Function that Makes a Graph</li>
#         <li>Question 1: Use yfinance to Extract Stock Data</li>
#         <li>Question 2: Use Webscraping to Extract Tesla Revenue Data</li>
#         <li>Question 3: Use yfinance to Extract Stock Data</li>
#         <li>Question 4: Use Webscraping to Extract GME Revenue Data</li>
#         <li>Question 5: Plot Tesla Stock Graph</li>
#         <li>Question 6: Plot GameStop Stock Graph</li>
#     </ul>
# <p>
#     Estimated Time Needed: <strong>30 min</strong></p>
# </div>
# 
# <hr>
# 

# %% [markdown]
# ***Note***:- If you are working Locally using anaconda, please uncomment the following code and execute it.
# Use the version as per your python version.
# 

# %%
!pip install yfinance
!pip install bs4
!pip install nbformat

# %%
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# %% [markdown]
# In Python, you can ignore warnings using the warnings module. You can use the filterwarnings function to filter or ignore specific warning messages or categories.
# 

# %%
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# %% [markdown]
# ## Define Graphing Function
# 

# %% [markdown]
# In this section, we define the function `make_graph`. **You don't have to know how the function works, you should only care about the inputs. It takes a dataframe with stock data (dataframe must contain Date and Close columns), a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock.**
# 

# %%
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

# %% [markdown]
# Use the make_graph function that we’ve already defined. You’ll need to invoke it in questions 5 and 6 to display the graphs and create the dashboard. 
# > **Note: You don’t need to redefine the function for plotting graphs anywhere else in this notebook; just use the existing function.**
# 

# %% [markdown]
# ## Question 1: Use yfinance to Extract Stock Data
# 

# %% [markdown]
# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is `TSLA`.
# 

# %%
tesla = yf.Ticker("TSLA")

# %% [markdown]
# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `tesla_data`. Set the `period` parameter to ` "max" ` so we get information for the maximum amount of time.
# 

# %%
tesla_data = tesla.history(period='max')

# %% [markdown]
# **Reset the index** using the `reset_index(inplace=True)` function on the tesla_data DataFrame and display the first five rows of the `tesla_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.
# 

# %%
tesla_data.reset_index(inplace=True)
tesla_data.head()

# %% [markdown]
# ## Question 2: Use Webscraping to Extract Tesla Revenue Data
# 

# %% [markdown]
# Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm Save the text of the response as a variable named `html_data`.
# 

# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = ' https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'

# Send GET request to the webpage
html_data = requests.get(url)

# %% [markdown]
# Parse the html data using `beautiful_soup` using parser i.e `html5lib` or `html.parser`.
# 

# %%
soup = BeautifulSoup(html_data.text, 'html.parser')

# %% [markdown]
# Using `BeautifulSoup` or the `read_html` function extract the table with `Tesla Revenue` and store it into a dataframe named `tesla_revenue`. The dataframe should have columns `Date` and `Revenue`.
# 

# %%
table = soup.find('table')

# Parse the table data
rows = table.find_all('tr')
tesla_revenue = []
for row in rows[1:]:
    cols = row.find_all('td')
    tesla_revenue.append({
        'Date': cols[0].text.strip(),
        'Revenue': cols[1].text.strip()
    })

# Create DataFrame
tesla_revenue = pd.DataFrame(tesla_revenue)

# Display last five rows
tesla_revenue.tail(5)

# %% [markdown]
# Execute the following line to remove the comma and dollar sign from the `Revenue` column. 
# 

# %%
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace('$', "", regex=False)
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',', "", regex=False)

# %% [markdown]
# Execute the following lines to remove an null or empty strings in the Revenue column.
# 

# %%
tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# %% [markdown]
# Display the last 5 row of the `tesla_revenue` dataframe using the `tail` function. Take a screenshot of the results.
# 

# %%
tesla_revenue.tail(5)

# %% [markdown]
# ## Question 3: Use yfinance to Extract Stock Data
# 

# %% [markdown]
# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is `GME`.
# 

# %%
gme = yf.Ticker("GME")

# %% [markdown]
# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `gme_data`. Set the `period` parameter to ` "max" ` so we get information for the maximum amount of time.
# 

# %%
gme_data = gme.history(period='max')

# %% [markdown]
# **Reset the index** using the `reset_index(inplace=True)` function on the gme_data DataFrame and display the first five rows of the `gme_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.
# 

# %%
gme_data.reset_index(inplace=True)
gme_data.head()

# %% [markdown]
# ## Question 4: Use Webscraping to Extract GME Revenue Data
# 

# %% [markdown]
# Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html. Save the text of the response as a variable named `html_data_2`.
# 

# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'

html_data_2 = requests.get(url)

# %% [markdown]
# Parse the html data using `beautiful_soup` using parser i.e `html5lib` or `html.parser`.
# 

# %%
soup_2 = BeautifulSoup(html_data_2.text, 'html.parser')

# %% [markdown]
# Using `BeautifulSoup` or the `read_html` function extract the table with `GameStop Revenue` and store it into a dataframe named `gme_revenue`. The dataframe should have columns `Date` and `Revenue`. Make sure the comma and dollar sign is removed from the `Revenue` column.
# 

# %% [markdown]
# > **Note: Use the method similar to what you did in question 2.**  
# 

# %% [markdown]
# <details><summary>Click here if you need help locating the table</summary>
# 
# ```
#     
# Below is the code to isolate the table, you will now need to loop through the rows and columns like in the previous lab
#     
# soup.find_all("tbody")[1]
#     
# If you want to use the read_html function the table is located at index 1
# 
# 
# ```
# 
# </details>
# 

# %%
table = soup_2.find('table')

# Parse the table data
rows = table.find_all('tr')
gme_revenue = []
for row in rows[1:]:
    cols = row.find_all('td')
    gme_revenue.append({
        'Date': cols[0].text.strip(),
        'Revenue': cols[1].text.strip()
    })

gme_revenue = pd.DataFrame(gme_revenue)
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace('$', "", regex=False)
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',', "", regex=False)

# %% [markdown]
# Display the last five rows of the `gme_revenue` dataframe using the `tail` function. Take a screenshot of the results.
# 

# %%
gme_revenue.tail(5)

# %% [markdown]
# ## Question 5: Plot Tesla Stock Graph
# 

# %% [markdown]
# Use the `make_graph` function to graph the Tesla Stock Data, also provide a title for the graph. Note the graph will only show data upto June 2021.
# 

# %% [markdown]
# <details><summary>Hint</summary>
# 
# ```
# 
# You just need to invoke the make_graph function with the required parameter to print the graphs.The structure to call the `make_graph` function is `make_graph(tesla_data, tesla_revenue, 'Tesla')`.
# 
# ```
#     
# </details>
# 

# %%
make_graph(tesla_data, tesla_revenue, 'Tesla')

# %% [markdown]
# ## Question 6: Plot GameStop Stock Graph
# 

# %% [markdown]
# Use the `make_graph` function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(gme_data, gme_revenue, 'GameStop')`. Note the graph will only show data upto June 2021.
# 

# %% [markdown]
# <details><summary>Hint</summary>
# 
# ```
# 
# You just need to invoke the make_graph function with the required parameter to print the graphs.The structure to call the `make_graph` function is `make_graph(gme_data, gme_revenue, 'GameStop')`
# 
# ```
#     
# </details>
# 

# %%
make_graph(gme_data, gme_revenue, 'GameStop')

# %% [markdown]
# <h2>About the Authors:</h2> 
# 
# <a href="https://www.linkedin.com/in/joseph-s-50398b136/">Joseph Santarcangelo</a> has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.
# 
# Azim Hirjani
# 

# %% [markdown]
# ## Change Log
# 
# | Date (YYYY-MM-DD) | Version | Changed By    | Change Description        |
# | ----------------- | ------- | ------------- | ------------------------- |
# | 2022-02-28        | 1.2     | Lakshmi Holla | Changed the URL of GameStop |
# | 2020-11-10        | 1.1     | Malika Singla | Deleted the Optional part |
# | 2020-08-27        | 1.0     | Malika Singla | Added lab to GitLab       |
# 
# <hr>
# 
# ## <h3 align="center"> © IBM Corporation 2020. All rights reserved. <h3/>
# 
# <p>
# 

