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
    
    $('.refund-form').hide();

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

        if(parseInt($('#id_lower_ball_num').val()) >= parseInt($('#id_upper_ball_num').val())){
            errorMessage += "Lower threshold must be less than upper threshold.  ";
            error += 1;
        }
        if(parseInt($('#id_lower_discount').val()) >= parseInt($('#id_upper_discount').val())){
            errorMessage += "Lower discount must be less than upper discount";
            error +=1;
        }
        displayError.text(errorMessage);

        if(error==0){
            var form = $(this).closest('#bulk-offer');
            form.submit();
        }
    });

    $('.ship').click(function(){
        var form = $(this).closest('.ship-form');
        form.submit();
          });
    
    $('.reveal-refund').click(function(){
        $(this).hide('slow');
        $('.ship').hide('slow');
        $('.refund-form').show('slow');
    });

    $('.cancel-refund').click(function(){
        $('.refund-form').hide('slow');
        $('.reveal-refund').show('slow');
        $('.ship').show('slow');
    })

    $('.refund').click(function(){
        var form = $(this).closest('.refund-form');
        var pk = $(this).data('pk');
        var aS = `#amount-${pk}`;
        var eP = `#errors-${pk}`;
        var errorPara = $(eP);
        var maxAmount = parseFloat($(this).data('max'));
        var amountSubmitted = parseFloat($(aS).val());

        if(maxAmount < amountSubmitted ){
            var errorText = `The maximum amount you can refund for this order is £${maxAmount}`;
            $(eP).text( errorText);
        }
        else{
            form.submit();
        }
    });
});