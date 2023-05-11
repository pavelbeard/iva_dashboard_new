import {modules} from "../queries";
import Chart from "./Chart";
import {useEffect} from "react";

const chartGroups = {
    id: 'group.Modules',
    charts: [
        {
            id: 'chart.modules.cpu.usage',
            query: modules.cpuUsage,
            name: "CPU",
            metricMeasure: "%"
        },
        {
            id: 'chart.modules.memory.resident',
            query: modules.memoryResident,
            name: "Resident memory",
            metricMeasure: "Mb"
        },
        {
            id: 'chart.modules.disk.read',
            query: modules.diskRead,
            name: "Disk read",
            metricMeasure: "Kb/s"
        },
        {
            id: 'chart.modules.disk.write',
            query: modules.diskWrite,
            name: "Disk write",
            metricMeasure: "Kb/s"
        },
        {
            id: 'chart.modules.processes',
            query: modules.processes,
            name: "Processes count",
            metricMeasure: ""
        },
        {
            id: 'chart.modules.threads',
            query: modules.threads,
            name: "Threads count",
            metricMeasure: ""
        },
        {
            id: 'chart.modules.fileDescriptors',
            query: modules.fileDescriptors,
            name: "Opened file descriptors",
            metricMeasure: ""
        },
        {
            id: 'chart.modules.hiccups.monotonic',
            query: modules.hiccupsMonotonic,
            name: "Monotonic hiccups",
            metricMeasure: "/s"
        },
        {
            id: 'chart.modules.hiccups.nonMonotonic',
            query: modules.hiccupsNonMonotonic,
            name: "Nonmonotonic hiccups",
            metricMeasure: "/s"
        },
    ]
};


const ModulesCharts = ({host}) => {
    useEffect(() => {

    }, [host])

    if (host) {
        return(
            <div className="overflow-auto h-auto">
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

export default ModulesCharts;
