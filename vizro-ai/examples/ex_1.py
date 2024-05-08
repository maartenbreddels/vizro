"""AI plot example."""
from dotenv import load_dotenv
import os

load_dotenv()
from vizro_ai import VizroAI
from vizro import Vizro
import plotly.express as px

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import vizro.models as vm
from vizro.tables import dash_ag_grid
import sys

sys.path.append('./dashboard')

from dotenv import load_dotenv
from dashboard.vizro_ai_db import VizroAIDashboard
from langchain_community.callbacks import get_openai_callback


model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# model = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# model = ChatAnthropic(
#     model='claude-3-opus-20240229',
#     anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
#     anthropic_api_url=os.environ.get("ANTHROPIC_BASE_URL")
# )
fig_builder = VizroAI(model=model)

df = px.data.gapminder()
query = ("I need a page with a bar chart shoing the population per continent "
         "and a scatter chart showing the life expectency per country as a function gdp. "
         "Make a filter on the country column and use a dropdown as selector. This filter should only "
         "apply to the bar chart. The bar chart should be a stacked bar chart, while "
         "the scatter chart should be colored by the column 'continent'. Make another filter "
         "that filters the GDP column, and it only applies to the scatter chart. I also want "
         "a table that shows the data. The title of the page should be: `This is big time data`. I also want a second page with two "
         "cards on it. One should be a card saying: `This was the jolly data dashboard, it was created in Vizro which is amazing`"
         ", and the second card should refer to the "
         " documentation and link to `https://vizro.readthedocs.io/`. The title of the dashboard should be: `My wonderful "
         "jolly dashboard showing a lot of data`.")
# df = px.data.tips()
# query = ("I want to create a Vizro style dashboard. I need One page. On this page, there are two charts. The first bar chart shows the average tip per day. The second chart shows the distribution of total bill. Add a checklist filter to filter on the time. On this page, also add a card with text 'This page is using the tips dataset.' ")

with get_openai_callback() as cb:
    vizro_ai_dashboard = VizroAIDashboard(model, fig_builder)
    dashboard = vizro_ai_dashboard.build_dashboard(df, query)
    print(cb)

Vizro().build(dashboard).run()
