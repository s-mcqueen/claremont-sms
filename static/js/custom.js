var $new_user_data,
    verif_code;

$(function(){

    // home page signup button - just validates signup info
    $('#signup-btn').on('click', function(e){
        e.preventDefault();

        // store the signup data
        $new_user_data = $('#signup-form')

        $.ajax({
            type: "POST",
            dataType: "json",
            url: $SCRIPT_ROOT + '/signup',
            data: $new_user_data.serialize()
        }).done(function(data) {

            if(data.errors) {

                $('.errors-detail').text(data.errors).show();
                $("#error").modal("show");
            }

            else {

                $("#verif").modal("show");
                send_verif();
            }           
        });

    });

    // if verif modal open, send the user the verification code 
    // and store data
    function send_verif() {

        $.ajax({
            type: "POST",
            dataType: "json",
            url: $SCRIPT_ROOT + '/send_verif',
            data: $new_user_data.serialize()
        })

    };


    // verif modal button - validate correct verif code and set is_active true
    $('#verif-btn').on('click', function(e){
        e.preventDefault();

        // add the verif-form data to the signup form data
        var data = $new_user_data.serialize() + "&" + $('#verif-form').serialize();

        $.ajax({
            type: "POST",
            dataType: "json",
            url: $SCRIPT_ROOT + '/receive_verif',
            data: data
        }).done(function(data){

            if(data.errors) {

                $("#verif").modal("hide");
                $('.errors-detail').text(data.errors).show();
                $("#error").modal("show");

            }

            else {
                
                $("#verif").modal("hide");
                $("#intro").modal("show");
            }
        }); 
    });
});
