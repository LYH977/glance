from raceplotly.plots import barplot

# from components.visual.figures.figure_method import configure_fig
from components.visual.figures.configuration import configure_fig
from utils.constant import BAR_CHART_RACE_CONSTANT, ITEM, VALUE, FRAME, BAR_CHART_RACE


def create_bar_chart_race(data, parameter):
    race_plot = barplot(
        data,
        item_column = parameter[BAR_CHART_RACE_CONSTANT[ITEM]],
        value_column = parameter[BAR_CHART_RACE_CONSTANT[VALUE]],
        time_column = FRAME
    )
    fig = race_plot.plot(
        item_label = 'Top 10 crops',
        value_label = 'Production quantity (tonnes)',
        frame_duration = 800
    )

    configure_fig(fig, BAR_CHART_RACE)
    return fig