let closeapp = {};

let init = (closeapp) => {
    closeapp.data = {
        show: true,
    }

    closeapp.close = function(x) {
        closeapp.vue.show = false;
    };

    closeapp.methods = {
        close: closeapp.close,
    }

    closeapp.vue = new Vue({
        el: "#vue-target",
        data: closeapp.data,
        methods: closeapp.methods
    });

    closeapp.init = () => {

    }

    closeapp.init();
}

init(closeapp);
