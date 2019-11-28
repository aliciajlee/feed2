$(document).ready(function () {
    $(".rating").each(function () {
        let rating = $(this).attr("data-rating");
        // console.log(rating);
        let txt = parseInt(rating);
        $(this).text(String.fromCodePoint(0x2b50).repeat(txt)); // star emoji
    });

    $(".price").each( function() {
        let price = $(this).attr("data-price");
        let txt = parseInt(price)
        console.log(price)
        $(this).text(String.fromCodePoint(0x0024).repeat(txt)); // dollar sign emoji
    })
  });

// (function () {
    
// })();


