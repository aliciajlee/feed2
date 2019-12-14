$(document).ready(function() {
    console.log("loaded post.js");

   $("#like").click(function() {
        if ($(this).attr("data-liked")=="False") {
            console.log("liked");
            $(this).css("color", "#EF3B3A");
            // $("#like-text").text("Unlike");
            $(this).attr("data-liked", "True");
            // ajax stuff here
        } else {
            console.log("unliked");
            $(this).css("color", "#5d5d5d");
            // $("#like-text").text("Like");
            $(this).attr("data-liked", "False");
            // ajax stuff here
        }
   });
})