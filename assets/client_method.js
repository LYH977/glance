get_ctx_type = (ctx) => {
    obj = ctx['prop_id'].split('.')[0]
    if(obj[0] === '{'){
        temp = JSON.parse(obj)
        type = temp['type']
    }
    else{  type = obj }
    return type
}

get_ctx_index = (ctx) => {
    obj = JSON.parse(ctx['prop_id'].split('.')[0])
    return obj['index']
}

get_ctx_property = (ctx) => { return ctx['prop_id'].split('.')[1] }

get_ctx_value = (ctx) => { return ctx['value'] }

change_frame = (ftype, fig2, value) => {
    fig2['data'][0] = fig2['frames'][value]['data'][0]
    fig2['layout']['title']['text'] = fig2['frames'][value]['name']

}


window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {

        large_params_function: function(param) {   return param;  },

        second_function: function(param, sim) {
            triggered = window.dash_clientside.callback_context.triggered[0]
            console.log('here', get_ctx_type(triggered))
            return param;
        },

        update_figure: function(value, legend, mapbox, param, atmax, live, new_fig, old_fig) {
            triggered = window.dash_clientside.callback_context.triggered[0]
            if(!triggered) throw 'No input yet'
            input_type = get_ctx_type(triggered)
            console.log({input_type})

            if (input_type === 'anim-slider'){
                fig2 = JSON.parse(JSON.stringify(new_fig)) // deep copy
                val = value
                if (live && atmax){
                    new_max = new_fig['frames'].length
                    val = new_max - 1
                }
                change_frame(param['vtype'], fig2, val)
                return fig2
            }
            else if(input_type == 'legend-theme'){
                fig2 = JSON.parse(JSON.stringify(new_fig))
                if(legend){ //dark theme
                    fig2['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(0,0,0,0.75)'
                    fig2['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(255,255,255,1)'
                    fig2['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(255,255,255,1)'
                }
                else{// light theme
                    fig2['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(255,255,255,0.75)'
                    fig2['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(0,0,0,1)'
                    fig2['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(0,0,0,1)'
                }
                change_frame(param['vtype'], fig2, value)
                return fig2
            }

            else if(input_type == 'mapbox-type'){
                fig2 = JSON.parse(JSON.stringify(new_fig))
                fig2['layout']['mapbox']['style'] = mapbox
                change_frame(param['vtype'], fig2, value)
                return fig2
            }
            console.log('return old fig')
            return old_fig

        }


    }
});