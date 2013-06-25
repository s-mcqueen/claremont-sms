$(function(){

    $('#signup-btn').on('click', function(e){
        e.preventDefault();

        $.ajax({
            type: "POST",
            dataType: "json",
            url: $SCRIPT_ROOT + '/signup',
            data: $('#signup-form').serialize()
        }).done(function(data) {

            if(data.errors) {
                console.log(data.errors);

                $('.signup-errors').text(data.errors).show();
                $("#error").modal("show");
            }

            else {
                console.log("success");

                $("#intro").modal("show");

            }           
        });

    });

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

                // do stuff
            }

            else {
                console.log("success")

                $("#signup-success").modal("show");
            }
        }); 
    });
});
