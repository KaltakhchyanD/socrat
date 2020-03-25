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

        // Return response instead of data to check for bad requests in Controller!
        let response = await fetch(endpoint_url, options);
        return response;
    }
}

class View {
    show_short_link(link){
        let data_html ="<br>"
        data_html+= "<h3>Here is your short link!</h3>" 
        data_html+="<div class=input-group mb-3>"
        data_html+="<input type=\"text\" class=\"form-control\" area-describedby=\"basic-addon2\" value=\""+window.location.href+link+ "\" data-toggle=\"tooltip\" data-placement=\"top\" title=\"Click button to copy\" id=\"text2copy\">  "
        data_html+="<div class\"input-group-append\">"
        data_html+="<button name=\"CopyButton\" class=\"btn btn-outline-secondary\" type=\"button\" >Click to copy</button>  "
        data_html+="</div>"
        data_html+="</div>"
        $("#result_link").html(data_html);
    }
    show_bad_long_url(){
        let data_html ="<br>"
        data_html+="<p>This URL you gave me is not valid! Try better next time</p>"
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
            let response = await this.model.create(create_json);
            if (response['status']==400) {
                this.view.show_bad_long_url();
            } else if (response['status']==200){
                let short_url = await response.json();
                this.view.show_short_link(short_url['short_url']);
                $('[data-toggle="tooltip"]').tooltip();
                this.initializeCopyButtonEvent();
            }
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

    initializeCopyButtonEvent(){
        let copy_buttons = $( ":button[name^='CopyButton']" );
        for (const some_button of copy_buttons){
            some_button.addEventListener ("click", (evt) =>this.myFunction(evt));
        }
    }

    myFunction(evt) {
        evt.preventDefault();
        var copyText = document.getElementById("text2copy");
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");
        $('[data-toggle="tooltip"]').attr('title', 'Copied!').tooltip('dispose').tooltip({title: 'Copied!'});
        $('[data-toggle="tooltip"]').tooltip('show');
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