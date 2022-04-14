(function($) {
  'use strict';
  $('#exampleModal-4').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var modal = $(this)
    modal.find('.modal-body input[name="namesh"]').val(button.data('d1'))
    modal.find('.modal-body input[name="emailsh"]').val(button.data('d2'))
    modal.find('.modal-body input[name="eid"]').val(button.data('d3'))
    $("#md21").attr("href",`mobile/delete/${button.data('d3')}/`)
  })
})(jQuery);