const MAXIMUM = 'MAXIMUM'
const MINIMUM = 'MINIMUM'


const get_ctx_type = (ctx) => {
    let obj = ctx['prop_id'].split('.')[0]
    let type
    if(obj[0] === '{'){
        let temp = JSON.parse(obj)
        type = temp['type']
    }
    else{  type = obj }
    return type
}

const get_ctx_index = (ctx) => {
    let obj = JSON.parse(ctx['prop_id'].split('.')[0])
    return obj['index']
}

const get_ctx_property = (ctx) => { return ctx['prop_id'].split('.')[1] }

const get_ctx_value = (ctx) => { return ctx['value'] }

const change_frame = (ftype, fig2, value) => {
    fig2['data'][0] = fig2['frames'][value]['data'][0]
    fig2['layout']['title']['text'] = fig2['frames'][value]['name']
}

const handle_out_of_range_notif = ( celery, slider )=>{
    let length = celery.length
    if(slider > length - 1) return true
    return false
}

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {

        large_params_function: function(param) {   return param;  },

        second_function: function(param, sim) {
            triggered = window.dash_clientside.callback_context.triggered[0]
            console.log('here', get_ctx_type(triggered))
            return param;
        },

        update_figure: function(value, legend, mapbox, param, atmax, live, new_fig) {
            triggered = window.dash_clientside.callback_context.triggered[0]
            if(!triggered)
                throw window.dash_clientside.PreventUpdate
            input_type = get_ctx_type(triggered)

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
                    fig2['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(0,0,0,1)'
                    fig2['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(255,255,255,1)'
                    fig2['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(255,255,255,1)'
                }
                else{// light theme
                    fig2['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(255,255,255,1)'
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
            throw window.dash_clientside.PreventUpdate

        },


        update_notif_body: function(cdata, slider, itype){
//            console.log('start here')
//             console.log({itype})
//            if(!itype){
//                console.log('throw here ', itype)
//                throw window.dash_clientside.PreventUpdate
//            }
            triggered = window.dash_clientside.callback_context.triggered[0]
            if(!triggered)
                throw window.dash_clientside.PreventUpdate
            if(handle_out_of_range_notif(cdata, slider))
                return ['Loading...', '-', '-']

            type = itype.split('-')[0]

            input_type = get_ctx_type(triggered)

//            console.log('check 1 ', cdata)
//            console.log({type})

            if(input_type == 'celery-data'){

                notif = (type.length > 0) ? cdata[slider][type]['data'] : ''
                return [notif, cdata[slider][MAXIMUM]['count'], cdata[slider][MINIMUM]['count'] ]
            }

            else if (input_type == 'anim-slider' && cdata ){
                notif = (type.length > 0) ? cdata[slider][type]['data'] : ''
                return [notif, cdata[slider][MAXIMUM]['count'], cdata[slider][MINIMUM]['count']]
            }
            else if ( input_type == 'last-notif-click'){
                notif = (type.length > 0) ? cdata[slider][type]['data'] : ''
                return [notif, cdata[slider][MAXIMUM]['count'], cdata[slider][MINIMUM]['count']]
            }
            throw window.dash_clientside.PreventUpdate
        }


    }
});