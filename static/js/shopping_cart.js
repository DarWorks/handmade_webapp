let app = {};

let init = (app) => {

    app.data = {
        cart: [],
        cart_size: 0,
        cart_total: 0,
        checkout_state: 'checkout',
        fulfillment: { name: "", address: "" },
    };

    app.stripe_session_id = null;

    app.store_cart = function () {
        localStorage[app_name] = JSON.stringify({ cart: app.vue.cart });
    };

    app.read_cart = function () {

        if (localStorage[app_name]) {
            try {
                app.vue.cart = JSON.parse(localStorage[app_name]).cart;

            } catch (error) {
                console.error(error);
                app.vue.cart = [];
            }
        } else {
            app.vue.cart = [];
        }
    };

    app.checkout = function () {
        app.vue.checkout_state = "pay";
    };

    app.pay = function () {
        axios.post(pay_url).then(function (r) {
            if (r.data.ok) {
                let stripe_session_id = r.data.session_id;
                stripe = Stripe(stripe_key);
                stripe.redirectToCheckout({
                    sessionId: stripe_session_id,
                }).then(function (result) {
                    Q.flash(result.error.message);
                });
            }
        });
    };

    app.methods = {
        pay: app.pay,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
        app.read_cart();
    };

    app.init();
};

init(app);
