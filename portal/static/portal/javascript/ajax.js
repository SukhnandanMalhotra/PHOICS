
$(document).ready(function() {
    $('.display1').on('click', function () {
        var imgid;
        var status;
        var text;
        console.log("hello");

        imgid = $(this).attr("data-imgid");

        $.get('/phoics/like/', {imgid: imgid, status: status}, function (data) {
            console.log("5+1");
            $('#count_like' + imgid).html(data);
            $('#hide' + imgid).text();
        })
    })
})
$(document).ready(function() {
    $('.display2').on('click', function () {
        var imgid;
        var status;
        var text;
        console.log("hello");

        imgid = $(this).attr("data-imgid");

        $.get('/phoics/like/', {imgid: imgid, status: status}, function (data) {
            console.log("5+1");
            $('#count_like' + imgid).html(data);
            $('#hide' + imgid).text();
        })
    })
})
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
})



