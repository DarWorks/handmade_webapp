let app = {};

let init = (app) => {

    app.data = {
        add_product_name: add_product_name,
        add_product_type: add_product_type,
        add_product_description: add_product_description,
        add_product_quantity: product_quantity,
        add_product_price: add_product_price,
        product_image1: "",
        product_image2: "",
        product_image3: "",
        product_image4: "",

        submitted: false,

        name_flag: false,
        type_flag: false,
        desc_flag: false,
        price_flag: false,
        img_flag: false,
    };

    app.enumerate = (a) => {
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.check_values = function () {
        let checker = false;

        console.log(app.vue.product_name)

        if (app.vue.add_product_name === "") {
            app.vue.name_flag = true;
            checker = true;
        }

        if (app.vue.add_product_type === "") {
            app.vue.type_flag = true;
            checker = true;
        }

        if (app.vue.add_product_description === "") {
            app.vue.desc_flag = true;
            checker = true;
        }

        if (app.vue.add_product_quantity < 1) {
            app.vue.quantity_flag = true;
            checker = true;
        }

        if (app.vue. add_product_price < 1) {
            app.vue.price_flag = true;
            checker = true;
        }
        return checker;
    }

    app.add_product_info = function () {
        if (!app.check_values()) {
            axios.post(add_product_info_url,
                {
                    product_name: app.vue.add_product_name,
                    product_type: app.vue.add_product_type,
                    product_description: app.vue.add_product_description,
                    product_quantity: app.vue.add_product_quantity,
                    product_price: app.vue.add_product_price,
                    product_image1: app.vue.product_image1,
                    product_image2: app.vue.product_image2,
                    product_image3: app.vue.product_image3,
                    product_image4: app.vue.product_image4,

                }).then(function (r) {
                  window.location.replace(on_edit_url);
                });
        }
    }

    app.upload_file = function (event) {
        let input = event.target;
        let file = input.files[0];
        let file2 = input.files[1];
        let file3 = input.files[2];
        let file4 = input.files[3];

        if (file) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                app.vue.product_image1 = reader.result;
            });
            reader.readAsDataURL(file);
        }
        if (file2) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                app.vue.product_image2 = reader.result;
            });
            reader.readAsDataURL(file2);
        }
        if (file3) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                app.vue.product_image3 = reader.result;
            });
            reader.readAsDataURL(file3);
        }
        if (file4) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                app.vue.product_image4 = reader.result;
            });
            reader.readAsDataURL(file4);
        }
    };

    app.delete = () => {
      axios.post(delete_prod_url).then(res => {
        console.log(on_delete_url);
        window.location.replace(on_delete_url);
      });
    };

    app.methods = {
        add_product_info: app.add_product_info,
        upload_file: app.upload_file,
        delete_prod: app.delete,
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
