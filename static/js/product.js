// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
      productImages: images,
      selectedImage: 1,
      comments: [],
      reviews: [],
      new_comment: "",
      new_review: "",
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.can_comment = function () {
      if (!isAuthenticated) {
       window.location.replace("/handB/auth/login");
       return false;
     } else if (!hasUsername) {
       window.location.replace("/handB/add_user_personalization");
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
       window.location.replace("/handB/auth/login");
       return false;
     } else if (!hasUsername) {
       window.location.replace("/handB/add_user_personalization");
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

    // This contains all the methods.
    app.methods = {
        add_comment: app.add_comment,
        can_comment: app.can_comment,
        add_review: app.add_review,
        can_review: app.can_review,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
      axios.get(get_comments_url).then(function (response) {
          app.vue.comments = response.data.comments
      })
      axios.get(get_reviews_url).then(function (response) {
          app.vue.reviews = response.data.reviews
      })
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
