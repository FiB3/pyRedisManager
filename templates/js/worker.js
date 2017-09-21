$(document).ready(function(){
    var send_button = $( "#submit_button");
    var cmd_input = $("input[name='command_text']");
    var output_texts_id = "#outputs";
    var output_texts = $(output_texts_id);

    var key_codes=new Array(33,34,35,36,37,38,39,40);

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
            e.preventDefault();
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
        cmd = cmd_input.val();

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
        $("#outputs p:last-child").text("> " + command);
        $( new_text ).appendTo(output_texts_id);
        var new_text = "<p>" + text2add + "</p>"
        $( new_text ).appendTo(output_texts_id);
        $( "<p>></p>" ).appendTo(output_texts_id);
        // text = old + " " + command;
        // text += "\n" + text2add;
        // text += "\n>";
        // text = text.replace("\n", "<br>")
        // outputs_text.text(text);
    };
});

// var sendButton = ;

// sendButton.on( "click", function( event ) {
//   request();
// });
// $( "#submit_button").submit(function( event ) {
//     alert("You've clicked me!");
// });
// sendButton.submit(function( event ) {
//
//   // Stop form from submitting normally
//   event.preventDefault();
//
//   // Get some values from elements on the page:
//   var $form = $( this ),
//     term = $form.find( "input[name='command_text']" ).val(),
//     url = "/api/commands";
//
//   // Send the data using post
//   var posting = $.post( url, term );
//
//   // Put the results in a div
//   posting.done(function( data ) {
//       alert(data)
//     // var content = $( data ).find( "#content" );
//     // $( "#result" ).empty().append( content );
//   });
// }

// function request() {
//     $.post( "/api/commands", "KEYS *" );
// }

// sendButton.ajax({
//   url: "/api/commands",
//   method: 'POST',
//   data: "KEYS *",
//   success: function( result ) {
//     alert(result);
//   }
// });
