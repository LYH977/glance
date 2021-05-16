const MAXIMUM = 'MAXIMUM'
const MINIMUM = 'MINIMUM'

const current_ind = 0

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


const insert_marker = () =>{
    let tt = 12
     return {
        coloraxis: "coloraxis",
        hovertemplate: 'tt='+tt+'<br>dfdf<extra></extra>',
        hovertext : ['sd'],
        lat: [31.533592],
        lon: [79.355590],
        marker: {
            size: 20,
            symbol: ['embassy'],
            allowoverlap: true
        },
        mode: 'markers',
        showlegend :false,
        legendgroup : '',
        name:'',
        subplot: 'mapbox',
        type: 'scattermapbox'
    }
}


///////////////////////////////////////////////////////////////////////////////



window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {

        large_params_function: function(param) {   return param;  },

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        second_function: function(param, sim) {
            triggered = window.dash_clientside.callback_context.triggered[0]
            console.log('here', get_ctx_type(triggered))
            return param;
        },


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


        update_figure: function(value, legend, mapbox, colorscale, marker, secondary, param, atmax, live, new_fig) {
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
                change_frame(param[current_ind]['vtype'], fig2, val)
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
                change_frame(param[current_ind]['vtype'], fig2, value)
                return fig2
            }

            else if(input_type == 'mapbox-type'){
                fig2 = JSON.parse(JSON.stringify(new_fig))
                fig2['layout']['mapbox']['style'] = mapbox
                change_frame(param[current_ind]['vtype'], fig2, value)
                return fig2
            }

            else if(input_type == 'chosen-color-scale'){
                fig2 = JSON.parse(JSON.stringify(new_fig))
                fig2['layout']['coloraxis']['colorscale'] = colorscale[current_ind]['value']
                console.log(fig2)
//                fig2['data'][1] = insert_marker()
//                fig2['data'][1] = fig2['frames'][2]['data'][0]
                change_frame(param[current_ind]['vtype'], fig2, value)
                return fig2
            }
            else if(input_type == 'marker-data'){
                fig2 = JSON.parse(JSON.stringify(new_fig))
                fig2['data'][1] = marker
                change_frame(param[current_ind]['vtype'], fig2, value)
                return fig2
            }
            else if(input_type == 'secondary-data'){
                fig2 = JSON.parse(JSON.stringify(new_fig))
                fig2['data'][2] = secondary['frames'][0]['data'][0]
                fig2['layout']['coloraxis2'] = secondary['coloraxis']
                fig2['layout']['coloraxis']['colorbar']['y'] = 0.496
                fig2['layout']['coloraxis']['colorbar']['len'] = 0.505
                console.log(fig2)
                change_frame(param[current_ind]['vtype'], fig2, value)
                return fig2
            }
            throw window.dash_clientside.PreventUpdate
        },

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        update_notif_body: function(cdata, slider, itype){
            triggered = window.dash_clientside.callback_context.triggered[0]
            if(!triggered)
                throw window.dash_clientside.PreventUpdate
            if(handle_out_of_range_notif(cdata, slider))
                return ['Loading...', '-', '-']

            type = itype.split('-')[0]

            input_type = get_ctx_type(triggered)
            if(input_type == 'celery-data'){
//                console.log('celery-data')
                if ( !(slider in cdata)){
                    throw window.dash_clientside.PreventUpdate
                }
                notif = (type.length > 0) ? cdata[slider][type]['data'] : ''
                return [notif, cdata[slider][MAXIMUM]['count'], cdata[slider][MINIMUM]['count'] ]
            }

            else if (input_type == 'anim-slider' && cdata ){
//                console.log(cdata)
//                console.log(slider)
                if ( !(slider in cdata)){
                    throw window.dash_clientside.PreventUpdate
                }
                notif = (type.length > 0) ? cdata[slider][type]['data'] : ''
                return [notif, cdata[slider][MAXIMUM]['count'], cdata[slider][MINIMUM]['count']]
            }
            else if ( input_type == 'last-notif-click'){
//                console.log('last-notif-click')
                if ( !(slider in cdata)){
                    throw window.dash_clientside.PreventUpdate
                }
                notif = (type.length > 0) ? cdata[slider][type]['data'] : ''
                return [notif, cdata[slider][MAXIMUM]['count'], cdata[slider][MINIMUM]['count']]
            }
            throw window.dash_clientside.PreventUpdate
        }
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    }
});