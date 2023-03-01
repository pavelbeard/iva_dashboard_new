export const HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
};

export const COLOR_PALLET = [
	"#98e5fa", "#ee36f9", "#00bf00",
	"#0042ee", "#008600", "#6912b6",
	"#00f9db", "#6e00a1", "#005300",
	"#bf63ff", "#135e13", "#ff7bff",
	"#004900", "#dd8aff", "#ae8400",
	"#4b0085", "#00efff", "#930051",
	"#00edff", "#670046", "#00c1ff",
	"#745c00", "#2f36a0", "#ba614d",
	"#009aff", "#2e1f00", "#3d9cff",
	"#0d110b", "#ca7ce1", "#00395d",
	"#a2afff", "#004d71", "#003f94",
];

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

export function chartUpdate(urlId, ) {
    const url = document.getElementById(urlId).getAttribute('data-url');

}

export function chartGenerator(chartId, chartTitle, chartData) {
    const context = document.getElementById(chartId).getContext('2d');
    return new Chart(context, setChartConfig(chartTitle, chartData));
}
