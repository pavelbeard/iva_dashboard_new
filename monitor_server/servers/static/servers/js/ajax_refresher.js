$(document).ready(function () {
    // current url /metrics/
    function getMetrics(url) {
        $.ajax({
            url: "metrics/processes",
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

    setInterval(getMetrics, 5000)
})