import {system} from "../queries";

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
    return(
        <div>CHARTS</div>
    )
}
