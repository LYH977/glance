window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        large_params_function: function(param) {
            return param;
        },
        second_function: function(param,lala) {
            console.log(lala)
            return param;
        }
    }
});