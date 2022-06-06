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
        localStorage[app_name + user_id] = JSON.stringify({ cart: app.vue.cart });
    };

    app.read_cart = function () {

        if (localStorage[app_name + user_id]) {
            try {
                app.vue.cart = JSON.parse(localStorage[app_name + user_id]).cart;

            } catch (error) {
                console.error(error);
                app.vue.cart = [];
            }
        } else {
            app.vue.cart = [];
        }
    };

    app.clear_cart = function () {
        localStorage[app_name + user_id] = JSON.stringify({ cart: [] });
    };

    app.delete_item = function (product) {
        let i = app.vue.cart.indexOf(product);
        if (i > -1) {
            app.vue.cart.splice(i, 1);
        }
        app.store_cart();

        app.calculate_cost();
    };

    app.checkout = function () {
        app.vue.checkout_state = "pay";
    };

    app.pay = function () {
        axios.post(pay_url, {
            cart: app.vue.cart,
            fulfillment: app.vue.fulfillment
        }).then(function (r) {
            if (r.data.ok) {
                let stripe_session_id = r.data.session_id;
                stripe = Stripe(stripe_key);
                stripe.redirectToCheckout({
                    sessionId: stripe_session_id,
                }).then(function (result) {
                    Q.flash(result.error.message);
                });
            }
            else {
                app.clear_cart();
                Q.flash("Someone has purchased the last stock on one of your items!")
            }

        });
    };

    app.decrease_amount = function (desired, product) {
        if (desired - 1 < 1) {
            return;
        }

        let i = app.vue.cart.indexOf(product);

        app.vue.cart[i].amount_desired -= 1;

        app.store_cart();

        app.calculate_cost();
    }

    app.increase_amount = function (available, desired, product) {
        if (available < desired + 1) {
            return;
        }

        let i = app.vue.cart.indexOf(product);

        app.vue.cart[i].amount_desired += 1;

        app.store_cart();

        app.calculate_cost();
    }

    app.calculate_cost = function () {
        app.vue.cart_total = 0;

        for (let i = 0; i < app.vue.cart.length; i += 1) {
            app.vue.cart_total += app.vue.cart[i].amount_desired * app.vue.cart[i].price
        }
    }

    app.methods = {
        pay: app.pay,
        delete_item: app.delete_item,
        decrease_amount: app.decrease_amount,
        increase_amount: app.increase_amount,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
        app.read_cart();

        app.calculate_cost();
    };

    app.init();
};

init(app);
