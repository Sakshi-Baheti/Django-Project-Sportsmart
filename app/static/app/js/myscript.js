$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

/* Using AJAX/JQuery for increase or decrease the quantity in addtocart.html
*/

$('.plus-cart').click(function(){
    // pid is coming from addtocart.htmlhaving class plus-cart at line no 27
    var id = $(this).attr("pid").toString();
    // Current Object's Parent Node's 2nd child
    var element = this.parentNode.children[2] 
    $.ajax({
        type : "GET",
        url : "/pluscart",
        data:{
            prod_id : id
        },
        success : function(cart_data) {
            // Current Object's Parent Node's 2nd child
            element.innerText = cart_data.quantity
            document.getElementById("amount").innerText = cart_data.amount
            document.getElementById("totalamount").innerText = cart_data.totalamount
        }
    })
})


$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var element = this.parentNode.children[2] 
    $.ajax({
        type : "GET",
        url : "/minuscart",
        data:{
            prod_id : id
        },
        success : function(cart_data) {
            // Current Object's Parent Node's 2nd child
            element.innerText = cart_data.quantity
            document.getElementById("amount").innerText = cart_data.amount
            document.getElementById("totalamount").innerText = cart_data.totalamount
        }
    })
})



$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var element = this
    $.ajax({
        type : "GET",
        url : "/removecart",
        data:{
            prod_id : id
        },
        success : function(cart_data) {
            document.getElementById("amount").innerText = cart_data.amount
            document.getElementById("totalamount").innerText = cart_data.totalamount
            element.parentNode.parentNode.parentNode.parentNode.remove()

        }
    })
})
