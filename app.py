import dash
import dash_bootstrap_components as dbc

from callback.upload_modal_callback import \
    register_update_option, \
    register_update_after_upload,\
    register_enable_create_btn, \
    register_clear_upload,\
    register_toggle_modal,\
    register_update_output_form


from callback.container_callback import \
    register_update_visual_container, \
    register_update_figure, \
    register_update_slider, \
    register_update_playing_status, \
    register_update_play_btn

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True, update_title=None,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
register_update_option(app)
register_update_after_upload(app)
register_enable_create_btn(app)
register_clear_upload(app)
register_update_output_form(app)

register_update_visual_container(app)
register_update_figure(app)
register_update_slider(app)
register_update_playing_status(app)
register_update_play_btn(app)
register_toggle_modal(app)


server = app.server
