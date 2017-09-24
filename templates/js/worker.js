$(document).ready(function(){
    var send_button = $( "#submit_button");
    var cmd_input = $("input[name='command_text']");
    var output_texts_id = "#outputs";
    var output_texts = $(output_texts_id);
    var terminal_view = $( "#terminal");

    var key_codes=new Array(33,34,35,36,37,38,39,40);

    // set focus to input:
    cmd_input.focus();

    // keep scrolled at the bottom:
    function scroll_terminal(){
        console.log("Scrolling");
        terminal_view.scrollTop = terminal_view.scrollHeight;
        terminal_view.animate({
            scrollTop: output_texts.height()
        }, "fast");
        return false;
    }

    // If the send button is pressed:
    send_button.click(function(){
        request();
    });

    // Prevent default key (arrows) behaviour:
    $(document).keydown(function(key) {
        if($.inArray(key.which,key_codes) > -1) {
            if (key.which == 38) {
                // get previous command (s)
                console.log("Up key pressed.");
            } else if (key.which == 40) {
                // get next command
                console.log("Down key pressed.");
            }
            return false;
        }
        return true;
    });

    // If some key is pressed:
    $(document).keypress(function(key){
        // docs: http://api.jquery.com/event.which/
        if (key.which == 13) {
            request();
        } else if (key.which == 38) {
            // get previous command (s)
            console.log("Up key pressed.");
        } else if (key.which == 40) {
            // get next command
            console.log("Down key pressed.");
        } else {
            // something else was pressed
            // lets try to work with that as with text:
            console.log("Some other key was pressed.");
        }
    });

    function request(){
        cmd = cmd_input.val().trim();

        if (cmd == "") {
            return;
        }

        $.ajax({
            url: "/api/commands",
            method: "POST",
            data: cmd
        }).done(function(data) {
            console.log(data)
            update_outputs(cmd, data)
        });
    };

    function update_outputs(command, text2add){
        $( "<p>> "  + command + "</p>" ).appendTo(output_texts_id);
        $( new_text ).appendTo(output_texts_id);

        console.log(text2add)
        text2add = text2add.replace(/\\n/g, '<br>');

        var new_text = "<p>" + text2add + "</p>"
        $( new_text ).appendTo(output_texts_id);

        scroll_terminal();
    };
});
