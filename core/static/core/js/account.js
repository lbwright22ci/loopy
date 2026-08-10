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
    }); 

    $('.refund_link').click(function(e){
        var csrfToken = $(this).data('csrf');
        var orderNum = $(this).data('order_num');
        var amount = parseFloat($(this).data('total'));
        var stripePid = $(this).data('pid');
        var url = `/checkout/cancel/${orderNum}/`;

        var data = {
            'csrfmiddlewaretoken': csrfToken,
            'amount':amount,
            'reason':'customer cancelled order',
            'stripe_pid': stripePid,
        };

        $.post(url, data).done(function() {
                location.reload();
            });
    });
})