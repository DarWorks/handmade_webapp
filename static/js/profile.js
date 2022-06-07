// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        chatButtonClicked: false,
        new_chat: "",
        chats: [],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.can_chat = function () {
      if (!isAuthenticated) {
       window.location.href = login_url;
       return false;
     } else if (!hasUsername) {
       window.location.href = personalization_url + "?reason=Please+select+a+username+before+you+can+chat";
       return false;
     }
     return true;
    }

    app.add_chat = function () {
      if (app.vue.can_chat()) {
        if (app.vue.new_chat.trim().length > 0) {
          let data = {"chat": app.vue.new_chat};
          axios.post(post_chat_url, data).then(function (response) {
            axios.get(get_chats_url).then(function (response) {
                app.vue.chats = response.data.chats
                app.vue.new_chat = ""
            })
          })
        }
      }
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        add_chat: app.add_chat,
        can_chat: app.can_chat,
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
      axios.get(get_chats_url).then(function (response) {
          app.vue.chats = response.data.chats
      })
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
