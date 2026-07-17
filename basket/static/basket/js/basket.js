$(document).ready(function () {

    function handleEnableDisable(colourId){
        var currentvalue = parseInt($('[data-item_id ="'+colourId+'" ]').val());
        var plusLimit = parseInt($('[data-item_id ="'+colourId+'" ]').attr('max'));
        var minusDisabled = currentvalue < 2;
        var plusDisabled = currentvalue > plusLimit-1;
        $('[data-item-id-plus= "'+colourId+'" ]').prop('disabled', plusDisabled);
        $('[data-item-id-minus= "'+colourId+'" ]').prop('disabled', minusDisabled);
    };

    // check all input fields plus and minus buttons are correct on page load: required for basket page
    var allQtyInputs = $('.qty-input');
    for(var i = 0; i < allQtyInputs.length; i++){
        var colourId = $(allQtyInputs[i]).data('item_id');
        handleEnableDisable(colourId);
    };


    $('.increment-qty').click(function() {
       var closestInput = $(this).closest('.input-group').find('.qty-input')[0];
       var currentValue = parseInt($(closestInput).val());
       $(closestInput).val(currentValue + 1);
       var colourId = $(this).data('item-id-plus');
       handleEnableDisable(colourId);
    });

    $('.decrement-qty').click(function() {
       var closestInput = $(this).closest('.input-group').find('.qty-input')[0];
       var currentValue = parseInt($(closestInput).val());
       $(closestInput).val(currentValue - 1);
       var colourId = $(this).data('item-id-minus');
       handleEnableDisable(colourId);
    });

    $('.qty-input').change(function(){
        var colourId = $(this).data('item_id');
        handleEnableDisable(colourId, );
    });

    $('.update').click(function(e) {
        var form =$(this).closest('.update-form');
        console.log(form);
        form.submit();
    });


})