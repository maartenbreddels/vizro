"""AI plot example."""
from dotenv import load_dotenv
import os

load_dotenv()
from vizro_ai import VizroAI
from vizro import Vizro
import plotly.express as px
from dashboard.model import get_model
from dashboard.plan import get_dashboard_plan, print_dashboard_plan
from dashboard.build import DashboardBuilder

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import vizro.models as vm
from vizro.tables import dash_ag_grid
import sys

sys.path.append('./dashboard')

from dotenv import load_dotenv


model = ChatOpenAI(model="gpt-4-turbo", temperature=0)
# model = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# model = ChatAnthropic(
#     model='claude-3-opus-20240229',
#     anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
#     anthropic_api_url=os.environ.get("ANTHROPIC_BASE_URL")
# )
fig_builder = VizroAI(model=model)

# df = px.data.gapminder()
# query = ("I need a page with a bar chart shoing the population per continent "
#          "and a scatter chart showing the life expectency per country as a function gdp. "
#          "Make a filter on the GDP column and use a dropdown as selector. This filter should only "
#          "apply to the bar chart. The bar chart should be a stacked bar chart, while "
#          "the scatter chart should be colored by the column 'continent'. I also want "
#          "a table that shows the data. The title of the page should be: `This is big time data`. I also want a second page with just "
#          "a card on it that links to `https://vizro.readthedocs.io/`. The title of the dashboard should be: `My wonderful "
#          "jolly dashboard showing a lot of data`.")
df = px.data.tips()
query = ("I want to create a Vizro style dashboard. I need One page. On this page, there are two charts. The first bar chart shows the average tip per day. The second chart shows the distribution of total bill. Add a checklist filter to filter on the time. On this page, also add a card with text 'This page is using the tips dataset.' ")

dashboard_plan = get_dashboard_plan(query, model)
print_dashboard_plan(dashboard_plan)

dashboard = DashboardBuilder(model=model, data=df, dashboard_plan=dashboard_plan, fig_builder=fig_builder).dashboard

Vizro().build(dashboard).run()
