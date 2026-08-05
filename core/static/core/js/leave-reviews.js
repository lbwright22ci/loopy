$(document).ready(function () {

  var comments = $('textarea');
  for(var i=0; i< comments.length; i++){
    var cc = $('textarea').eq(i).val().trim();
    $('textarea').eq(i).val(cc);
  }

  var rating = $('span[name=rating]');
  for(var i=0; i< rating.length; i++){
    var currentValue = parseInt($('span[name=rating]').eq(i).text().trim(1,-1));
    if(currentValue){
    
      if(currentValue==1){
        $('span[name=rating]').eq(i).prevAll('.1').removeClass('fa-regular').addClass('fa-solid');
      }
      else if(currentValue==2){
        $('span[name=rating]').eq(i).prevAll('.1, .2').removeClass('fa-regular').addClass('fa-solid');
      }
      else if(currentValue==3){
        $('span[name=rating]').eq(i).prevAll('.1, .2, .3').removeClass('fa-regular').addClass('fa-solid');
      }
      else if(currentValue==4){
        $('span[name=rating]').eq(i).prevAll('.1, .2, .3, .4').removeClass('fa-regular').addClass('fa-solid');
      }
      else if(currentValue==5){
      $('span[name=rating]').eq(i).prevAll('.1, .2, .3, .4, .5').removeClass('fa-regular').addClass('fa-solid');};
  };
  };

  $('.1').click(function(){
    $(this).nextAll().removeClass('fa-solid').addClass('fa-regular');
    $(this).removeClass('fa-regular').addClass('fa-solid');
    var yarn = $(this).data('yarn');
    var temp = `#rating-${yarn}`; 
    $(temp).text(1);
  });
  $('.2').click(function(){
    $(this).nextAll().removeClass('fa-solid').addClass('fa-regular');
    $(this).removeClass('fa-regular').addClass('fa-solid');
    $(this).prevAll().removeClass('fa-regular').addClass('fa-solid');
    var yarn = $(this).data('yarn');
    var temp = `#rating-${yarn}`; 
    $(temp).text(2);
  });
  $('.3').click(function(){
    $(this).nextAll().removeClass('fa-solid').addClass('fa-regular');
    $(this).removeClass('fa-regular').addClass('fa-solid');
    $(this).prevAll().removeClass('fa-regular').addClass('fa-solid');
    var yarn = $(this).data('yarn');
    var temp = `#rating-${yarn}`; 
    $(temp).text(3);
  });
  $('.4').click(function(){
    $(this).nextAll().removeClass('fa-solid').addClass('fa-regular');
    $(this).removeClass('fa-regular').addClass('fa-solid');
    $(this).prevAll().removeClass('fa-regular').addClass('fa-solid');
    var yarn = $(this).data('yarn');
    var temp = `#rating-${yarn}`; 
    $(temp).text(4);
  });
  $('.5').click(function(){
    $(this).removeClass('fa-regular').addClass('fa-solid');
    $(this).prevAll().removeClass('fa-regular').addClass('fa-solid');
    var yarn = $(this).data('yarn');
    var temp = `#rating-${yarn}`; 
    $(temp).text(5);
  });

  $('.feedback').click(function(e){
        var yarn =parseInt($(this).data('yarn'));
        var temp =`span[name=rating][data-yarn=${yarn}]`;
        var rating = $(temp).text();
        rating = parseInt(rating);
        var csrf=$(this).data('csrf');
        var order=$(this).data('order');
        var ttemp = `textarea[name=comment][data-yarn=${yarn}]`
        var comment = $(ttemp).val();

        if(!rating){
          $(`p[data-yarn=${yarn}]`).text('Have you forgotten to enter a star rating?');
        };
        if(!comment){
          $(`p[data-yarn=${yarn}]`).text('Please leave a comment to submit your feedback.');
        };
        if(rating && comment){
        var url = `/my_account/review/submit/${order}/`;

        var data ={
          'rating': rating,
          'comment':comment,
          'yarn':yarn,
          'csrfmiddlewaretoken':csrf,
        }
        $.post(url, data).done(function() {
                location.reload();
            });
}});
});
