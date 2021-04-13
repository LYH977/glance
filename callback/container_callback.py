from datetime import datetime

import dash
from dash.dependencies import Input, Output, ALL, State, MATCH
from dash.exceptions import PreventUpdate
import time

import task
from components import container
from components.carousel import create_ca_img
from utils import collection
from utils.collection import visual_container
from utils.method import get_ctx_type, get_ctx_index, formatted_time_value
from utils.constant import CAROUSEL, FRAME, TIME, CAROUSEL_CONSTANT, ITEM


# update visualization container by appending or removing item from array
def register_update_visual_container(app):
    @app.callback(
        [
            Output('visual-collection', 'children'),
            Output('dashboard-toast', 'data')
        ],
        [
            Input('create-visual', 'n_clicks'),
            Input({'type': 'visualization-container', 'index': ALL}, 'style'),
        ],
        [
            State('visual-collection', 'children') ,
            State('last-param', 'data'),
            State('chosen-tformat', 'data'),
            State('chosen-dropdown', 'data'),

        ],
        prevent_initial_call=True)
    def update_visual_container(create_clicks,  style, div_children, param, tformat, dbname):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)

        if create_clicks and input_type == 'create-visual': # input from add button
            collection.temp = collection.temp.dropna()
            collection.temp.reset_index(drop=True, inplace=True)
            collection.temp[FRAME] = collection.temp[TIME].map(lambda x: formatted_time_value(x, tformat))
            collection.data[create_clicks] = collection.temp
            collection.live_processing[create_clicks] = False
            now = datetime.now().timestamp()
            if param['vtype'] == CAROUSEL: #  carousel
                temp = []
                for row in collection.temp.index:
                    temp.append( create_ca_img(collection.temp.loc[row, param['parameter'][CAROUSEL_CONSTANT[ITEM]]]) )
                collection.img_container[create_clicks] = temp
            else: # other than carousel
                result = task.process_dataset.delay(create_clicks, collection.temp.to_dict(), param['vtype'], param['parameter'], now)
                # task.process_dataset(create_clicks, collection.temp.to_dict(), param['vtype'], param['parameter'], now)

            new_child = container.render_container(create_clicks, param, tformat, dbname, now, collection.new_col)
            div_children.append(new_child)
            visual_container.append(create_clicks)
            toast = {
                'children': f"Visualization {create_clicks} is successfully created.",
                'is_open': True,
                'icon': 'success',
                'header': 'SUCCESS'
            }
            collection.new_col = {'expression': [], 'numeric_col': []}
            # test = str(div_children[0]).split("'type': 'my-index', 'index':")[1].split('}')[0]
            # print(type(test) )

            return div_children, toast

        # elif deletable and input_type=='dlt-btn' : # input from delete button
        #     print(ctx.triggered[0])
        #     delete_index = get_ctx_index(ctx)
        #     # temp = visual_container.index(delete_index)
        #     # del div_children[temp]
        #     # del visual_container[temp]
        #     for vs, i in zip(div_children, range(len(div_children))):
        #         index = int(str(vs).split("'type': 'my-index', 'index': ")[1].split('}')[0])
        #         if delete_index == index:
        #             print('i',i)
        #             div_children.pop(i)
        #             break
        #     toast = {
        #         'children': f"Visualization {delete_index} is successfully deleted.",
        #         'is_open': True,
        #         'icon': 'success',
        #         'header': 'SUCCESS'
        #     }
        #     return div_children, toast
        elif input_type=='visualization-container' : # input from delete button
            delete_index = get_ctx_index(ctx)
            # temp = visual_container.index(delete_index)
            # del div_children[temp]
            # del visual_container[temp]
            time.sleep(0.7) # wait for delete animation
            for vs, i in zip(div_children, range(len(div_children))):
                index = int(str(vs).split("'type': 'my-index', 'index':")[1].split('}')[0])
                if delete_index == index:
                    div_children.pop(i)
                    break
            toast = {
                'children': f"Visualization {delete_index} is successfully deleted.",
                'is_open': True,
                'icon': 'info',
                'header': 'SUCCESS'
            }
            return div_children, toast
        raise PreventUpdate


#############################################################################################################################################

# update play button label according to playing status

def register_delete_animation(app):
    @app.callback(
        Output({'type': 'visualization-container', 'index': MATCH}, 'style'),
        [Input({'type': 'dlt-btn', 'index': MATCH}, 'n_clicks')],
        State({'type': 'visualization-container', 'index': MATCH}, 'style'),

        prevent_initial_call=True
    )
    def delete_animation(click, style):
        if click is not None:
            news = style
            news['opacity'] = 0
            news['transform'] = 'scale(0,0)'
            return news
        raise PreventUpdate