"""AI plot example."""
from dotenv import load_dotenv
import os

load_dotenv()
from vizro_ai import VizroAI
from vizro import Vizro
import plotly.express as px
from dashboard.model import get_model
from dashboard.plan import get_dashboard_plan

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import vizro.models as vm
from vizro.tables import dash_ag_grid
import sys

sys.path.append('./dashboard')

query = ("I need a page with a bar chart shoing the population per continent "
         "and a scatter chart showing the life expectency per country as a function gdp. "
         "Make a filter on the continent column. This filter should only "
         "apply to the bar chart. Make another filter that filter the scatter chart for population. "
         "The bar chart should be a stacked bar chart, while "
         "the scatter chart should be colored by the column 'continent'. "
         " I also want a table that shows the data. The title of the page should be `My wonderful "
         "jolly dashboard showing a lot of data`.")

model = ChatOpenAI(model="gpt-4-turbo", temperature=0)
# model = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# model = ChatAnthropic(
#     model='claude-3-opus-20240229',
#     anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
#     anthropic_api_url=os.environ.get("ANTHROPIC_BASE_URL")
# )

fig_builder = VizroAI(model=model)
gapminder = px.data.gapminder()

plan = get_dashboard_plan(query, model)
for i in plan.pages[0].components.components:
    print(repr(i))
available_components = [comp.component_id for comp in plan.pages[0].components.components]
for i in plan.pages[0].controls.controls:
    print(repr(i))

page = vm.Page(
    title=plan.pages[0].title,
    components=[
        comp.create(fig_builder=fig_builder, df=gapminder, model=model) for comp in plan.pages[0].components.components
    ],
    controls=[y for x in plan.pages[0].controls.controls if
              (y := x.create(df=gapminder, model=model, available_components=available_components)) is not None],
)

dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
