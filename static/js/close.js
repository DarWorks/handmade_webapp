let app = {};

let init = (app) => {
    app.data = {
        show: true,
    }

    app.close = function(x) {
        app.vue.show = false;
    };

    app.methods = {
        close: app.close,
    }

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {

    }

    app.init();
}

init(app);
