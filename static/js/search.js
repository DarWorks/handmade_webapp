let searchapp = {};

let searchinit = (searchapp) => {
    searchapp.data = {
        query: "",
        results: [],
    }

    searchapp.search = function() {
      if (searchapp.vue.query.length < 2) {
        return;
      }
      let data = {
        "params": {
          "q": searchapp.vue.query
        }
      }
      axios.get(searchRoute, data).then((res) => {
        searchapp.vue.results = res.data.results
      })
    };

    searchapp.methods = {
        search: searchapp.search,
    }

    searchapp.vue = new Vue({
        el: "#search-target",
        data: searchapp.data,
        methods: searchapp.methods
    });

    searchapp.init = () => {

    }

    searchapp.init();
};

searchinit(searchapp);
