import React, {useEffect, useState} from "react";
import {Cpu} from "react-bootstrap-icons";
import axios from "axios";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";

const CpuState = ({address, port, refreshInterval}) => {
    const [cpuData, setCpuData] = useState("N/A");
    const [cpuDataTooltip, setCpuDataTooltip] = useState();
    const [cpuCoresCount, setCpuCoresCount] = useState();
    const [color, setColor] = useState("#000000");
    const [iRefreshInterval, setIRefreshInterval] = useState(300);    //innerRefreshInterval



    useEffect(() => {
        const interval = address && port ? setInterval(() => {
            const querylist = JSON.stringify([
                {label: "cpuData", query: "query?" +
                "query=(sum(irate(node_cpu_seconds_total[1h])) " +
                "without (cpu) * 100) / count(node_cpu_seconds_total) without (cpu)"},
                {label: "cpuCores", query: "query?" +
                        "query=count(node_cpu_seconds_total{mode='idle'}) without (cpu, mode)"}
            ]);

            const host = `${address}:${port}`;
            const url = `/api/v1/cpu_data/${host}`;
            axios.get(url, {params: {querylist: querylist}})
                .then(response => {
                    if (response.data) {
                        const parsedData = JSON.parse(response.data);
                        let cpuLoad = (100 - parseFloat(parsedData[0].value.data[0].value));

                        setCpuCoresCount(parsedData[1].value.data[0].coresCount);

                        if ( 0 <= cpuLoad && cpuLoad < 50.0)
                            setColor("#16b616")
                        else if ( 50.0 <= cpuLoad && cpuLoad < 75.0)
                            setColor("#ff9900")
                        else if (75.0 <= cpuLoad && cpuLoad <= 100.0)
                            setColor("#ff0000")
                        else
                            cpuLoad = 0;
                            setColor("#16b616")

                        setIRefreshInterval(refreshInterval);
                        setCpuDataTooltip(parsedData[0].value.data);
                        setCpuData(cpuLoad.toFixed(2) + "%");
                    }
            }).catch(err => {
                setColor("#000000");
                setCpuDataTooltip(undefined);
                setCpuData("N/A")

            });
        }, iRefreshInterval) : 500;

        return () => clearInterval(interval);

    }, []);

    const uuid = v4()

    return(
        <div className="d-flex flex-row justify-content-start mt-3">
            <Cpu height="24" width="24" color={color} data-ivcs-server-img-attr="cpu"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="cpu">
                <a data-tooltip-id={uuid}>{cpuData}</a>
                <Tooltip id={uuid} place="bottom" key={20}>
                    <div>{cpuCoresCount === undefined ? "" : `CPU Cores: ${cpuCoresCount}`}</div>
                    {cpuDataTooltip === undefined ? "N/A" : cpuDataTooltip.map(
                        data => {
                            return(
                                <div key={data.mode}>
                                    {data.mode}: {data.value}
                                </div>
                            )
                        }
                    )}
                </Tooltip>
            </div>
        </div>
    );
};

export default CpuState;