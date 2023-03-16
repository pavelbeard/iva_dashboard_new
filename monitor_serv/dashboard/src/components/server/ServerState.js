import React, {useEffect, useState} from "react";
import axios from "axios";
import {Server} from "react-bootstrap-icons";
import 'react-tooltip/dist/react-tooltip.css';
import {Tooltip} from 'react-tooltip';
import {v4} from "uuid";

import './Server.css';

const ServerState = ({address, port, refreshInterval}) => {
    const [targetInfo, setTargetInfo] = useState([])
    const [nodeStatus, setNodeStatus] = useState("N/A");
    const [color, setColor] = useState("#000000");
    const [iRefreshInterval, setIRefreshInterval] = useState(300);    //innerRefreshInterval


    useEffect(() => {
        const host = `${address}:${port}`;

        const interval = address && port ? setInterval(() => {
            const url = `/api/v1/prom_targets/${host}`;
            axios(url).then(response => {
                setNodeStatus("UP");
                setTargetInfo(response.data);
                setColor("#16b616")
                setIRefreshInterval(refreshInterval);

            }).catch(() => {
                setNodeStatus("DOWN")
                setTargetInfo([])
                setColor("#ff2d16")
                // console.log(err)
            });
        }, iRefreshInterval) : 5000;

        return () => clearInterval(interval)
    }, [])

    const uuid = v4();

    return(
        <div className="server">
            <div className="d-flex flex-row justify-content-center mt-3">
                <Server height="32" width="32" color={color} data-ivcs-server-img-attr="server"/>
            </div>
            <div className="text-center mt-2" data-ivcs-server-attr="status">
                {nodeStatus === undefined ? "N/A" : nodeStatus}
            </div>
            <div className="text-center mt-2" data-ivcs-server-attr="address">
                {address === undefined && port === undefined ? "N/A" : `${address}:${port}`}
            </div>
            <div className="text-center mt-2" data-ivcs-server-attr="targetInfo">
                <a data-tooltip-id={uuid}>Target info</a>
                <Tooltip id={uuid} place="bottom" key={10}>
                    {targetInfo.data === undefined ? "N/A" : targetInfo.data.activeTargets.map(ti => {
                        return(
                            <div key={ti.labels.instance}>
                                <div>Label: {ti.labels.instance}</div>
                                <div>Health: {ti.health}</div>
                            </div>
                        );
                    })}
                </Tooltip>
            </div>
        </div>
    );
};

export default ServerState;