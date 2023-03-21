import React, {useEffect, useState} from "react";
import axios from "axios";
import {Server} from "react-bootstrap-icons";
import 'react-tooltip/dist/react-tooltip.css';
import {Tooltip} from 'react-tooltip';
import {v4} from "uuid";

import './Server.css';
import {getData} from "../base";

const ServerState = ({host, refreshInterval, onClick}) => {
    const [targetInfo, setTargetInfo] = useState([])
    const [targetStatus, setTargetStatus] = useState("N/A");
    const [color, setColor] = useState("#000000");

    const setTargetStatusCallback = async () => {
        const urlRequest = `${process.env.REACT_APP_BACKEND_URL}/api/v1/prom_targets`
            + `?host=${host}`;

        const data = await getData(urlRequest);

        if (data) {
            setTargetStatus("UP");

            const __targetInfo___ = data.data.activeTargets;

            setTargetInfo(__targetInfo___);
            setColor("#16b616");
        }
        else {
            setColor("#000000")
            setTargetStatus("ERR");
        }
    };

    const setDataImmediately = () => {
        setTimeout(setTargetStatusCallback, 0);
    };

    useEffect(() => {
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);
    }, []);

    const uuid = v4();

    return(
        <div className="server">
            <div className="d-flex flex-row justify-content-center mt-3">
                <Server height="32" width="32" color={color} data-ivcs-server-img-attr="server"/>
            </div>
            <div className="text-center mt-2" data-ivcs-server-attr="status">
                {targetStatus}
            </div>
            <div className="text-center mt-2" data-ivcs-server-attr="address">
                {host}
            </div>
            <div className="text-center mt-2" data-ivcs-server-attr="targetInfo">
                <a data-tooltip-id={uuid}>Target info</a>
                <Tooltip id={uuid} place="bottom" key={10}>
                    {targetInfo.map(data => {
                        return(
                            <div key={data.labels.instance}>
                                <div>Label: {data.labels.instance}</div>
                                <div>Health: {data.health}</div>
                            </div>
                        );
                    })}
                </Tooltip>
            </div>
        </div>
    );
};

export default ServerState;