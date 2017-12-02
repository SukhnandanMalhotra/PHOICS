

// $(document).ready(function() {
//     $('.display2').on('mousedown', function () {
//         var imgid;
//         console.log("from start to like");
//
//         imgid = $(this).attr("data-imgid");
//
//         $.get('/phoics/like/', {imgid: imgid}, function (data) {
//             console.log("5");
//             $('#count_like' + imgid).html(data);
//         })
//     })
// });
$(document).ready(function() {
    $('.display').on('click', function () {
        var imgid;
        console.log("hello");
        imgid = $(this).attr("img-id");
        $.get('/phoics/user_list/', {imgid: imgid}, function (data) {
            console.log("5+1");
            $('#user' + imgid).html(data);
        })
    })
});



