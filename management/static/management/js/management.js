$(document).ready(function () {

    var val = $('input[name="bulk"]:checked').val();
        if(val == 'freeshipping'){
            $('#shipping-offer').show();
            $('#bulk-offer').hide();
        }
        else{
            $('#shipping-offer').hide();
            $('#bulk-offer').show();
        }

    $('#which').on('change', 'input[name="bulk"]', function(){
        var val = $('input[name="bulk"]:checked').val();
        if(val == 'freeshipping'){
            $('#shipping-offer').show('slow');
            $('#bulk-offer').hide('slow');
        }
        else{
            $('#shipping-offer').hide('slow');
            $('#bulk-offer').show('slow');
        }
    })



})