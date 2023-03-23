import Chart from "chart.js/auto";
import {chartConfig} from "../../../base";
import React, {useEffect, useRef} from "react";
import zoomPlugin from 'chartjs-plugin-zoom';

Chart.register(zoomPlugin);

export const ChartComponent = () => {
    const chartRef = useRef();

    const createChart = () => {
        return new Chart(chartRef.current.getContext('2d'), chartConfig);
    }

    useEffect(() => {
        let chart = createChart();
        return () => chart.destroy();
    }, []);

    return(
        <div>
            <canvas ref={chartRef} id={"test"}></canvas>
        </div>
    )
};