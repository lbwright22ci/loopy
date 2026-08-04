$(document).ready(function () {

  var comments = $('textarea');
  for(var i=0; i< comments.length; i++){
    var cc = $('textarea').eq(i).val().trim();
    $('textarea').eq(i).val(cc);
  }


  $('.feedback').click(function(e){
        var form = $(this).closest('.feedback-form');
        form.submit();
        $(this).closest('.feedback-form').prop('disabled');
        });
});
