$(document).ready(function() {
    console.log("loaded post.js");

   $("#like").click(function() {
        if ($(this).attr("data-liked")=="False") {
            console.log("liked");
            $(this).css("color", "#EF3B3A");
            $(this).attr("data-liked", "True");
            // ajax stuff here
        } else {
            console.log("unliked");
            $(this).css("color", "#5d5d5d");
            $(this).attr("data-liked", "False");
            // ajax stuff here
        }
   });
})