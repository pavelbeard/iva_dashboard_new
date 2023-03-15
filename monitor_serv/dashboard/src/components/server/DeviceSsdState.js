import React, {useEffect, useState} from "react";
import {DeviceSsd} from "react-bootstrap-icons";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";
import axios from "axios";

const DeviceSsdState = ({address, port, refreshInterval}) => {
    const [deviceSsdUsedSpace, setDeviceSsdUsedSpace] = useState("N/A");
    const [deviceSsdTooltip, setDeviceSsdTooltip] = useState();
    const [color, setColor] = useState("#000000");

    useEffect(() => {
        const interval = address && port ? setInterval(() => {
            const querylist = JSON.stringify([
                {label: "totalSpace", query: "query?query=node_filesystem_size_bytes"},
                {label: "usedSpace", query: "query?query=node_filesystem_size_bytes-node_filesystem_free_bytes"},
                {label: "reservedSpace", query: "query?query=node_filesystem_free_bytes-node_filesystem_avail_bytes"},
                {label: "freeSpace", query: "query?query=node_filesystem_avail_bytes"},
            ]);

            const host = `${address}:${port}`;
            const url = `/api/v1/filesystem_data/${host}`;
            axios.get(url, {params: {querylist: querylist}})
                .then(response => {
                    if (response.data) {
                        const parsedData = JSON.parse(response.data);
                        const totalSpace = parseFloat(parsedData[0].value[0].value);
                        const freeSpace = parseFloat(parsedData[3].value[0].value);
                        const ssdUsedSpacePrc = (1 - (freeSpace / totalSpace)) * 100;

                        if (0 <= ssdUsedSpacePrc && ssdUsedSpacePrc < 50.0)
                            setColor("#16b616")
                        else if (50.0 <= ssdUsedSpacePrc && ssdUsedSpacePrc < 75.0)
                            setColor("#ff9900")
                        else
                            setColor("#ff0000")

                        setDeviceSsdUsedSpace(ssdUsedSpacePrc.toFixed(2) + "%");
                        setDeviceSsdTooltip(parsedData);

                    }
                }).catch(err => {
                    setColor("#000000");
                    setDeviceSsdTooltip(undefined);
                    setDeviceSsdUsedSpace("N/A")
            });

        }, refreshInterval) : 500;

        return () => clearInterval(interval);
    });

    const uuid = v4();

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <DeviceSsd height="24" width="24" color={color} data-ivcs-server-img-attr="filespace"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="filespace">
                <a data-tooltip-id={uuid}>{deviceSsdUsedSpace}</a>
                <Tooltip id={uuid} place="bottom">
                    <div>
                        {/*style={{maxHeight: "200px", overflowY: "auto"}}*/}
                        {deviceSsdTooltip === undefined ? "N/A" : deviceSsdTooltip.map(i => {
                        return(
                            <div>
                                <div>{i.label}</div>
                                <table className="mb-2">
                                    <thead>
                                    <tr>
                                        <th>Device</th>
                                        <th>Fstype</th>
                                        <th>Mountpoint</th>
                                        <th>Value</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {i.value.map(v => {
                                        return(
                                            <tr>
                                                <td>{v.metric.device}</td>
                                                <td>{v.metric.fstype}</td>
                                                <td>{v.metric.mountpoint}</td>
                                                <td>{v.value}GB</td>
                                            </tr>
                                        )
                                    })}
                                    </tbody>
                                </table>
                            </div>
                        )
                    })}</div>
                </Tooltip>
            </div>
        </div>
    );
};

export default DeviceSsdState;