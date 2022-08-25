$(document).ready(function () {

    $('.add-to-cart').click(function (e) {
        e.preventDefault()
        const product_id = $(this).closest('.product_data').find('.prod_id').val(); // add to cart for multiple objects on page
        const token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: "POST",
            url: "/cart/add-to-cart-ajax",
            data: {
                'prod_id': product_id,
                csrfmiddlewaretoken: token
            },
            dataType: "json",
            success: function (response) {
                $('#message').replaceWith($(response.html));
            }
        })
    });

    $('.decr_prod').click(function (e) {
        e.preventDefault()
        const product_id = $(this).closest('.prod_info').find('.prod_id').val(); // decrement quantity for multiple objects on page
        const token = $('input[name=csrfmiddlewaretoken]').val();
        const action = 'decrement'
        $.ajax({
            type: "POST",
            url: "/cart/manage-cart-ajax",
            data: {
                'prod_id': product_id,
                'action': action,
                csrfmiddlewaretoken: token
            },
            dataType: "json",
            success: function (response) {
                if (response.data == undefined) {
                    $('#message').replaceWith($(response.html));
                }
                else {
                    var quantity = response.data.quantity
                    var subtotal = response.data.subtotal
                    var final_price = response.data.final_price
                    var quantity_id = '#quantity_'+product_id
                    var subtotal_id = '#subtotal_'+product_id
                    $(quantity_id).html(quantity);
                    $(subtotal_id).html(subtotal);
                    $('#final_price').html(final_price);
                }
            }
        })
    });
    $('.incr_prod').click(function (e) {
        e.preventDefault()
        const product_id = $(this).closest('.prod_info').find('.prod_id').val(); // increment quantity for multiple objects on page
        const token = $('input[name=csrfmiddlewaretoken]').val();
        const action = 'increment'
        $.ajax({
            type: "POST",
            url: "/cart/manage-cart-ajax",
            data: {
                'prod_id': product_id,
                'action': action,
                csrfmiddlewaretoken: token
            },
            dataType: "json",
            success: function (response) {
                if (response.data == undefined) {
                    $('#message').replaceWith($(response.html));
                }
                else {
                    var quantity = response.data.quantity
                    var subtotal = response.data.subtotal
                    var final_price = response.data.final_price
                    var quantity_id = '#quantity_' + product_id
                    var subtotal_id = '#subtotal_' + product_id
                    $(quantity_id).html(quantity);
                    $(subtotal_id).html(subtotal);
                    $('#final_price').html(final_price);
                }
            }
        })
    });
    $('.remove_prod').click(function (e) {
        e.preventDefault()
        const product_id = $(this).closest('.prod_info').find('.prod_id').val(); // delete from cart for multiple objects on page
        const token = $('input[name=csrfmiddlewaretoken]').val();
        const action = 'remove'
        $.ajax({
            type: "POST",
            url: "/cart/manage-cart-ajax",
            data: {
                'prod_id': product_id,
                'action': action,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                $('#product_' + product_id).remove();
                var final_price = response.data.final_price
                $('#final_price').html(final_price);
                $('#message').replaceWith($(response.html));
                if (final_price == 0) {
                    $('#checkout').remove();
                }
            }
        });
    });

    $('.product-favourite').click(function(e) {
        e.preventDefault()
        const product_id = $(this).closest('.product_data').find('.prod_id').val();
        const token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: "POST",
            url: "/product/add-to-favourite",
            data: {
                'prod_id': product_id,
                csrfmiddlewaretoken: token
            },
            dataType: "json",
            success: function (response) {
                $('#favourite').replaceWith($(response.html));
            },
        })
    })
})
