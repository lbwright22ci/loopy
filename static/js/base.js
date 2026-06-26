$(document).ready(function(){

    $(".dropdown").on("mouseover", function(){
        element = $(this);
        element.children("ul:first-of-type").addClass("show");
    });

    $(".dropdown").on("mouseleave", function(){
        $("ul:first-of-type").removeClass("show");
    });

    // $("#mobile-hamburger").on("click", function(){
    //     $("#expand-hambuger").toggleClass("show");
    // });

    // $("#user-toggle").on("click", function(){
    //     $("#user-toggle-reveal").toggleClass("show");
    //     $(this).toggleClass("show");
    //     state = $(this).attr('aria-expanded');
    //     if (state ==='true'){
    //         $(this).attr('aria-expanded','false');
    //     } else{
    //         $(this).attr('aria-expanded','true');
    //     };
    // });

    // $(document).mouseup(function(e){
    //     if($("#expand-hambuger").hasClass("show")){
    //         $("#yarn-menu-mobile").on("click", function(){
    //             $('#expand-hambuger').removeClass("show");
    //             $('#yarn-mobile-filter').addClass("show");
    //         });
    //         if($(e.target).closest("#expand-hambuger").length===0){
    //             $('#expand-hambuger').removeClass("show");
    //         };
    //     };
    //     if($("#yarn-mobile-filter").hasClass("show")){
    //         $("#mob-back-filter").on("click", function(){
    //             $('#yarn-mobile-filter').removeClass("show");
    //             $('#expand-hambuger').addClass("show");
    //         });
    //         if($(e.target).closest("#yarn-mobile-filter").length===0){
    //             $('#yarn-mobile-filter').removeClass("show");
    //         };
    //     };
    // });

});