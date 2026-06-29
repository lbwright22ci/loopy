$(document).ready(function(){

    $(".dropdown").on("mouseover", function(){
        element = $(this);
        element.children("ul:first-of-type").addClass("show");
    });

    $(".dropdown").on("mouseleave", function(){
        $("ul:first-of-type").removeClass("show");
    });

});