$(document).ready(function () {

    function getMetrics() {
        $.ajax({
            url: "/processes/",
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