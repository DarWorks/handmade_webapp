let app = {};


let init = (app) => {

    app.data = {
        profile_pic: "",
    };

    app.enumerate = (a) => {
        let k = 0;
        a.map((e) => { e._idx = k++; });
        return a;
    };

    app.upload_file = async function (event) {
        app.convert_image(event);

        setTimeout(function(){ 
            if (app.vue.profile_pic) {

                axios.post(add_profile_pic_url,
                    {
                        profile_pic: app.vue.profile_pic,
                    })
            }
        }, 1000);
    }

    app.convert_image = function (event) {
        let input = event.target;
        let file = input.files[0];

        if (file) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                app.vue.profile_pic = reader.result;
            });
            reader.readAsDataURL(file);
        }
    }

    app.grab_profile_pic = function () {
        axios.get(get_profile_pic_url).then(function (response) {
            app.vue.profile_pic = response.data.profile_pic;
        })
    }

    app.methods = {
        upload_file: app.upload_file,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
        app.grab_profile_pic();
        console.log();
    };

    app.init();
};

init(app);
