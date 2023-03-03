import {chartGenerator, setChartConfig} from "../../../../static/js/base.js";

export class ChartBuilder {
    constructor() {

    }
    static build(chartData, chartTitles, chartIdArray) {
        let configs = [];
        chartData.forEach((chartDataItem, i=0) => {
            configs.push(setChartConfig(chartTitles[i], chartDataItem)); i++;
        })

        let charts = [];
        configs.forEach((config, i=0) => {
           charts.push(chartGenerator(chartIdArray[i], config));
           i++;
        });

        return charts;
    }
}