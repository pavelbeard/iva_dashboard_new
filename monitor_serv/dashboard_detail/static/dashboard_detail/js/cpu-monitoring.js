import {headers, setChartConfig} from "./base.js";

const labels = JSON.parse(document.getElementById("labels").textContent);

const data = {
    labels: labels,
    datasets: [
        {
            label: 'idle',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: JSON.parse(document.getElementById("cpu-idle-data").textContent)
        },
        {
            label: 'iowait',
            backgroundColor: 'rgb(128, 99, 132)',
            borderColor: 'rgb(128, 99, 132)',
            data: JSON.parse(document.getElementById("cpu-iowait-data").textContent)
        },
        {
            label: 'irq',
            backgroundColor: 'rgb(64, 99, 132)',
            borderColor: 'rgb(64, 99, 132)',
            data: JSON.parse(document.getElementById("cpu-irq-data").textContent)
        },
        {
            label: 'nice',
            backgroundColor: 'rgb(192, 99, 132)',
            borderColor: 'rgb(192, 99, 132)',
            data: JSON.parse(document.getElementById("cpu-nice-data").textContent)
        },
        {
            label: 'softirq',
            backgroundColor: 'rgb(255, 0, 132)',
            borderColor: 'rgb(255, 0, 132)',
            data: JSON.parse(document.getElementById("cpu-softirq-data").textContent)
        },
        {
            label: 'steal',
            backgroundColor: 'rgb(0, 64, 99)',
            borderColor: 'rgb(0, 64, 99)',
            data: JSON.parse(document.getElementById("cpu-steal-data").textContent)
        },
        {
            label: 'sys',
            backgroundColor: 'rgb(0, 128, 132)',
            borderColor: 'rgb(0, 128, 132)',
            data: JSON.parse(document.getElementById("cpu-sys-data").textContent)
        },
        {
            label: 'user',
            backgroundColor: 'rgb(9,182,255)',
            borderColor: 'rgb(9,182,255)',
            data: JSON.parse(document.getElementById("cpu-user-data").textContent)
        },
    ]
}


async function chartUpdate() {

    const response = await fetch($("#cpu-url").attr("data-url"), {
        method: "GET", headers: headers
    }).then(async resp => {
        return await resp.json();
    });

    window.lineChart.config.data.datasets[0].data = [];
    response['cpu_idle_data'].forEach(el => {
        window.lineChart.config.data.datasets[0].data.push(el);
    })
    window.lineChart.config.data.datasets[1].data = [];
    response['cpu_iowait_data'].forEach(el => {
        window.lineChart.config.data.datasets[1].data.push(el);
    })
    window.lineChart.config.data.datasets[2].data = [];
    response['cpu_irq_data'].forEach(el => {
        window.lineChart.config.data.datasets[2].data.push(el);
    })
    window.lineChart.config.data.datasets[3].data = [];
    response['cpu_nice_data'].forEach(el => {
        window.lineChart.config.data.datasets[3].data.push(el);
    })
    window.lineChart.config.data.datasets[4].data = [];
    response['cpu_softirq_data'].forEach(el => {
        window.lineChart.config.data.datasets[4].data.push(el);
    })
    window.lineChart.config.data.datasets[5].data = [];
    response['cpu_steal_data'].forEach(el => {
        window.lineChart.config.data.datasets[5].data.push(el);
    })
    window.lineChart.config.data.datasets[6].data = [];
    response['cpu_sys_data'].forEach(el => {
        window.lineChart.config.data.datasets[6].data.push(el);
    })
    window.lineChart.config.data.datasets[7].data = [];
    response['cpu_user_data'].forEach(el => {
        window.lineChart.config.data.datasets[7].data.push(el);
    })

    window.lineChart.config.data.labels = []
    response['record_dates'].forEach(el => {
        window.lineChart.config.data.labels.push(el)
    });

    window.lineChart.update();
}

window.onload = async function () {
    let ctx = document.getElementById('lineChart').getContext('2d');
    window.lineChart = new Chart(ctx, setChartConfig('Мониторинг CPU', data));

    // TODO: перевести в файлы скриптов обработчики данных для графиков: RAM, Disk, Net
    // TODO: создать обработчики данных для графиков: load average

    setInterval(chartUpdate, 5000)
}