const MAXIMUM = 'MAXIMUM'
const MINIMUM = 'MINIMUM'
const FULL = 'FULL'
const FIRST = 'FIRST'
const SECOND = 'SECOND'
const HIDDEN = 'HIDDEN'
//const EXTRA_FOOTER = '</extra>'

const LEGEND_STYLE = {
    HIDDEN : {  y: 0.01,  len: 0  },
    FULL: {  y: 0.01,  len: 0.99  },
    FIRST: {  y: 0.496,  len: 0.505 },
    SECOND: {  y: 0.01,  len: 0.495 },
}

const set_full_legend_style = (fig, coloraxis, style) =>{
    fig['layout'][coloraxis]['colorbar']['y'] = LEGEND_STYLE[style]['y']
    fig['layout'][coloraxis]['colorbar']['len'] = LEGEND_STYLE[style]['len']
    return fig
}

const current_ind = 0

const reset_trace = () =>{
    return {
//        coloraxis:'coloraxis',
        lat: [],
        lon: [],
        marker: {size: 0},
        mode: 'markers',
        showlegend: false,
        type: 'scattermapbox'
    }
}

const modify_hovertemplate = (fig2, number) =>{
    let id = number
    if(number === 1){
        id = 0
    }
//    console.log(fig2['data'][id]['hovertemplate'])
//    let to_split = fig2['data'][id]['hovertemplate'].split(EXTRA_FOOTER)
//    fig2['data'][id]['hovertemplate'] = to_split[0] + 'Layer '+ number + EXTRA_FOOTER

    let text = fig2['data'][id]['hovertemplate']
    fig2['data'][id]['hovertemplate'] = '<b>(Layer '+ number + ')</b><br>'+ text

    return fig2
}

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


const change_frame = (ftype, fig2, value, backup_frames) => {

    if(Object.keys(backup_frames).length !== 0){//multulayer
        let pointers = fig2['frames'][value]['pointers']
        if(pointers.length === 2){
            fig2['data'][0] =  JSON.parse(JSON.stringify(eval('backup_frames' + pointers[0]))) //deepcopy
            fig2['data'][2] = JSON.parse(JSON.stringify(eval('backup_frames' + pointers[1]))) //deepcopy
            fig2 = set_full_legend_style(fig2, 'coloraxis', FIRST)
            fig2 = set_full_legend_style(fig2, 'coloraxis2', SECOND)
//            console.log(fig2)
            fig2 = modify_hovertemplate(fig2, 1)
            fig2 = modify_hovertemplate(fig2, 2)
        }
        else{
            let num = parseInt(pointers[0][8])
            if(num === 0){
                fig2['data'][0] = JSON.parse(JSON.stringify(eval('backup_frames' + pointers[0]))) //deepcopy
                fig2['data'][2] = reset_trace()
                fig2 = set_full_legend_style(fig2, 'coloraxis', FULL)
                fig2 = set_full_legend_style(fig2, 'coloraxis2', HIDDEN)
                fig2 = modify_hovertemplate(fig2, 1)
            }
            else{
                fig2['data'][2] = JSON.parse(JSON.stringify(eval('backup_frames' + pointers[0]))) //deepcopy
                fig2['data'][0] = reset_trace()
                fig2 = set_full_legend_style(fig2, 'coloraxis2', FULL)
                fig2 = set_full_legend_style(fig2, 'coloraxis', HIDDEN)
                fig2 = modify_hovertemplate(fig2, 2)
            }
        }
    }
    else{                                          // single layer
        fig2['data'][0] = fig2['frames'][value]['data'][0]
        fig2 = set_full_legend_style(fig2, 'coloraxis', FULL)
    }

   fig2['layout']['title']['text'] = fig2['frames'][value]['name']



}

const handle_out_of_range_notif = ( celery, slider )=>{
    let length = celery.length
    if(slider > length - 1) return true
    return false
}

//
//const insert_marker = () =>{
//    let tt = 12
//     return {
////        coloraxis: "coloraxis",
//        hovertemplate: 'tt='+tt+'<br>dfdf<extra></extra>',
//        hovertext : ['sd'],
//        lat: [31.533592],
//        lon: [79.355590],
//        marker: {
//            size: 20,
//            symbol: ['embassy'],
//            allowoverlap: true
//        },
//        mode: 'markers',
//        showlegend :false,
//        legendgroup : '',
//        name:'',
//        subplot: 'mapbox',
//        type: 'scattermapbox'
//    }
//}


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


        update_figure: function(value, legend, mapbox, colorscale, marker, secondary, param, atmax, live, new_fig,backup_frames) {
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
                change_frame(param['vtype'], fig2, val,backup_frames)
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
                change_frame(param['vtype'], fig2, value, backup_frames)
                return fig2
            }

            else if(input_type == 'mapbox-type'){
                fig2 = JSON.parse(JSON.stringify(new_fig))
                fig2['layout']['mapbox']['style'] = mapbox
                change_frame(param['vtype'], fig2, value, backup_frames)
                return fig2
            }

            else if(input_type == 'chosen-color-scale'){
                fig2 = JSON.parse(JSON.stringify(new_fig))
                fig2['layout']['coloraxis']['colorscale'] = colorscale['0']['value']
                  if (Object.keys(secondary).length !== 0 && ( Object.keys(fig2['layout']).length === 0 || fig2['layout'].hasOwnProperty("coloraxis2") )){
                      fig2['layout']['coloraxis2']['colorscale'] = colorscale['2']['value']

                 }
                change_frame(param['vtype'], fig2, value , backup_frames)
                return fig2
            }
            else if(input_type == 'marker-data'){
                fig2 = JSON.parse(JSON.stringify(new_fig))
                fig2['data'][1] = marker
                change_frame(param['vtype'], fig2, value,backup_frames)
                return fig2
            }
            else if(input_type == 'secondary-data'){
                if (Object.keys(secondary).length !== 0){
                    fig2 = JSON.parse(JSON.stringify(new_fig))
                    fig2['data'][2] = secondary['frames'][0]['data'][0]
                    fig2['layout']['coloraxis2'] = secondary['coloraxis']
                    fig2['layout']['coloraxis']['colorbar']['y'] = 0.496
                    fig2['layout']['coloraxis']['colorbar']['len'] = 0.505
                    change_frame(param['vtype'], fig2, value, backup_frames)
                    return fig2
                }

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