import React, {useEffect, useRef} from "react";
import {system} from '../../queries';
import Chart from 'chart.js/auto'
import {chartConfig} from "../../../base";
import {ChartComponent} from "./ChartComponent";

const chartGroups = [
    {
        id: 'group.System',
        charts: [
            {
                id: 'chart.system.cpu.usage',
                query: system.cpuData,
            },
            {
                id: 'chart.system.la',
                query: system.la,
            },
            {
                id: 'chart.system.memory',
                query: system.memory,
            },
            {
                id: 'chart.system.contextSwitches',
                query: system.contextSwitches,
            },
            {
                id: 'chart.system.uptime',
                query: system.uptime,
            }
        ]
    }
]

export default function SystemCharts() {
    const chartRef = useRef();

    const createChart = () => {
        const chart = new Chart(chartRef.current.getContext('2d'), chartConfig);

        return chart;
    }

    useEffect(() => {
        const chart = createChart();
        return () => chart.destroy();
    }, [])

    return(
        <div className="container-fluid d-flex flex-column justify-content-center p-md-5"
             style={{maxHeight:"500px", overflowY: "auto"}}>
            <ChartComponent />
        </div>
    )
}
