$(function(){

    $('#btnflip').on('click', function(e){
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


});
