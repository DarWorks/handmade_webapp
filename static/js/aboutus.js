let app = {};

let init = (app) => {
    app.data = {
        aaron: true,
        aarontext: false,
        amaan: true,
        amaantext: false,
        darien: true,
        darientext: false,
        jonathan: true,
        jonathantext: false,
        yashaswi: true,
        yashaswitext: false,
    }

    app.show = function(x) {
        if (x == 1) {
            app.vue.aaron = false;
            app.vue.aarontext = true;
        }
        else if (x == 2) {
            app.vue.amaan = false;
            app.vue.amaantext = true;
        }
        else if (x == 3) {
            app.vue.darien = false;
            app.vue.darientext = true;
        }
        else if (x == 4) {
            app.vue.jonathan = false;
            app.vue.jonathantext = true;
        }
        else if (x == 5) {
            app.vue.yashaswi = false;
            app.vue.yashaswitext = true;
        }
    };

    app.hide = function(x) {
        if (x == 1) {
            app.vue.aaron = true;
            app.vue.aarontext = false;
        }
        else if (x == 2) {
            app.vue.aaman = true;
            app.vue.aamantext = false;
        }
        else if (x == 3) {
            app.vue.darien = true;
            app.vue.darientext = false;
        }
        else if (x == 4) {
            app.vue.jonathan = true;
            app.vue.jonathantext = false;
        }
        else if (x == 5) {
            app.vue.yashaswi = true;
            app.vue.yashaswitext = false;
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
