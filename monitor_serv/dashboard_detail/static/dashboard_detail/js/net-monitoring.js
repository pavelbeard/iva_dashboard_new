import {chartUpdate, setChartData, setChartConfig, chartGenerator} from "../../../../static/js/base.js";
import {ChartBuilder} from "./chart-builder.js";

window.onload = async function () {
    const chartData = JSON.parse(document.getElementById("chartData").textContent);
    const titles = ["Принято/передано информации, bytes",
                    "Принято/передано пакетов, bytes",
                    "Ошибок"];
    const chartIdArray = ['lineChartNet1', 'lineChartNet2', 'lineChartNet3', ];

    const charts = ChartBuilder.build(chartData, titles, chartIdArray)

    setInterval(chartUpdate, 5000, 'net-url', charts);
}