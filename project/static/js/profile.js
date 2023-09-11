
// const axios = require('axios/dist/browser/axios.cjs'); // browser
//axios.defaults.baseURL = "http://localhost:5000";

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

add_tag = async function(button, type){
    button.disabled = true;
    res = await axios.get("/api/tags");

    console.log(res);
    new_html = '<select class="form-select" aria-label="выбор интереса">';
    for (let i = 0; i < res.data.length; i++) {
        new_html += '<option value="' + res.data[i]["id"] + '">' + res.data[i]["name"] + '</option>'
    }
    button.parentElement.innerHTML =new_html + '</select><button class="btn btn-sm bg-primary mt-2 mb-2" onclick=\'finish_add_tag(this, "' + type + '")\'>Добавить</button>' + button.parentElement.innerHTML;

}

finish_add_tag = async function(button, type){
    
    console.log(button.parentElement)
    value = button.parentElement.getElementsByClassName('form-select')[0].value
    if (value == '') {
        value = '1'
    }
    axios.put("/api/" + type, {
        id: parseInt(value),
    })
    window.location.href = window.location.href;
}

add_subtag = async function(button, tag_id, type){
    button.disabled = true;
    res = await axios.get("/api/tags/" + tag_id + "/subtags");

    console.log(res);
    new_html = '<select class="form-select" aria-label="выбор интереса">';
    for (let i = 0; i < res.data.length; i++) {
        new_html += '<option value="' + res.data[i]["id"] + '">' + res.data[i]["name"] + '</option>'
    }
    button.parentElement.innerHTML =new_html + '</select><button class="btn btn-sm bg-primary mt-2 mb-2" onclick=\'finish_add_tag(this, ' + tag_id + ',"' + type + '")\'>Добавить</button>' + button.parentElement.innerHTML;
    
}

finish_add_tag = async function(button, tag_id, type){
    
    console.log(button.parentElement)
    value = button.parentElement.getElementsByClassName('form-select')[0].value
    if (value == '') {
        value = '1'
    }
    axios.put("/api/" + type, {
        id: parseInt(value),
    })
    window.location.href = window.location.href;
}