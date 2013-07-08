var $new_user_data,
    verif_code;

$(function(){

    // home page signup button
    $('#signup-btn').on('click', function(e){
        e.preventDefault();

        $new_user_data = $('#signup-form').serialize()
        $.ajax({
            type: "POST",
            dataType: "json",
            url: $SCRIPT_ROOT + '/signup',
            data: $new_user_data
        }).done(function(data) {

            if(data.errors) {

                $('.signup-errors').text(data.errors).show();
                $("#error").modal("show");
            }

            else {

                $("#verif").modal("show");
            }           
        });

    });

    // if verif modal open, send the user the verification code
    if ($('#verif').attr('aria-hidden') == 'false') {

        console.log("here");

        $.ajax({
            type: "POST",
            dataType: "json",
            url: $SCRIPT_ROOT + '/send_verif',
            data: $new_user_data
        })
    }

    $('#verif-btn').on('click', function(e){
        e.preventDefault();

        $.ajax({
            type: "GET",
            dataType: "json",
            url: $SCRIPT_ROOT + '/verify',
            data: $('#verif-form').serialize()
        }).done(function(data){

            if(data.errors) {
                console.log(data.errors);

                $('.signup-errors').text(data.errors).show();
                $("#error").modal("show");

            }

            else {
                console.log("success")

                $("#intro").modal("show");
            }
        }); 
    });
});
