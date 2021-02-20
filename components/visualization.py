import pandas as pd                  # for DataFrames
import plotly.express as px
import dash_core_components as dcc
import os

access_token = os.environ['MAP_TOKEN']
px.set_mapbox_access_token(access_token)

# data_url = 'https://shahinrostami.com/datasets/time-series-19-covid-combined.csv'
# data = pd.read_csv(data_url)

def create_scattermap(dataframe,parameter):
    data = dataframe.dropna()
    fig = px.scatter_mapbox(
        data, lat=parameter['latitude'], lon=parameter['longitude'],
        size=parameter['size'], size_max=50,
        color=parameter['color'], color_continuous_scale=px.colors.sequential.Pinkyl,
        hover_name=parameter['name'],
        mapbox_style='dark', zoom=1,
        animation_frame=parameter['frame'],
        # animation_group="Province/State",
        height=600,
        hover_data=parameter['message']
        # hover_data=['Active', 'Confirmed']
        # custom_data=['Date']
    )
    fig.layout.sliders[0].visible = False
    fig.layout.updatemenus[0].visible = False
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
    fig.layout.coloraxis.showscale = False
    fig.layout.margin.t = 30
    fig.layout.margin.b = 30
    fig.layout.updatemenus[0].showactive = True
    return fig





data = pd.read_csv(r"C:\Users\FORGE-15\PycharmProjects\glance\datasets\density.csv")
missing_states = pd.isnull(data['Province/State'])
data.loc[missing_states, 'Province/State'] = data.loc[missing_states, 'Country/Region']
data['Active'] = data['Confirmed'] - data['Recovered'] - data['Deaths']
data = data.dropna()
df_date = data['Date'].unique()
maxValue = df_date.shape[0] - 1
fig = px.scatter_mapbox(
    data, lat="Lat", lon="Long",
    size="Active", size_max=50,
    color="Deaths", color_continuous_scale=px.colors.sequential.Pinkyl,
    hover_name="Province/State",
    mapbox_style='dark', zoom=1,
    animation_frame="Date",
    # animation_group="Province/State",
    height=600,
    hover_data=['Active','Confirmed']
    # custom_data=['Date']
)

data2 = pd.read_csv(r"C:\Users\FORGE-15\PycharmProjects\glance\datasets\eq.csv")
fig.add_densitymapbox(
    lat=data2['Lat'], lon=data2['Long'],
    z=data2['Magnitude'], radius=10, autocolorscale=True, showscale=False
)

fig.layout.sliders[0].visible = False
fig.layout.updatemenus[0].visible = False

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
fig.layout.coloraxis.showscale = False
fig.layout.margin.t = 30
fig.layout.margin.b = 30
fig.layout.updatemenus[0].showactive = True

# fig.layout.updatemenus[0].pad.t = 10

# fig.layout.sliders[0].active = 5

# fig = px.density_mapbox(
#     data, lat="Lat", lon="Long",
#     z="Magnitude", radius=10,
#     center=dict(lat=0, lon=180), zoom=0,
#     animation_frame="Date",
#     height=600,
# )