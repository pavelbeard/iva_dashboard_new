import {chartUpdate, setChartData, setChartConfig, chartGenerator, formatBytes} from "../../../../static/js/base.js";
import {ChartBuilder} from "./chart-builder.js";

window.onload = async function () {
    const chartData = JSON.parse(document.getElementById("chartData").textContent);
    const titles = ["Размер файловой системы, bytes", "Занято места, bytes", "Доступно места, bytes"];
    const chartIdArray = ["lineChartDisk1", "lineChartDisk2", "lineChartDisk3"];

    // let cb = function (value, index, values) {
    //     return formatBytes(value);
    // };

    const charts = ChartBuilder.build(chartData, titles, chartIdArray);

    setInterval(chartUpdate, 5000, 'disk-url', charts);
}