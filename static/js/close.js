let closeapp = {};

let init = (closeapp) => {
    closeapp.data = {
        notifbutton: true,
    }

    closeapp.close = function(x) {
        closeapp.vue.notifbutton = false;
    }

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

init(closeapp);
