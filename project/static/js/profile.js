
// const axios = require('axios/dist/browser/axios.cjs'); // browser
axios.defaults.baseURL = "http://localhost:80";

let set_bio = document.getElementById("set_bio");


set_bio.addEventListener(`click`, function () {
    let bio = document.getElementById("bio").value;
    if (bio.length != 0) {
        axios.put("/api/user/bio", {
            bio: bio,
        })
    } else {
        console.log('No bio!');
    }
})

