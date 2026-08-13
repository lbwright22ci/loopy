$(document).ready(function () {

    var val = $('input[name="bulk"]:checked').val();
        if(val == 'freeshipping'){
            $('#shipping-offer').show();
            $('#bulk-offer').hide();
        }
        else{
            $('#shipping-offer').hide();
            $('#bulk-offer').show();
        };

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
    });

    $('#bulk').click(function(){
        var errorMessage ="";
        var error =0;
        var displayError = $('#error-messages');

        if($('#id_lower_ball_num').val() > $('#id_upper_ball_num').val()){
            errorMessage += "Lower threshold must be less than upper threshold";
            error += 1;
        };
        if($('#id_lower_discount').val > $('#id_upper_discount').val()){
            errorMessage += "Lower discount must be less than upper discount";
            error +=1;
        };
        displayError.text(errorMessage);

        if(error==0){
            var form = $(this).closest(('#bulk-offer'));
            form.submit();
        }

    })


})