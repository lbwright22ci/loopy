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

    $('.swatches').click(function(){
        var colourId = $(this).data('colvar_id');
        addHightlight(colourId);
        window.scrollTo(20,0);
        changeSelected(colourId);
        displaySwatch(colourId);
    });

    $('#colour-options-form').change(function(){
        var colourId = $(this).val();
        addHightlight(colourId);
        displaySwatch(colourId);
    });

})