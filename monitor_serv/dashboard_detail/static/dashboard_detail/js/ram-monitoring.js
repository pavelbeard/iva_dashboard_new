import {chartUpdate, setChartData, setChartConfig, chartGenerator, formatBytes} from "../../../../static/js/base.js";
import {ChartBuilder} from "./chart-builder.js";

window.onload = async function () {
    const chartData = JSON.parse(document.getElementById("chartData").textContent);
    const titles = ["Всего ОЗУ, bytes", "Мониторинг ОЗУ, bytes"];
    const chartIdArray = ["lineChartRam1", "lineChartRam2"];

    const charts = ChartBuilder.build(chartData, titles, chartIdArray);

    setInterval(chartUpdate, 5000, 'ram-url', charts);
}