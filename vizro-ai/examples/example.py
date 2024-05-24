"""AI plot example."""

import vizro.plotly.express as px
from vizro_ai import VizroAI

from dotenv import load_dotenv
load_dotenv()

vizro_ai = VizroAI(model="gpt-4-turbo")
df = px.data.gapminder()
fig = vizro_ai.plot(df, "describe the composition of gdp in continent,and horizontal line for avg gdp", explain=True)
fig.show()
