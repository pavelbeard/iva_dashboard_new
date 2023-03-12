import React, {useEffect, useState} from "react";
import axios from "axios";
import {Server} from "react-bootstrap-icons";
import 'react-tooltip/dist/react-tooltip.css';
import {Tooltip} from 'react-tooltip';
import {renderToStaticMarkup} from "react-dom/server";
import {v4} from "uuid";

const ServerState = ({address, port, refreshInterval}) => {
    const [targetInfo, setTargetInfo] = useState([])
    const [nodeStatus, setNodeStatus] = useState("N/A");
    const [color, setColor] = useState("#000000");

    useEffect(() => {
        const host = `${address}:${port}`;

        const interval = setInterval(() => {
            const url = `http://${host}/api/v1/targets?state=any`;
            axios(url).then(response => {
                setNodeStatus("UP");
                setTargetInfo(response.data);
                setColor("#16b616")

            }).catch(() => {
                setNodeStatus("DOWN")
                setTargetInfo([])
                setColor("#ff2d16")
                // console.log(err)
            });
        }, refreshInterval)

        return () => clearInterval(interval)
    }, [])

    const uuid = v4();

    return(
        <div>
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
                <Tooltip id={uuid} place="bottom">
                    {targetInfo.data === undefined ? "N/A" : targetInfo.data.activeTargets.map(ti => {
                        return(
                            <div>
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