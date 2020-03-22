class Model {

    async create(long_url) {
        let options = {
            method: "POST",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
                "accepts": "application/json"
            },
            body: JSON.stringify(long_url)
        };
        let endpoint_url = "api/v1/short/";
        // Call the REST endpoint and wait for data
        let response = await fetch(endpoint_url, options);
        let data = await response.json();
        return data;
    }
}

class View {
    show_short_link(link){
        let data_html = "<h3>Here is your short link!</h3>" 
        data_html+="<a href=\""+link +"\">"+window.location.href+link+ "</a>"
        $("#result_link").html(data_html); 
    }
}

class Controller{
    constructor(model, view) {
        this.model = model;
        this.view = view;
        this.initialize();
    }

    async initialize() {
        this.initializeButtonEvent();
    }

    async send_create_button_action(evt, button){
        evt.preventDefault();
        try {   
            let create_json = {
                "long_url":$("#LongUrl").val()
            }
            let short_url = await this.model.create(create_json);
            this.view.show_short_link(short_url['short_url']);
        } catch(err) {
            console.log(err)
        }
    }

    initializeButtonEvent(){
        let send_buttons = $( ":button[name^='SendLongURL']" );
        for (const some_button of send_buttons){
            some_button.addEventListener ("click", (evt) =>this.send_create_button_action(evt, some_button));
        }
    }
}


// Create the MVC components
const model = new Model();
const view = new View();
const controller = new Controller(model, view);

// export the MVC components as the default
export default {
    model,
    view,
    controller
};