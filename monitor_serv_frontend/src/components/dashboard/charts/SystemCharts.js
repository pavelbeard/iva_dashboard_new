import {system} from "../queries";
import Chart from "./Chart";

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
];

const metricName = "cpu.stats";

const SystemCharts = () => {

    // const q = 'sum by (mode,instance) (label_keep(rate(node_cpu_seconds_total[1h]), "mode")) * 100 / distinct(label_value(node_cpu_seconds_total, "cpu"))';
    // chartGroups[0].charts[0].query
    return(
        <div>
            <Chart metricName={metricName}
                   query={chartGroups[0].charts[0].query}
                   host={"127.0.0.1:9091"}
                   name={"CPU"}/>
        </div>
    )
};

export default SystemCharts;
