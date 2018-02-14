$(function() {
    $('body').on('click', 'button.delete', function () {
        var del = $(this).attr('data-value');
        $.ajax({
            url: '/api/delete_product/' + del,
            type: 'DELETE',
            success: function () {
                $('div.card-number-' + del).fadeOut(2000, function () {
                    $(this).remove();
                });
            },
            error: function (error) {
                console.log(error);
                alert('error deleting product');
            }
        });
    });

});