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
        const url = `/api/v1/ram_data/${host}`;
        const interval = address && port ? setInterval(() => {
            const querylist = JSON.stringify([
                {label: "memTotal", query: "query?query=node_memory_MemTotal_bytes"},
                {label: "buffers", query: "query?query=node_memory_Buffers_bytes"},
                {label: "slab", query: "query?query=node_memory_Slab_bytes"},
                {label: "memFree", query: "query?query=node_memory_MemFree_bytes"},
                {label: "memAvail", query: "query?query=node_memory_MemAvailable_bytes"},
                {label: "cached", query: "query?query=node_memory_Cached_bytes"},
            ]);
            axios.get(url, {params: {querylist: querylist}})
                .then(response => {
                    if (response.data) {
                        const parsedData = JSON.parse(response.data);
                        const availMemPrc = (1 - (
                            parseFloat(parsedData[4].value.value)
                            / parseFloat(parsedData[0].value.value))) * 100

                        if (0 <= availMemPrc && availMemPrc < 50.0)
                            setColor("#16b616");
                        else if (50.0 <= availMemPrc && availMemPrc < 75.0)
                            setColor("#ff9900")
                        else
                            setColor("#ff0000")

                        setIRefreshInterval(refreshInterval);
                        setMemoryDataTooltip(parsedData);
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
                    {memoryDataTooltip === undefined ? "N/A" : memoryDataTooltip.map(data => {
                        return(
                            <div key={data.value.metric}>
                                {data.value.metric}: {data.value.value}GB
                            </div>
                        );
                    })}
                </Tooltip>
            </div>
        </div>
    );
};

export default MemoryState;