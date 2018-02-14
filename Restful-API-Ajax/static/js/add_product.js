$(function() {
    $('button.save').on('click', function () {

        var newProduct = {
            product_name: $('input.product_name').val(),
            price: $('input.price').val(),
            quantity: $('input.quantity').val(),
            discount: $('input.discount').val(),
            description: $('input.description').val(),
            category: $('input.category').val()
        };

        if(newProduct.product_name.length === 0){
            alert("you have not write a product name!");
            $('input.product_name').focus()}
        else if(newProduct.price.length === 0){
            alert("you have not write a price!");
            $('input.price').focus()}
        else if(newProduct.quantity.length === 0){
            alert("you have not write a quantity!");
            $('input.quantity').focus()}
        else if(newProduct.description.length <= 10){
            alert("your description is less than 10 letters!");
            $('input.description').focus()}
        else if(newProduct.category.length === 0){
            alert("you have not write a category!");
            $('input.category').focus()}

        else {
            $.ajax({
                url: '/api/add_product',
                type: 'POST',
                data: JSON.stringify(newProduct),
                contentType: 'application/json;charset=UTF-8',
                success: function (response) {
                    console.log(response, newProduct);

                    $('.cards-warpper').prepend('<div class="card">\n' +
                        '<div class="id">' + response.id + '</div>\n' +
                        '<h1>Name: ' + response.product_name + '</h1>\n' +
                        '<h5>Price: ' + response.price + '</h5>\n' +
                        '<h5>Quantity: ' + response.quantity + '</h5>\n' +
                        '<h5>Number of views: ' + response.number_of_views + '</h5>\n' +
                        '<h5>Number of sales: ' + response.number_of_sales + '</h5>\n' +
                        '<h5>Files: ' + response.files + '</h5>\n' +
                        '<h5>Discount: ' + response.discount + '</h5>\n' +
                        '<h5 style="overflow: hidden;">Description: ' + response.description + '</h5>\n' +
                        '<h5>Create date: ' + response.create_date + '</h5>\n' +
                        '<h5>Category: ' + response.category + '</h5>\n' +
                        '</div>');
                    $('input.product_name').val('');
                    $('input.price').val('');
                    $('input.quantity').val('');
                    $('input.discount').val('');
                    $('input.description').val('');
                    $('input.category').val('');
                },
                error: function (error) {
                    console.log(error);
                    alert('error saving product');
                }
            });
        }
    });

});