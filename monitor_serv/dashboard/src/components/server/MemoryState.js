import React, {useEffect, useState} from "react";
import {Memory} from "react-bootstrap-icons";
import axios from "axios";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";

const MemoryState = ({address, port, refreshInterval}) => {
    const [memoryData, setMemoryData] = useState("N/A");
    const [memoryDataTooltip, setMemoryDataTooltip] = useState();
    const [color, setColor] = useState("#000000");
    const [iRefreshInterval, setIRefreshInterval] = useState(300);    //innerRefreshInterval


    useEffect(() => {
        const host = `${address}:${port}`;
        const url = `/api/v1/prom_data/${host}`;
        const interval = address && port ? setInterval(() => {
            const query = 'query?query=label_keep(('
                        + 'alias(node_memory_MemTotal_bytes / 1073741824, "Total"),'
                        + 'alias(node_memory_Buffers_bytes / 1073741824, "Buffered"),'
                        + 'alias(node_memory_Slab_bytes / 1073741824, "Slab"),'
                        + 'alias(node_memory_MemFree_bytes / 1073741824, "Free"),'
                        + 'alias(node_memory_MemAvailable_bytes / 1073741824, "Available"),'
                        + 'alias(node_memory_Cached_bytes / 1073741824, "Cached")'
                        + '), "__name__")';

            axios.get(url, {params: {query: query}})
                .then(response => {
                    if (response.data) {
                        const availMemPrc = (1 - (
                            parseFloat(response.data.data.result[0].value[1])
                            / parseFloat(response.data.data.result[5].value[1]))) * 100

                        if (0 <= availMemPrc && availMemPrc < 50.0)
                            setColor("#16b616");
                        else if (50.0 <= availMemPrc && availMemPrc < 75.0)
                            setColor("#ff9900")
                        else
                            setColor("#ff0000")

                        setIRefreshInterval(refreshInterval);
                        setMemoryDataTooltip(response.data);
                        setMemoryData(availMemPrc.toFixed(2) + "%");

                    }
                }).catch(err => {
                    setColor("#00000");
                    setMemoryDataTooltip(undefined)
                    setMemoryData("N/A");
            });

        }, iRefreshInterval) : 500;

        return () => clearInterval(interval);

    }, []);

    const uuid = v4();

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <Memory height="24" width="24" color={color} data-ivcs-server-img-attr="memory"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="memory">
                <a data-tooltip-id={uuid}>{memoryData}</a>
                <Tooltip id={uuid} place="bottom" key={30}>
                    <table>
                        <thead>
                            <tr>
                                <th>Metric</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            {memoryDataTooltip === undefined ? "N/A" : memoryDataTooltip.data.result.map(i => {
                                return(
                                    <tr key={i.metric.__name__}>
                                        <td>{i.metric.__name__}</td>
                                        <td>{parseFloat(i.value[1]).toFixed(2)}GB</td>
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

export default MemoryState;