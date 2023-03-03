import {chartUpdate, setChartData, setChartConfig, chartGenerator} from "../../../../static/js/base.js";
import {ChartBuilder} from "./chart-builder.js";



window.onload = async function () {
    const chartData = JSON.parse(document.getElementById("chartData").textContent);
    const titles = ["Мониторинг CPU"];
    const chartIdArray = ["lineChartCpu"];

    const charts = ChartBuilder.build(chartData, titles, chartIdArray)

    setInterval(chartUpdate, 5000, 'cpu-url', charts);
}