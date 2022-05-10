let app = {};

let init = (app) => {

    app.data = {
        add_product_name: "",
        add_product_type: "",
        add_product_description: "",
        add_product_price: 0,
        product_image1: "",
        submitted: false,
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
                product_price: app.vue.add_product_price,
                product_image1: app.vue.product_image1,
            }).then(function (r) {
                app.vue.submitted = true;
            });
    }

    app.upload_file = function (event) {
        let input = event.target;
        let file = input.files[0];
        if (file) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                app.vue.product_image1 = reader.result;
            });
            reader.readAsDataURL(file);
        }
    };

    app.methods = {
        add_product_info: app.add_product_info,
        upload_file: app.upload_file,
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
