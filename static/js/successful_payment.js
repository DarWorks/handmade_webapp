let app = {};

let init = (app) => {

    app.data = {
    };

    app.enumerate = (a) => {
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.clear_cart = function () {
        localStorage[app_name] = JSON.stringify({ cart: [] });
    }

    app.methods = {
        clear_cart: app.clear_cart,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
        app.clear_cart();
    };

    app.init();
};

init(app);