$(document).ready(function () {

    $('.fav-icon').click(function(e){
        var csrfToken = $(this).data('csrf');
        var itemId = $(this).data('product_id');
        var url = `/yarns/fav/${itemId}/`;
        var data = {'csrfmiddlewaretoken': csrfToken};
        $.post(url, data)
            .done(function() {
                location.reload();
            });
    }) 

})