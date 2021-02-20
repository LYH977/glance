def set_slider_calendar(dataframe):
    calendar = []
    for i in range(0, dataframe.shape[0]):
        value = dataframe[i] if i % 7 == 0 else ''
        calendar.append(value)
    return calendar