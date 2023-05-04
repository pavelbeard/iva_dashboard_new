import {system} from "../queries";
import Chart from "./Chart";
import {useEffect} from "react";

const chartGroups = {
    id: 'group.System',
    charts: [
        {
            id: 'chart.system.cpu.usage',
            query: system.cpuData,
            name: "CPU usage",
            metricMeasure: "%"
        },
        {
            id: 'chart.system.la',
            query: system.la,
            name: "Load Average",
            metricMeasure: ""
        },
        {
            id: 'chart.system.memory',
            query: system.memory,
            name: "RAM",
            metricMeasure: "GB"
        },
        {
            id: 'chart.system.contextSwitches',
            query: system.contextSwitches,
            name: "Context switches",
            metricMeasure: "s"
        },
        {
            id: 'chart.system.uptime',
            query: system.uptime,
            name: "Uptime",
            metricMeasure: "hours"
        }
    ]
};


const SystemCharts = ({host}) => {
    useEffect(() => {

    }, [host])

    if (host) {
        return(
            <div className="overflow-auto" style={{height: "500px"}}>
                {chartGroups.charts.map(chart => {
                    return (
                        <div key={chart.name}>
                            <Chart metricName={chart.id}
                                   query={chart.query}
                                   host={host}
                                   name={chart.name}
                                   metricMeasure={chart.metricMeasure}
                            />
                        </div>
                    );
                })}
            </div>
        )
    }

    return <div className="container-fluid p-5">Нет серверов!</div>
};

export default SystemCharts;
