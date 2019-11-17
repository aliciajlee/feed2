function displayRatings() {
    $(".rating").each(function () {
        rating = $(this).attr("data-rating");
        console.log(rating);
        txt = parseInt(rating);
        $(this).text(String.fromCodePoint(0x2b50).repeat(txt));
    });
}

displayRatings();