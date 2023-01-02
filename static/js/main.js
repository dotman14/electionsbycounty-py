
$(document).ready(function () {
    //Auto complete. Homepage and API Generate page.
    $("#id_county_state").autocomplete({
        minLength: 3,
        source: function (request, response) {
            $.ajax({
                url: "getcounty/",
                dataType: 'json',
                scroll: true,
                data: { prefix: request.term },
                success: function (data) {
                    response($.map(data.success, function (item) {
                        return { label: item , value: item };
                    }));
                }
            });
        }
    });
});
