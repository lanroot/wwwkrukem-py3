$(document).ready(function() {
    $("input#id_q").autocomplete({
        source: function(request, response) {
            $.ajax({
                //dataType: "json",
                type: "GET",
                url: "/ru/userdir/search/autocomplete",
                data: { q: request.term },
                success: function(data) {
                    response(data);
                },
                /*
                error: function(data, textStatus) {
                    alert(data.statusText);
                }
                */
            });
        },
        minLength: 3,
        select: function(event, ui) {
            location.href="/ru/userdir/get/" + ui.item.value + "/";
        }
    });
})
