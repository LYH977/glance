from dash.dependencies import Input, Output


# update play button label according to playing status
def register_update_dashboard(app):
    @app.callback(
        Output('empty-scene', 'children'),
        [Input('visual-collection', 'children')],
        prevent_initial_call=True
    )
    def update_dashboard(children):
        if len(children) >0:
            return None
        else:
            return 'Welcome to Glance'