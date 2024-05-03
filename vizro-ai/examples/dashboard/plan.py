"""Module containing the planner functionality."""
from typing import Literal, List, Union
from pydantic.v1 import BaseModel as BaseModelV1
from pydantic.v1 import Field
from model import get_model

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

component_type = Literal["AgGrid", "Card", "Graph"]
control_type = Literal["Filter"]


class Component(BaseModelV1):
    component_name: component_type
    component_description: str = Field(...,
                                       description="Description of the component. Include everything that seems to relate to this component.")


class Components(BaseModelV1):
    components: List[Component]


class Control(BaseModelV1):
    control_name: control_type
    control_description: str = Field(...,
                                     description="Description of the control. Include everything that seems to relate to this control.")
#TODO: there is definitely room for dynamic model creation, e.g. with literals for targets

class Controls(BaseModelV1):
    controls: List[Control]


class PagePlanner(BaseModelV1):
    title: str = Field(...,
                       description="Title of the page. If no description is provided, make a short and concise title from the components.")
    components: Components  # List[Component]#
    controls: Controls  # Optional[List[FilterPlanner]]#List[Control]#


class DashboardPlanner(BaseModelV1):
    pages: List[PagePlanner]


def get_dashboard_plan(query: str, model: Union[ChatOpenAI, ChatAnthropic],
                       max_retry: int = 3) -> PagePlanner:
    return get_model(query, model, result_model=DashboardPlanner, max_retry=max_retry)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    query = "I need a page with a bar chart and a scatter chart that filters on "
    "the GDP column and uses a dropdown as selector. This filter should only "
    "apply to the bar chart. The bar chart should be a stacked bar chart, while "
    "the scatter chart should be colored by the column 'continent'. I also want "
    "a table that shows the data. The title of the page should be `My wonderful "
    "jolly dashboard showing a lot of data`."

    model = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    # model = ChatAnthropic(
    #     model='claude-3-opus-20240229',
    #     anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
    #     anthropic_api_url=os.environ.get("ANTHROPIC_BASE_URL")
    # )

    plan = get_dashboard_plan(query, model)
    print(repr(plan))
