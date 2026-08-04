$(document).ready(function () {

  var comments = $('textarea');
  for(var i=0; i< comments.length; i++){
    var cc = $('textarea').eq(i).val().trim();
    $('textarea').eq(i).val(cc);
  }

  $('.1').click(function(){
    $(this).nextAll().removeClass('fa-solid').addClass('fa-regular');
    $(this).removeClass('fa-regular').addClass('fa-solid');
    $(this).next("input[name='rating']").attr('value', 1);
  });
  $('.2').click(function(){
    $(this).nextAll().removeClass('fa-solid').addClass('fa-regular');
    $(this).removeClass('fa-regular').addClass('fa-solid');
    $(this).prevAll().removeClass('fa-regular').addClass('fa-solid');
    $(this).closest("input[name='rating']").attr('value', 2);
  });
  $('.3').click(function(){
    $(this).nextAll().removeClass('fa-solid').addClass('fa-regular');
    $(this).removeClass('fa-regular').addClass('fa-solid');
    $(this).prevAll().removeClass('fa-regular').addClass('fa-solid');
    $(this).closest("input[name='rating']").attr('value', 3);
  });
  $('.4').click(function(){
    $(this).nextAll().removeClass('fa-solid').addClass('fa-regular');
    $(this).removeClass('fa-regular').addClass('fa-solid');
    $(this).prevAll().removeClass('fa-regular').addClass('fa-solid');
    $(this).closest("input[name='rating']").attr('value', 4);
  });
  $('.5').click(function(){
    $(this).removeClass('fa-regular').addClass('fa-solid');
    $(this).prevAll().removeClass('fa-regular').addClass('fa-solid');
    $(this).closest("input[name='rating']").attr('value', 5);
  });

  $('.feedback').click(function(e){
        var form = $(this).closest('.feedback-form');
        form.submit();
        $(this).closest('.feedback-form').prop('disabled');
        });
});
