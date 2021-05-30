import dash
import dash_bootstrap_components as dbc

from callback.carousel_callback import register_display_image, register_ca_update_slider, register_update_ca_play_btn, \
    register_update_ca_playing_status, register_update_ca_live_mode, register_ca_update_atmax, \
    register_ca_update_live_data, register_reset_ca_slider_n_interval

from callback.container_callback import register_update_visual_container
from callback.dashboard_callback import register_update_dashboard
from callback.edit_visual_callback import register_toggle_open_edit_modal, register_validate_bc_create_edit_modal, \
    register_validate_d_create_edit_modal, register_validate_sm_create_edit_modal, \
    register_validate_ch_create_edit_modal, register_update_chosen_tformat_edit_modal, register_assign_param_to_edit, \
    register_validate_ca_create_edit_modal, register_toggle_edit_btn
from callback.navbar_callback import register_update_adjust_btn_color, register_toggle_is_adjusting_status, \
    register_toggle_mask_interface, register_disable_floating_btn

from callback.select_dataset_modal_callback import \
    register_update_after_upload, register_enable_create_btn, \
    register_update_output_form, register_validate_sm_create, register_validate_bc_create, \
    register_validate_d_create, register_validate_ch_create, register_validate_ca_create, register_update_dt_dropdown, \
    register_update_chosen_dropdown, register_update_chosen_tformat, register_update_equation, \
    register_update_new_column, register_update_operand_type, register_toggle_new_column_btn, \
    register_clear_popup_value, register_close_popup, register_update_visual_dropdown, register_toggle_modal_action_btn, \
    register_update_visual_type_data

from callback.toast_callback import register_update_toast

from callback.visualization_callback import \
    register_update_figure, register_update_slider, register_update_playing_status, \
    register_update_play_btn, register_update_live_mode, register_update_live_data, register_update_atmax, \
    register_toggle_collapse, register_update_celery_data, register_update_notif_body, register_toggle_badge_color, \
    register_update_last_celery_key, register_export_visual, register_handle_export_btn_click, \
    register_reset_export_interval, register_reset_slider_n_interval, register_update_color_scale, \
    register_update_marker_namelist, register_update_marker_data, register_update_marker_marked_name, \
    register_update_marker_name_section_data, register_reset_lat_long, register_toggle_coordinate_apply_btn, \
    register_update_secondary_frames, register_toggle_secondary_btn_visibility, register_toggle_live_mode, \
    register_update_secondary_action_click, register_update_info_secondary, \
    register_update_secondary_colorscale, register_close_legacy_popover

# meta_tags are required for the app layout to be mobile responsive
from callback.upload_modal_callback import register_update_preview, register_update_datetime_modifier, \
    register_update_datetime_filled, register_update_datetime_upload_btn, register_update_datetime_format, \
    register_update_form_complete, register_clear_dropdown, \
    register_update_datetime_value, register_update_upload_modal, register_clear_upload_content, \
    register_update_dt_input_validity, register_handle_upload_click

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'],
    suppress_callback_exceptions=True,
    update_title=None,
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
)
# app.css.append_css({'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'})

# select_dataset_modal_callback
register_update_after_upload(app)
register_enable_create_btn(app)
register_update_chosen_tformat(app)
register_update_output_form(app)
register_validate_sm_create(app)
register_validate_bc_create(app)
register_validate_d_create(app)
register_validate_ch_create(app)
register_validate_ca_create(app)
register_update_dt_dropdown(app)
register_update_chosen_dropdown(app)
register_update_equation(app)
register_update_new_column(app)
register_update_operand_type(app)
register_toggle_new_column_btn(app)
register_clear_popup_value(app)
register_close_popup(app)
register_update_visual_dropdown(app)
register_update_visual_type_data(app)


# register_toggle_modal(app)
register_toggle_modal_action_btn(app)

# visualization_callback
register_update_figure(app)
register_update_color_scale(app)
register_update_slider(app)
register_update_playing_status(app)
register_reset_slider_n_interval(app)
register_update_play_btn(app)
register_update_live_mode(app)
register_update_live_data(app)
register_update_atmax(app)
register_toggle_collapse(app)
register_update_celery_data(app)
register_update_notif_body(app)
register_toggle_badge_color(app)
register_update_last_celery_key(app)
register_export_visual(app)
register_handle_export_btn_click(app)
register_reset_export_interval(app)
register_update_marker_namelist(app)
register_update_marker_data(app)
register_update_marker_name_section_data(app)
register_update_marker_marked_name(app)
register_reset_lat_long(app)
register_toggle_coordinate_apply_btn(app)
register_update_secondary_action_click(app)
register_update_secondary_frames(app)
register_toggle_secondary_btn_visibility(app)
register_toggle_live_mode(app)
# register_toggle_add_secondary_visual_btn(app)
register_update_info_secondary(app)
register_update_secondary_colorscale(app)
register_close_legacy_popover(app)

# carousel_callback
register_display_image(app)
register_ca_update_slider(app)
register_update_ca_play_btn(app)
register_update_ca_playing_status(app)
register_reset_ca_slider_n_interval(app)
register_update_ca_live_mode(app)
register_ca_update_atmax(app)
register_ca_update_live_data(app)


# upload_modal_callback
register_update_preview(app)
register_update_datetime_modifier(app)
register_update_datetime_filled(app)
register_update_datetime_upload_btn(app)
register_update_datetime_format(app)
register_update_form_complete(app)
register_clear_dropdown(app)
register_update_datetime_value(app)
register_update_upload_modal(app)
register_clear_upload_content(app)
register_update_dt_input_validity(app)
register_handle_upload_click(app)

#  dashboard callback
register_update_dashboard(app)

#  container callback
register_update_visual_container(app)
# register_delete_animation(app)

#  toast callback
register_update_toast(app)

#navbar callback
register_toggle_mask_interface(app)
register_update_adjust_btn_color(app)
register_toggle_is_adjusting_status(app)
register_disable_floating_btn(app)


#edit_visual_callback
register_toggle_open_edit_modal(app)
register_validate_sm_create_edit_modal(app)
register_validate_bc_create_edit_modal(app)
register_validate_d_create_edit_modal(app)
register_validate_ch_create_edit_modal(app)
register_validate_ca_create_edit_modal(app)
register_update_chosen_tformat_edit_modal(app)
register_assign_param_to_edit(app)
register_toggle_edit_btn(app)

server = app.server



