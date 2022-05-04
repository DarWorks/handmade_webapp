let app = {};

let init = (app) => {

    app.data = {
        fulfillment: {name: "Cool Guy", address: "Moon"},
    };

    app.stripe_session_id = null;
    app.items = [];

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

    // This creates the Vue instance.
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
