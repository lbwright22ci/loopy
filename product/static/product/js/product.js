$(document).ready(function () {
    $('.sort-selector').change(function () {
        var selector = $(this);
        var currentUrl = new URL(window.location);

        var selectedVal = selector.val();

        if (selectedVal != "reset") {
            var sort = selectedVal.split('_')[0];
            var direction = selectedVal.split('_')[1];

            currentUrl.searchParams.set('sort', sort);
            currentUrl.searchParams.set('direction', direction);
            window.location.replace(currentUrl);

        } else {
            currentUrl.searchParams.delete('sort');
            currentUrl.searchParams.delete('direction');
            window.location.replace(currentUrl);
        }
    });

    $('#clip-swatches').click(function(e) {
        var hiddenText = "Show more...";
        var revealedText = "Show less...";

        var initialState = $(this).text();

        $('.swatches-hidden').toggle('slow');

        if (initialState == hiddenText) {
            $(this).text(revealedText);
        } else {
            $(this).text(hiddenText);
        };
    });

    function addHightlight(colourId){
        var allSwatch = $('.swatches');
        for (var i=0; i<allSwatch.length; i++){
            var itemId = $(allSwatch[i]).data('colvar_id');
            if (itemId != colourId){
                $(allSwatch[i]).removeClass('selected-colour-option');
            } else {
                $(allSwatch[i]).addClass('selected-colour-option');
            };
        };
    };

    function changeSelected(colourId){
        $('form select[name=colour_var]').val(colourId).change();
    };

    function displaySwatch(colourId){
        var src = $(`.colvar_id_${colourId}`).attr('src');
        var altText = $(`.colvar_id_${colourId}`).attr('src');
        $('.mini-selected-swatch').html(`<img src=${src} alt=${altText} class='img-mini-selected'>`);
    };

    function displayQuantityField(colourId, colLS){
        var maxBalls = 0;
        if (colLS == true ){
            maxBalls = 10;
            $('#low-stock-warning').text('Low Stock! Max. 10 balls per customer only');
        } else {
            maxBalls = 50;
            $('#low-stock-warning').text('');
        }
        $('#quant-in').removeClass('d-none');
        
        $('.decrement-qty').attr('data-item-id-minus', `${colourId}`);
        
        $('.increment-qty').attr('data-item-id-plus', `${colourId}`);

        $('.qty-input').attr('data-item_id', `${colourId}`);
        $('.qty-input').attr('max', `${maxBalls}`);
    };

    function resetQuantityField(){
        $('#quant-in').addClass('d-none');
        $('.mini-selected-swatch').attr('colour', 0);
        $('.decrement-qty').attr('data-item-id-minus', 0);
        $('.increment-qty').attr('data-item-id-plus', 0);
        $('.qty-input').attr('data-item_id', 0);
        $('.qty-input').attr('max', 0);
        $('.qty-input').val(1);
        $('#low-stock-warning').text('');
        $('.mini-selected-swatch').html('');
    };

    function handleEnableDisable(colourId, colLS){
        var currentvalue = parseInt($('[data-item_id ="'+colourId+'" ]').val());
        var plusLimit =0
        if (colLS == true){
            plusLimit = 9;
        }else{
            plusLimit = 49;
        }
        var minusDisabled = currentvalue < 2;
        var plusDisabled = currentvalue > plusLimit;
        $('[data-item-id-plus= "'+colourId+'" ]').prop('disabled', plusDisabled);
        $('[data-item-id-minus= "'+colourId+'" ]').prop('disabled', minusDisabled);
    };

    // check all input fields plus and minus buttons are correct on page load: required for basket page
    var allQtyInputs = $('.qty-input');
    for(var i = 0; i < allQtyInputs.length; i++){
        var colourId = $(allQtyInputs[i]).data('item_id');
       var colLS=$(`.colvar_id_${colourId}`).data('col_ls');
        handleEnableDisable(colourId, colLS);
    };


    $('.swatches').click(function(){
        var colourId = $(this).data('colvar_id');
        
        var colLS = $(this).data('col_ls');

        addHightlight(colourId);
        
        window.scrollTo(20,0);
        changeSelected(colourId);
        // console.log('gets here');
        resetQuantityField();
        displaySwatch(colourId);
        displayQuantityField(colourId, colLS);
        handleEnableDisable(colourId, colLS);
    });


    $('#colour-options-form').change(function(){
        var colourId = $(this).val();
        var colLS=$(`.colvar_id_${colourId}`).data('col_ls');
        addHightlight(colourId);
        if (colourId == 0){
            resetQuantityField();
        }
        else{
        resetQuantityField();
        displaySwatch(colourId);
        displayQuantityField(colourId, colLS);
        handleEnableDisable(colourId, colLS);}
    });


    $('.increment-qty').click(function() {
       
       var closestInput = $(this).closest('.input-group').find('.qty-input')[0];
       var currentValue = parseInt($(closestInput).val());
       $(closestInput).val(currentValue + 1);
       var colourId = $(this).data('item-id-plus');
       var colLS=$(`.colvar_id_${colourId}`).data('col_ls');
       handleEnableDisable(colourId, colLS);
    });

    $('.decrement-qty').click(function() {
       
       var closestInput = $(this).closest('.input-group').find('.qty-input')[0];
       
       var currentValue = parseInt($(closestInput).val());
       $(closestInput).val(currentValue - 1);
       var colourId = $(this).data('item-id-minus');
       var colLS=$(`.colvar_id_${colourId}`).data('col_ls');
       handleEnableDisable(colourId, colLS);
    });

    $('.qty-input').change(function(){
        var colourId = $(this).data('item_id');
       var colLS=$(`.colvar_id_${colourId}`).data('col_ls');
       handleEnableDisable(colourId, colLS);
    });

})