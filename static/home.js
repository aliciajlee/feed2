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
    });

    $("#sort-by-form").on("submit", function(e) {
        alert("fuck");
        e.preventDefault();
        var s = $("#sort-by").val();
        console.log(s);
    });

    $("#tag-form").on("submit", function(e) {
        e.preventDefault();
        var t = $("#tag").val();
        console.log(t);
    });

    $("#sort-by").change(function () {
        console.log(this.value);
    })
  });


