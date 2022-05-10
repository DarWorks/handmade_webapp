let app = {};

let init = (app) => {

    app.data = {
        add_product_name: "",
        add_product_type: "",
        add_product_description: "",
        add_product_price: 0,

    };

    app.enumerate = (a) => {
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.add_product_info = function() {
        axios.post(add_product_info_url,
            {
                product_name: app.vue.add_product_name,
                product_type: app.vue.add_product_type,
                product_description: app.vue.add_product_description,
                product_price : app.vue.add_product_price,
            })
    }

    app.methods = {
        add_product_info: app.add_product_info,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {

    };

    app.init();
};

init(app);
