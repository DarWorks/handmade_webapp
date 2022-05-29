// This will be the object that will contain the Vue attributes
// and be used to addProdLinkInitialize it.
let addProdLink = {};


// Given an empty addProdLink object, addProdLinkInitializes it filling its attributes,
// creates a Vue instance, and then addProdLinkInitializes the Vue instance.
let addProdLinkInit = (addProdLink) => {

    // This is the Vue data.
    addProdLink.data = {
        "username": "",
        "addProdLink": "",
    };

    addProdLink.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };


      // This contains all the methods.
    addProdLink.methods = {
        // Complete as you see fit.
//        getPage: addProdLink. getPage,
    };
//
//    addProdLink.getPage = function(){
//
//        axios.get("/handB/username").then((res) => {
//        addProdLink.vue.username = res.data.username
//        addProdLink.vue.addProdLink = `/handB/add_product/${res.data.username}`
//       }).catch((e) => {
//            console.log(e)
//
//       });
//
//
//    }
//

    // This creates the Vue instance.
    addProdLink.vue = new Vue({
        el: "#addProd-link-target",
        data: addProdLink.data,
        methods: addProdLink.methods
    });

    // And this addProdLinkInitializes it.
    addProdLink.addProdLinkInit = () => {
      axios.get("/handB/username").then((res) => {
        addProdLink.vue.username = res.data.username
        addProdLink.vue.addProdLink = `/handB/add_product/${res.data.username}`
      })

    };


    // Call to the addProdLinkInitializer.
    addProdLink.addProdLinkInit();
};

// This takes the (empty) addProdLink object, and addProdLinkInitializes it,
// putting all the code i
addProdLinkInit(addProdLink);