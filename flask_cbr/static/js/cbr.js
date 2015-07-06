$("#commandForm").submit(function (event) {
    event.preventDefault();
    $form = $(this);
    var info = $("#executingAlert");
    info.show();
    $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize(),
        success: function (data) {
            $("#commandOutput").text(data);
            info.hide();
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            info.hide();
            $("#commandOutput").text(errorThrown);
        }

    });
});

$("#gitPullForm").submit(function (event) {
    event.preventDefault();
    $form = $(this);
    var info = $("#executingAlert");
    info.show();
    $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize(),
        success: function (data) {
            $("#commandOutput").text(data);
            info.hide();
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            info.hide();
            $("#commandOutput").text(errorThrown);
        }

    });
});