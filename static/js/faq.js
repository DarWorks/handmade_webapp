let app = {};

let init = (app) => {
    app.data = {
        a1: true,
        a2: true,
        a3: true,
    }

    app.show = function(x) {
        if (x == 1) {
            app.vue.a1 = false;
        }
        else if (x == 2) {
            app.vue.a2 = false;
        }
        else if (x == 3) {
            app.vue.a3 = false;
        }
    };

    app.hide = function(x) {
        if (x == 1) {
            app.vue.a1 = true;
        }
        else if (x == 2) {
            app.vue.a2 = true;
        }
        else if (x == 3) {
            app.vue.a3 = true;
        }
    };

    app.methods = {
        show: app.show,
        hide: app.hide,
    }

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {

    }

    app.init();
};

init(app);
