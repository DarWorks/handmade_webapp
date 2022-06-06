let app = {};

let init = (app) => {
    app.data = {
      cart: [],
      product_id: 0,
      product_added: false,
      rateButtonClicked: false,
      showReviewWarning: false,
      productImages: images,
      selectedImage: 1,
      comments: [],
      reviews: [],
      new_comment: "",
      new_review: "",
      defaultstars: 0,
      display: 0,
      product_available: true,
    };

    app.set_stars = function(num_stars) {
      if (hasUsername) { // equivalent to isPersonalized
        app.vue.defaultstars = num_stars;
        axios.post(set_rating_url, {rating: num_stars});
      } else if (isAuthenticated) { // redirect to personalization page if not personalized
        window.location.href = personalization_url + "?reason=You+need+a+username+before+you+can+rate+a+product";
      } else { // redirect to login if not logged in
        window.location.href = login_url;
      }
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
       window.location.href = login_url;
       return false;
     } else if (!hasUsername) {
       window.location.href = personalization_url + "?reason=You+need+a+username+before+you+can+comment";
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
       window.location.replace(login_url);
       return false;
     } else if (!hasUsername) {
       window.location.href = personalization_url+"?reason=You+need+a+username+before+you+can+leave+a+review";
       return false;
     } else if (!hasPurchasedBefore) {
       app.vue.showReviewWarning = true;
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


    // Puts item into shopping cart
    app.add_to_cart = function () {
      if (!isAuthenticated) {
        window.location.href = login_url;
        return false;
      }

      axios.get(get_product_url, { params: { id: product_id } }).then(function (response) {
          app.vue.cart.push(response.data.row);
          localStorage[app_name + user_id] = JSON.stringify({ cart: app.vue.cart });
          app.vue.product_added = true;
      });
  };

    app.check_added = function () {
      for (let i = 0; i < app.vue.cart.length; i += 1) {
        if (app.vue.cart[i].id == product_id) {
          app.vue.product_added = true;
        }
      }
    }

    app.check_available = function () {
      axios.get(get_product_url, { params: { id: product_id } }).then(function (response) {
        if (response.data.row['quantity'] == 0) {
          app.data.product_available = false;
        }  
    })
    }

    app.methods = {
        add_comment: app.add_comment,
        can_comment: app.can_comment,
        add_review: app.add_review,
        can_review: app.can_review,
        add_to_cart: app.add_to_cart,
        set_stars: app.set_stars,
        stars_out: app.stars_out,
        stars_over: app.stars_over,
        available: app.check_available,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
      app.read_cart();
      app.check_added();
      app.check_available();

      axios.get(get_comments_url).then(function (response) {
          app.vue.comments = response.data.comments
      })
      axios.get(get_reviews_url).then(function (response) {
          app.vue.reviews = response.data.reviews
      })
      if (hasUsername) { // equivalent to isPersonalized
        axios.get(get_rating_url)
        .then((result) => {
          app.vue.defaultstars = result.data.rating;
          app.vue.display = result.data.rating;
        });
      }

    };

    app.init();
};

init(app);
