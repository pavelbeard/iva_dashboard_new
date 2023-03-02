import {chartUpdate, setChartData, setChartConfig, chartGenerator} from "../../../../static/js/base.js";



window.onload = async function () {
    const chartData = JSON.parse(document.getElementById("chartData").textContent);

    const config = setChartConfig("Мониторинг CPU", chartData);

    const chartId = 'lineChartCpu';
    const chart = chartGenerator(chartId, config);

    // TODO: перевести в файлы скриптов обработчики данных для графиков: RAM, Disk, Net
    // TODO: создать обработчики данных для графиков: load average

    setInterval(chartUpdate, 5000, 'cpu-url', chart)
}