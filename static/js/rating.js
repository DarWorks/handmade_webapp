let rating = {};

let ratinginit = (rating) => {
    rating.data = {
        defaultstars: 0,
        display: 0,
    };

    rating.set_stars = function(num_stars) {
        rating.vue.defaultstars = num_stars;
        axios.post(set_rating_url, {rating: num_stars});
    };

    rating.stars_out = function() {
        rating.vue.display = rating.vue.defaultstars;
    };

    rating.stars_over = function(num_stars) {
        rating.vue.display = num_stars;
    };

    rating.methods = {
        set_stars: rating.set_stars,
        stars_out: rating.stars_out,
        stars_over: rating.stars_over,
    };

    rating.vue = new Vue({
        el: "#rating-target",
        data: rating.data,
        methods: rating.methods
    });

    rating.init = () => {
        axios.get(get_rating_url)
            .then((result) => {
                rating.vue.defaultstars = result.data.rating; 
                rating.vue.display = result.data.rating; 
            });
    };

    rating.init();
};

ratinginit(rating);