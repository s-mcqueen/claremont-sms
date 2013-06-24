 
    var flip = flippant.flip;
    var toFlip = document.getElementById('btnflip');

    toFlip.addEventListener('click', function(e){
            e.preventDefault();

            var flipper = document.getElementById('signup');
            var back;
            var textarea = '<h1 style="color: #1ABC9C;"> Thanks! </h1>'

            var modal = '<h1 style="color: #1ABC9C;"> Thanks! </h1>\
            <p>You should receive an SMS confirmation shortly. <p>Send a \
            text to your friend by providing their first and last name followed \
            by a colon and the message you would like to send. For example:</p> \
            <div class="well well-small"><p>Sean McQueen: You are such a dream \
            boat! </p></div><p>If your friend has an account with Claremont SMS, \
            they will receive an anonymous text to their phone.</p><p>When you\
            receive a text, it might look something like this:</p><div class="well\
            well-small"><p>You are such a dream boat! (27281)</p></div><p>You have the \
            opportunity to guess who sent you that text by responding with the \
            five-digit ID number that follows your text. For example:<p><div \
            class="well well-small"><p>27281: Evan Casey</p></div><p>If you guess \
            correctly, we will let you know!</p>'

            back = flip(flipper, modal);

            back.addEventListener('click', function(e){
                event.trigger(back, 'close');
            })
    
    })

