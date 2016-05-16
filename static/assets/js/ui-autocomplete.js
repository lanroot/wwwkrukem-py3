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

            var v = ui.item.value;

            // Set autocomplete element to display the label
            this.value = ui.item.label;

            // Store value in hidden field
            $('#hidden_field').val(ui.item.value);

            document.location.href="/ru/userdir/get/" + v + "/";

            // Prevent default behaviour
            return false;
        }
    });
})
