let app = {};

let init = (app) => {

    app.data = {
        add_product_name: "",
        add_product_type: "",
        add_product_description: "",
        add_product_price: 0,
        product_image1: "",
        product_image2: "",
        product_image3: "",
        product_image4: "",
        submitted: false,
        show_image1: false,
        show_image2: false,
        show_image3: false,
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
                product_image2: app.vue.product_image1,
                product_image3: app.vue.product_image1,
                product_image4: app.vue.product_image1,
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
                if (!app.vue.product_image1) {
                    app.vue.product_image1 = reader.result;
                }
                if (!app.vue.product_image2) {
                    app.vue.product_image2 = reader.result;
                }
                if (!app.vue.product_image3) {
                    app.vue.product_image3 = reader.result;
                }
                if (!app.vue.product_image4) {
                    app.vue.product_image4 = reader.result;
                }
            });
            reader.readAsDataURL(file);

            event = "";
        }
    };

    app.image_status = function (new_status) {
        if (new_status = "one") {
            app.vue.show_image1 = true;
        }
        if (new_status = "two") {
            app.vue.show_image2 = true;
        }
        if (new_status = "three") {
            app.vue.show_image2 = true;
        }
    };

    app.methods = {
        add_product_info: app.add_product_info,
        upload_file: app.upload_file,
        image_status: app.image_status,
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
