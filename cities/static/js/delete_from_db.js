$(document).ready(function() {
  $("button").click(function () {
      var id = $(this).parents(".main").attr('id');
      $(this).parents(".main").remove();
      $.ajax({
        method: 'POST',
        url: '/delete_id_from_db/',
        data: { id: id },
        success: function() {
        }
      });
  });

});
