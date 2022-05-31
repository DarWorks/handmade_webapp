let app = {};

let init = (app) => {
    app.data = {
      cart: [],
      product_id: 0,
      product_added: false,
      productImages: images,
      selectedImage: 1,
      comments: [],
      reviews: [],
      new_comment: "",
      new_review: "",
      defaultstars: 0,
      display: 0,
    };

    app.set_stars = function(num_stars) {
      app.vue.defaultstars = num_stars;
      axios.post(set_rating_url, {rating: num_stars});
    };

    app.stars_out = function() {
      app.vue.display = app.vue.defaultstars;
    };

    app.stars_over = function(num_stars) {
      app.vue.display = num_stars;
    };

    app.methods = {
        set_stars: app.set_stars,
        stars_out: app.stars_out,
        stars_over: app.stars_over,
    };

    app.enumerate = (a) => {
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.can_comment = function () {
      if (!isAuthenticated) {
       window.location.replace("/handmade_webapp/auth/login");
       return false;
     } else if (!hasUsername) {
       window.location.replace("/handmade_webapp/add_user_personalization");
       return false;
     }
     return true;
    }

    app.add_comment = function () {
      if (app.vue.can_comment()) {
        if (app.vue.new_comment.trim().length > 0) {
          let data = {"comment": app.vue.new_comment};
          axios.post(post_comment_url, data).then(function (response) {
            axios.get(get_comments_url).then(function (response) {
                app.vue.comments = response.data.comments
                app.vue.new_comment = ""
            })
          })
        }
      }
    };

    app.can_review = function () {
      if (!isAuthenticated) {
       window.location.replace("/handmade_webapp/auth/login");
       return false;
     } else if (!hasUsername) {
       window.location.replace("/handmade_webapp/add_user_personalization");
       return false;
     }
     return true;
    }

    app.add_review = function () {
      if (app.vue.can_review()) {
        if (app.vue.new_review.trim().length > 0) {
          let data = {"review": app.vue.new_review};
          axios.post(post_reviews_url, data).then(function (response) {
            axios.get(get_reviews_url).then(function (response) {
                app.vue.reviews = response.data.reviews
                app.vue.new_review = ""
            })
          })
        }
      }
    };


    // Reads initial contents of shopping cart
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


    // Puts item into shopping cart
    app.add_to_cart = function () {
      axios.get(get_product_url, { params: { id: product_id } }).then(function (response) {
          app.vue.cart.push(response.data.row);
          localStorage[app_name] = JSON.stringify({ cart: app.vue.cart });

          app.vue.product_added = true;
      });
  };


    app.methods = {
        add_comment: app.add_comment,
        can_comment: app.can_comment,
        add_review: app.add_review,
        can_review: app.can_review,
        add_to_cart: app.add_to_cart,
        set_stars: app.set_stars,
        stars_out: app.stars_out,
        stars_over: app.stars_over,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
      app.read_cart();

      axios.get(get_comments_url).then(function (response) {
          app.vue.comments = response.data.comments
      })
      axios.get(get_reviews_url).then(function (response) {
          app.vue.reviews = response.data.reviews
      })
      axios.get(get_rating_url)
            .then((result) => {
              app.vue.defaultstars = result.data.rating; 
              app.vue.display = result.data.rating; 
            });
    };

    app.init();
};

init(app);
