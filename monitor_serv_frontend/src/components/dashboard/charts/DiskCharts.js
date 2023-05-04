import {disk} from "../queries";
import Chart from "./Chart";
import {useEffect} from "react";

const chartGroups = {
    id: 'group.Disk',
    charts: [
        {
            id: 'chart.disk.rootSpace',
            query: disk.rootSpace,
            name: "Root space",
            metricMeasure: "GB"
        },
        {
            id: 'chart.disk.merges',
            query: disk.merges,
            name: "Merges",
            metricMeasure: "/s"
        },
        {
            id: 'chart.disk.io',
            query: disk.io,
            name: "I/O",
            metricMeasure: "MB/s"
        },
        {
            id: 'chart.disk.operations',
            query: disk.operations,
            name: "Operations",
            metricMeasure: "/s"
        },
        {
            id: 'chart.disk.times',
            query: disk.times,
            name: "Times",
            metricMeasure: ""
        },
    ]
};


const DiskCharts = ({host}) => {
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

export default DiskCharts;
