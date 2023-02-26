export const headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
};

export function setChartConfig(title, data) {
    return  {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            size: 14,
                        }
                    }
                },
                title: {
                    display: true,
                    text: title,
                    font: {
                        size: 14
                }
            },
        },
        scales: {
            yAxes: [{
                display: true,
                    gridLines: {
                        color: "rgb(210,210,211)"
                    },
                    ticks: {
                        max: 100,
                        min: 0,
                        padding: 20
                    }
                }],
                xAxes: [{
                    type: 'time',
                    time: {
                        displayFormats: {
                            hour: 'HH:mm',
                            minute: 'HH:mm',
                            second: 'HH:mm:ss',
                            millisecond: 'HH:mm:ss.SS',
                            quarter: 'MMM YYYY',
                        }
                    },
                }]
            }
        }
    };
}