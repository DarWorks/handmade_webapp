// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        add_first_name: "",
        add_last_name: "",
        add_user_userName: "",
        add_user_Email: "",
        add_preference1:"",
        add_preference2:"",
        add_preference3:"",
        add_balance:"",
        validUsername: false,
        submitted: false,
        rows: [],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };


   app.add_personalization = function() {
        //TODO: add row into userProfile DB with  user app.data collected w/vue form
        axios.post(add_personalization_url,
            {
                user_first_name: app.vue.add_first_name,
                user_last_name: app.vue.add_last_name,
                user_userName: app.vue.add_user_userName,
                user_email: app.vue.add_user_Email,
                user_preference1: app.vue.add_preference1,
                user_preference2: app.vue.add_preference2,
                user_preference3: app.vue.add_preference3,

            }).then(function (r) {
                app.vue.submitted = true;
                app.vue.user_userName = true;
            }).catch(function(error){
                 app.vue.user_userName = false;

            });



   };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit
        add_personalization: app.add_personalization,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // This will be a network call to the server to
    // load user data.
    // For the moment, we 'loading' the data from a string.
    app.init = () => {
        axios.get(load_users_url).then(function (response) {
            app.vue.rows = app.enumerate(response.data.rows);
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
