$(document).ready(function () {

    // set number of rating stars
    $(".rating").each(function () {
        let rating = $(this).attr("data-rating");
        // console.log(rating);
        let txt = parseInt(rating);
        $(this).text(String.fromCodePoint(0x2b50).repeat(txt)); // star emoji
    });

    // set number of dollar signs 
    $(".price").each( function() {
        let price = $(this).attr("data-price");
        let txt = parseInt(price)
        $(this).text(String.fromCodePoint(0x0024).repeat(txt)); // dollar sign emoji
    });

    // ??
    $("#tag-form").on("submit", function(e) {
        e.preventDefault();
        var t = $("#tag").val();
        console.log(t);
    });

   
  });


