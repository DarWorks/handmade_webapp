// This will be the object that will contain the Vue attributes
// and be used to profilelinkinitialize it.
let profilelinkapp = {};


// Given an empty profilelinkapp object, profilelinkinitializes it filling its attributes,
// creates a Vue instance, and then profilelinkinitializes the Vue instance.
let profilelinkinit = (profilelinkapp) => {

    // This is the Vue data.
    profilelinkapp.data = {
        "username": "",
        "profileURL": "",
    };

    profilelinkapp.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };


    // This contains all the methods.
    profilelinkapp.methods = {
        // Complete as you see fit.
    };

    // This creates the Vue instance.
    profilelinkapp.vue = new Vue({
        el: "#profile-link-target",
        data: profilelinkapp.data,
        methods: profilelinkapp.methods
    });

    // And this profilelinkinitializes it.
    profilelinkapp.profilelinkinit = () => {
      axios.get("/handQ/username").then((res) => {
        profilelinkapp.vue.username = res.data.username
        profilelinkapp.vue.profileURL = `/handQ/profile/${res.data.username}`
      })
    };

    // Call to the profilelinkinitializer.
    profilelinkapp.profilelinkinit();
};

// This takes the (empty) profilelinkapp object, and profilelinkinitializes it,
// putting all the code i
profilelinkinit(profilelinkapp);
