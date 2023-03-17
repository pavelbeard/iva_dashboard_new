import React, {useEffect, useState} from "react";
import {Cpu} from "react-bootstrap-icons";
import axios from "axios";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";

const CpuState = ({host, refreshInterval, targetHealth}) => {
    const [cpuLoad, setCpuLoad] = useState("N/A");
    const [cpuDataTooltip, setCpuDataTooltip] = useState([]);
    const [cpuCoresCount, setCpuCoresCount] = useState([]);
    const [cpuCoresLabel, setCpuCoresLabel] = useState([]);
    const [color, setColor] = useState("#000000");
    const [iRefreshInterval, setIRefreshInterval] = useState(300);    //innerRefreshInterval

    useEffect(() => {
        const interval = setInterval(async () => {
            const query1 = 'query?query=sum by (mode,instance) ' +
                '(label_keep(rate(node_cpu_seconds_total), "mode")) * 100 / ' +
                'distinct(label_value(node_cpu_seconds_total, "cpu"))';

            const query2 = 'query?query=label_keep(alias(count(node_cpu_seconds_total{mode="idle"}) ' +
                'without (cpu, mode), "Cpu cores"), "__name__", "device")';

            const url = `/api/v1/prom_data/${host}`;

            axios.get(url, {params: {query: encodeURI(query1)}})
                .then(response => {
                    if (response?.data?.data?.result) {
                        const __cpuDataTooltip__ = response.data.data.result;
                        const idle = parseFloat(__cpuDataTooltip__[0]?.value[1]);
                        let __cpuLoad__ = (100 - idle).toFixed(2);

                        if (0 <= __cpuLoad__ && __cpuLoad__ < 50.0)
                            setColor("#16b616")
                        else if (50.0 <= __cpuLoad__ && __cpuLoad__ < 75.0)
                            setColor("#ff9900")
                        else if (75.0 <= __cpuLoad__ && __cpuLoad__ <= 100.0)
                            setColor("#ff0000")
                        else
                            __cpuLoad__ = 0;

                        setColor("#16b616");
                        setCpuDataTooltip(__cpuDataTooltip__);
                        setCpuLoad(__cpuLoad__ + "%");
                        setIRefreshInterval(refreshInterval);
                    }
                }).catch(err => {
                    console.log(err);
            });

            axios.get(url, {params: {query: encodeURI(query2)}})
                .then(response => {
                    if (response.data) {
                        const __cpuCoresData__ = response.data.data.result;
                        setCpuCoresCount(__cpuCoresData__[0]?.value[1]);
                        setCpuCoresLabel(__cpuCoresData__[0]?.metric.__name__);
                    }
                }).catch(err => {
                    console.log(err);
            });

        }, iRefreshInterval);

        return () => clearInterval(interval);

    }, []);

    const uuid = v4()

    return(
        <div className="d-flex flex-row justify-content-start mt-3">
            <Cpu height="24" width="24" color={color} data-ivcs-server-img-attr="cpu"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="cpu">
                <a data-tooltip-id={uuid}>{cpuLoad}</a>
                <Tooltip id={uuid} place="bottom" key={20}>
                    <table>
                        <thead>
                            <tr>
                                <th>{cpuCoresLabel}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{cpuCoresCount}</td>
                            </tr>
                        </tbody>
                    </table>
                    <table>
                        <thead>
                            <tr>
                                <th>mode</th>
                                <th>value</th>
                            </tr>
                        </thead>
                        <tbody>
                            {cpuDataTooltip.map(i => {
                                return (
                                    <tr key={i.metric.mode}>
                                        <td>{i.metric.mode}</td>
                                        <td>{parseFloat(i.value[1]).toFixed(2)}</td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </table>
                </Tooltip>
            </div>
        </div>
    );
};

export default CpuState;