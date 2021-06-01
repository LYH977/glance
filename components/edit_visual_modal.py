import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from utils.constant import FIGURE_OPTION, FIGURE_PARAM, CREATE_BTN_ID, SM_PARAM, SG_PARAM, D_PARAM, CA_PARAM, CH_PARAM, \
    BC_PARAM, SCATTER_MAP, DENSITY, CHOROPLETH, CAROUSEL, BAR_CHART_RACE, TIME_FORMAT, YEAR, SECONDARY_FIGURE_OPTION, \
    EDIT_MODAL


edit_modal = html.Div(
    [
        dcc.Store(id='edit-dbname', data=None),
        dcc.Store(id='edit-index', data=None),
        dcc.Store(id='edit-location', data= None),
        dcc.Store(id='param-to-edit', data={}),
        dcc.Store(id='last-saved-param', data={}),
        dcc.Store(id='chosen-tformat_edit_modal', data= YEAR),
        dcc.Store(id='last-saved-tformat', data=YEAR),

        # dcc.Store(id='chosen-dropdown', data= None),
        dbc.Modal(
            [
                dbc.ModalHeader("Edit Visualization", id = 'edit-modal-head'),
                dbc.ModalBody(
                    html.Div(id='edit-visual-portal'),
                ),
                dbc.ModalFooter(
                    html.Div([
                        dbc.Button(
                            "Edit",
                            id="confirm-edit-visual",
                            className="ml-auto",
                            color="success",
                            disabled=True,
                            # style={'display':'block'}
                        ),
                        dbc.Button("Close", id="cancel-edit-visual", className="ml-auto",color="danger"),
                    ], className= 'mod-footer')
                ),
            ],
            id="edit-visual-modal",
            size="xl",
            backdrop='static',
            is_open=False,
            autoFocus=False,
            # style={'background': 'red'}
            contentClassName='select-modal-content',
        ),
    ],
)

def unpack_edit_parameter(param, old_param):
    label  =[]
    id  =[]
    value= []
    multi  =[]
    for p_id, p_info in param.items():

        label.append( p_info['label'] )
        id.append( p_id + '_edit_modal' )
        value.append( old_param[p_id] )
        multi.append( p_info['multi'] )
    return zip(label, id, value, multi)

def edit_parameter_option(columns, label, id, value, multi = False):
    if not multi:
        dropdown = dbc.Select(
            style={'width': '100%'},
            id=id,
            options=[{"label": i, "value": i} for i in columns],
            value = value
        )
    else:
        dropdown = dcc.Dropdown(
            style={'width': '100%'},
            id=id,
            options=[{"label": i, "value": i} for i in columns],
            multi= multi,
            value=value
        )
    return  \
        dbc.FormGroup(
            [
                dbc.Label(label, className="mr-2"),
                dropdown,
            ],
            style={'width': '50%', 'padding':'5px'}
        )


def time_format_option(tformat):
    return  \
        dbc.FormGroup(
                    [
                        dbc.Label('Choose Time Format ?', className="mr-2"),
                        dbc.Select(
                            style={'width': '100%'},
                            id='time-format_edit_modal',
                            options=[{"label": i, "value": j} for i, j in
                                     zip(TIME_FORMAT.keys(), TIME_FORMAT.values())],
                            value = tformat
                        )
                    ],
                    style={'width': '50%', 'padding':'5px'}
        )

def edit_visual_portal_markup(old_param, columns, tformat):
    parameter={}
    type = old_param['vtype']
    for p_id, p_info in FIGURE_PARAM[type].items():
        parameter[p_id] = p_info['value']
    options = [ edit_parameter_option(columns, label, id, value, multi)
                for label, id, value, multi in unpack_edit_parameter( FIGURE_PARAM[type], old_param['parameter'] ) ]
    options.append(time_format_option(tformat))
    return html.Div([
        dcc.Store(id=SM_PARAM+EDIT_MODAL, data={  'vtype': SCATTER_MAP,'parameter': parameter if type == SCATTER_MAP else None,  }),
        dcc.Store(id=D_PARAM+EDIT_MODAL, data={'vtype': DENSITY,'parameter': parameter if type == DENSITY else None,}),
        dcc.Store(id=CH_PARAM+EDIT_MODAL, data={'vtype': CHOROPLETH,'parameter': parameter if type == CHOROPLETH else None,}),
        dcc.Store(id=CA_PARAM+EDIT_MODAL, data={'vtype': CAROUSEL,'parameter': parameter if type == CAROUSEL else None,}),
        dcc.Store(id=BC_PARAM+EDIT_MODAL, data={'vtype': BAR_CHART_RACE,'parameter': parameter if type == BAR_CHART_RACE else None,}),

        dbc.Form(
            options,
            inline=True,
            # style={'background':'red'}
        )
    ])