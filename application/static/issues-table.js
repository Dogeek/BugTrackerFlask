$(".upvote").click(function(event) {
    var classId = event.target.className;
    $.post("/voting/upvote/" + classId.split(/-/)[2]);
});

$(".downvote").click(function(event) {
    var classId = event.target.className;
    $.post("/voting/downvote/" + classId.split(/-/)[2]);
});

$(".table-row").click(function(event) {
    var id = event.target.parentElement.className.split(/table-row-(\d+)/)[1];
    if (id != undefined) {
        window.location.href = "/issue/" + id;
    }
});