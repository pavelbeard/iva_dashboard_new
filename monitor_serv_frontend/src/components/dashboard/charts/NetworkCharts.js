import {network} from "../queries";
import Chart from "./Chart";
import {useEffect} from "react";

const chartGroups = {
    id: 'group.Network',
    charts: [
        {
            id: 'chart.network.errors',
            query: network.errors,
            name: "Errors",
            metricMeasure: ""
        },
        {
            id: 'chart.network.throughput',
            query: network.throughput,
            name: "Throughput",
            metricMeasure: "kbit/s"
        },
        {
            id: 'chart.network.packets',
            query: network.packets,
            name: "Packets",
            metricMeasure: ""
        },
    ]
};


const NetworkCharts = ({host}) => {
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

export default NetworkCharts;
