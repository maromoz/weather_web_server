function armDeleteButtons(){
    $(".delete_button").click(function () {
        var id = $(this).parents(".main").attr('id');
        $(this).parents(".main").remove();
        $.ajax({
            method: 'POST',
            url: '/delete_id_from_db/',
            data: {id: id},
            success: function () {
            }
        });
    });
}

$(document).ready(function () {
    armDeleteButtons();

    $('#add_button').click(function () {
        var city = $('#add_to_db').val();
        $.ajax({
            method: 'POST',
            url: '/add_id_to_db/',
            data: {city: city},
            success: function (element_to_add) {
                $("#before_first_main").after(element_to_add);
                armDeleteButtons();
            }
        });
    });
    $('#add_to_db').on('keyup', function () {
        if (this.value.length > 0) {
            console.log(this.value);
            var text_to_complete = this.value;
            $.ajax({
                method: 'GET',
                url: '/get_auto_complete_cities/',
                data: {"text": text_to_complete},
                success: function (response) {
                    var possible_names = response["possible_cities"];
                    $("#add_to_db").autocomplete({source:possible_names});
                }
            })
        }
    });

});
