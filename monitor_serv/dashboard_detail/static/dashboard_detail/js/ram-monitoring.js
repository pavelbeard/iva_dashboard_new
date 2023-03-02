import {chartUpdate, setChartData, setChartConfig, chartGenerator} from "../../../../static/js/base.js";

window.onload = async function () {
    const chartData = JSON.parse(document.getElementById("chartData").textContent);
    const titles = ["Всего ОЗУ, bytes", "Мониторинг ОЗУ, bytes"];
    const chartIds = ["lineChartRam1", "lineChartRam2"];

    let configs = [];
    chartData.forEach((chartDataItem, i=0) => {
        configs.push(setChartConfig(titles[i], chartDataItem));
        i++;
    });

    let charts = [];
    configs.forEach((config, i=0) => {
       charts.push(chartGenerator(chartIds[i], config));
       i++;
    });

    charts.forEach(chart => {
        setInterval(chartUpdate, 5000, 'ram-url', chart);
    });
}