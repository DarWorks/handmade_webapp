let app = {};

let init = (app) => {
    app.data = {
        aaron: true,
        amaan: true,
        darien: true,
        jonathan: true,
        yashaswi: true,
    }

    app.show = function(x) {
        if (x == 1) {
            app.vue.aaron = false;
        }
        else if (x == 2) {
            app.vue.amaan = false;
        }
        else if (x == 3) {
            app.vue.darien = false;
        }
        else if (x == 4) {
            app.vue.jonathan = false;
        }
        else if (x == 5) {
            app.vue.yashaswi = false;
        }
    };

    app.hide = function(x) {
        if (x == 1) {
            app.vue.aaron = true;
        }
        else if (x == 2) {
            app.vue.amaan = true;
        }
        else if (x == 3) {
            app.vue.darien = true;
        }
        else if (x == 4) {
            app.vue.jonathan = true;
        }
        else if (x == 5) {
            app.vue.yashaswi = true;
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
}

init(app);
