$(document).ready(function () {
    function getMetrics() {
        $.ajax({
            url: "metrics/",
            method: "GET",
            dataType: "json",
            success: (data) => {
                $(".servers").text(data)
            },
            error: (data) => {
                $(".servers").text(data.error)

            }

        })
    }

    getMetrics()
})