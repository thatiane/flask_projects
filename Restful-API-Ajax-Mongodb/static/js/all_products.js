$(function() {
    // $('body').on('click', 'button.delete', function () {
    //     console.log($(this).attr('data-value'));
    // });
    $.ajax({
        url: '/api/all_products',
        type: 'GET',
        success: function (products) {
            console.log(products);
            $('span.loading').remove();
            $.each(products, function (p, product) {
                $('.cards-warpper').append('<div class="card card-number-'  + product.id + '">\n' +
                    '<button class="delete" title="Delete Product" data-value="' + product.id + '">Delete</button>' +
                    '<button class="edit" title="Edit Product" data-id="' + product.id + '">Edit</button>' +
                    '<button class="save" title="Save Edit" style="display: none;" data-id="' + product.id + '">Save</button>' +
                    '<button class="cancel" title="Cancel Edit" style="display: none;" data-id="' + product.id + '">Cancel</button>' +
                    '<div class="id">' + product.id + '</div>\n' +
                    '<h1 class="product_name">Name: ' + product.product_name + '</h1>\n' +
                    '<h5 class="price">Price: ' + product.price + '</h5>\n' +
                    '<h5 class="quantity">Quantity: ' + product.quantity + '</h5>\n' +
                    '<h5>Number of views: ' + product.number_of_views + '</h5>\n' +
                    '<h5>Number of sales: ' + product.number_of_sales + '</h5>\n' +
                    '<h5>Files: ' + product.files + '</h5>\n' +
                    '<h5 class="discount">Discount: ' + product.discount + '</h5>\n' +
                    '<h5 class="description" style="overflow: hidden;">Description: ' + product.description + '</h5>\n' +
                    '<h5>Create date: ' + product.create_date + '</h5>\n' +
                    '<h5 class="category">Category: ' + product.category + '</h5>\n' +
                    '</div>');
            });
        },
        error: function (error) {
            console.log(error);
            alert('error loading products information');
        }
        //     products.forEach((item) => {
        //         $('.cards-warpper').append(`
        //             <div class="card">
        //                 <div class="id">${item.id}</div>
        //                 <h1>Name: ${item.product_name}</h1>
        //                 <h5>Price: ${item.price}</h5>
        //                 <h5>Quantity: ${item.quantity}</h5>
        //                 <h5>Number of views: ${item.number_of_views}</h5>
        //                 <h5>Number of sales: ${item.number_of_sales}</h5>
        //                 <h5>Files: ${item.files}</h5>
        //                 <h5>Discount: ${item.discount}</h5>
        //                 <h5 style="overflow: hidden;">Description: ${item.description}</h5>
        //                 <h5>Create date: ${item.create_date}</h5>
        //                 <h5>Category: ${item.category}</h5>
        //             </div>
        //         `)
        // })
        // },
        // error: function (error) { // if ajax couldn't get the data for some resone it will run this function
        //     console.log(error)
        // }
    });

});