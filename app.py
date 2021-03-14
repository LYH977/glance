import dash
import dash_bootstrap_components as dbc

from callback.carousel_callback import register_display_image, register_ca_update_slider, register_update_ca_play_btn, \
    register_update_ca_playing_status
from callback.dashboard_callback import register_update_dashboard

from callback.select_dataset_modal_callback import \
    register_update_after_upload, \
    register_enable_create_btn, \
    register_toggle_modal, \
    register_update_output_form, register_validate_sm_create, register_validate_sg_create, register_validate_bc_create, \
    register_validate_d_create, register_validate_ch_create, register_validate_ca_create, register_update_dt_dropdown, \
    register_update_chosen_dropdown, register_update_chosen_tformat

from callback.container_callback import \
    register_update_visual_container, \
    register_update_figure, \
    register_update_slider, \
    register_update_playing_status, \
    register_update_play_btn, register_update_live_mode, register_update_live_data, register_update_atmax, \
    register_toggle_collapse

# meta_tags are required for the app layout to be mobile responsive
from callback.upload_modal_callback import register_update_preview, register_update_datetime_modifier, \
    register_update_datetime_filled, register_update_datetime_upload_btn, register_update_datetime_format, \
    register_update_form_complete, register_handle_upload_click, register_clear_dropdown, \
    register_update_datetime_value, register_update_upload_modal, register_clear_upload_content

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True, update_title=None,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
# select_dataset_modal_callback
register_update_after_upload(app)
register_enable_create_btn(app)
register_update_chosen_tformat(app)
register_update_output_form(app)
register_validate_sm_create(app)
register_validate_sg_create(app)
register_validate_bc_create(app)
register_validate_d_create(app)
register_validate_ch_create(app)
register_validate_ca_create(app)
register_update_dt_dropdown(app)
register_update_chosen_dropdown(app)

# container_callback
register_update_visual_container(app)
register_update_figure(app)
register_update_slider(app)
register_update_playing_status(app)
register_update_play_btn(app)
register_toggle_modal(app)
register_update_live_mode(app)
register_update_live_data(app)
register_update_atmax(app)
register_toggle_collapse(app)

# carousel_callback
register_display_image(app)
register_ca_update_slider(app)
register_update_ca_play_btn(app)
register_update_ca_playing_status(app)

# upload_modal_callback
register_update_preview(app)
register_update_datetime_modifier(app)
register_update_datetime_filled(app)
register_update_datetime_upload_btn(app)
register_update_datetime_format(app)
register_update_form_complete(app)
register_handle_upload_click(app)
register_clear_dropdown(app)
register_update_datetime_value(app)
register_update_upload_modal(app)
register_clear_upload_content(app)


#  dashboard callback
register_update_dashboard(app)
server = app.server
