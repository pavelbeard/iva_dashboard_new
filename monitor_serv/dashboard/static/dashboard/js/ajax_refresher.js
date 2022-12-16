$(document).ready(function () {
    // current url /dashboard/
    function drawTable(data) {
        let obj = JSON.parse(data)
        for (let o in obj) {
            $('.servers-2').append('div').attr('id', `row-${o}`).addClass('row').text(obj[o].hostname)
            // console.log(obj[o].hostname)
            // console.log(obj[o].data)
            for (let i in obj[o].data) {
                console.log(obj[o].data[i].status)
                console.log(obj[o].data[i].service)
            }
        }
    }

    function getMetrics(url) {
        $.ajax({
            url: url,
            method: "GET",
            dataType: "json",
            success: (data) => {
                drawTable(data)
            },
            error: (data) => {
                $(".servers").text(data.error)
            }

        })
    }

    setInterval(getMetrics, 5000, "processes/");
})