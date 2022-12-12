$(document).ready(function () {
    let counter = 0

    $("#add-servers").click(function () {
        $('#add-servers').text("Server is added: " + counter++)
    });
})