// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        hover: false,
        firstRowText: "",
        trendingProducts: [],
        firstProductRow: [],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.setHover =  (hoverBool) => {
        app.vue.hover = hoverBool;
    };

    app.secondRowDisplay = function() {
        axios.get(get_index_data_url).then( function(response) {
            for (let i = 0; i < response.data.trendingProducts.length; i++) {
                  app.vue.trendingProducts.push({
                    trendingProducts: response.data.trendingProducts[i],
                });
            }
            for (let i = 0; i < response.data.firstProductRow.length; i++) {
                  app.vue.firstProductRow.push({
                    firstProductRow: response.data.firstProductRow[i],
                });
            }
            });
            app.enumerate(app.vue.trendingProducts);
            app.enumerate(app.vue.firstProductRow);
            app.vue.firstRowText = response.data.firstRowText;
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        setHover: app.setHover,
        secondRowDisplay: app.secondRowDisplay,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
      // Put here any initialization code.
      // Typically this is a server GET call to load the data.
            axios.get(get_index_data_url).then((result) => {
                app.vue.trendingProducts = app.enumerate(result.data.trendingProducts);
                app.vue.firstProductRow = app.enumerate(result.data.firstProductRow);
                app.vue.firstRowText = result.data.firstRowText;
//                app.secondRowDisplay();
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
