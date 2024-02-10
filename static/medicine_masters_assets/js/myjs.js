// let shoppingCart = document.querySelector('.shopping-cart');

// document.querySelector('#cart-btn').onclick = () =>
// {
//     shoppingCart.classList.toggle('active');
// }



$("#login").click(
    function(){
        $("#signuppage").removeClass("d-block").addClass("d-none");
        $("#loginpage").addClass("d-block").removeClass("d-none");
    }
);

$("#registration").click(
    function(){
        $("#loginpage").removeClass("d-block").addClass("d-none");
        $("#signuppage").addClass("d-block").removeClass("d-none");
    }
);

$(document).ready(function(){
    $("#table").dataTable();
});