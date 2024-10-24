import vizro.plotly.express as px

gapminder = px.data.gapminder().query(
    "year == 2007 and country.isin(['United States', 'Pakistan', 'India', 'China', 'Indonesia'])"
)

fig = figure = px.bar(gapminder, y="pop", x="country")
