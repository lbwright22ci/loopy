$(document).ready(function(){

    $(".dropdown").on("mouseover", function(e){
        e.preventDefault();
        element = $(this);
        element.children("ul:first-of-type").addClass("show");
    });

    $(".dropdown-menu").on("mouseleave", function(e){
        e.preventDefault();
        $("ul:first-of-type").removeClass("show");
    });

    $('#basket').click(function(e){
        e.preventDefault();
        $('#show-basket').toggleClass('d-none');
    });

    $('#basket-mob').click(function(e){
        e.preventDefault();
        $('#show-basket').toggleClass('d-none');
    });

    $('#show-basket').on('mouseleave', function(e){
        e.preventDefault();
        $(this).toggleClass('d-none');
    });

    $(document).mouseup(function(e){
        if(!$("#show-basket").hasClass("d-none")){
            if($(e.target).closest("#show-basket").length===0){
                $('#show-basket').addClass("d-none");
            };
        };
    });

    $('.toast').toast('show');

    $('.to-top-link').click(function(e) {
		window.scrollTo(0,0);
	});

});