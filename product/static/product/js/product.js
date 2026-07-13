$(document).ready(function () {
    $('#sort-selector').change(function () {
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
        $('#quant-in').replaceWith(`<div  id="quant-in">
                                    <div class="input-group div-colour-select-form">
                                        <button class="decrement-qty btn btn-main" type="button" >
                                            <span >
                                                <i class="fas fa-minus"></i>
                                            </span>
                                        </button>
                                        <input id="quant-in" class="form-control" 
                                        type="number" name="quantity" value="1"  min="1" 
                                        max="${maxBalls}" data-item_id="${colourId}" >
                                        <button class="increment-qty btn btn-main" type="button">
                                            <span >
                                                <i class="fas fa-plus"></i>
                                            </span>
                                        </button>
                                    </div>
                                    <div class="text-center div-colour-select-form">
                                        <a type="submit" aria-label="" class="btn btn-main mb-4 mt-4" 
                                        role="button"> Add to basket</a>
                                    </div>
                                    </div>`)
    };

    function removeQuantityField(){
        $('#quant-in').replaceWith(`<div  id="quant-in"> </div>`);
        $('#low-stock-warning').text('');
        $('.mini-selected-swatch').html("");
    };

    $('.swatches').click(function(){
        var colourId = $(this).data('colvar_id');
        var colLS = $(this).data('col_ls');
        addHightlight(colourId);
        window.scrollTo(20,0);
        changeSelected(colourId);
        displaySwatch(colourId);
        displayQuantityField(colourId, colLS);
    });

    $('#colour-options-form').change(function(){
        var colourId = $(this).val();
        var colLS=$(`.colvar_id_${colourId}`).data('col_ls');
        addHightlight(colourId);
        if (colourId == 0){
            removeQuantityField();
        }
        else{
        displaySwatch(colourId);
        displayQuantityField(colourId, colLS);}
    });

})