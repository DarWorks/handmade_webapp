let closeapp = {};

let closeinit = (closeapp) => {
    closeapp.data = {
        notifshow: true,
    }

    closeapp.close = function(x) {
        closeapp.vue.notifshow = false;
    };

    closeapp.methods = {
        close: closeapp.close,
    }

    closeapp.vue = new Vue({
        el: "#close-target",
        data: closeapp.data,
        methods: closeapp.methods
    });

    closeapp.init = () => {

    }

    closeapp.init();
};

closeinit(closeapp);
