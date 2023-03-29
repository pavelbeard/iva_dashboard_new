import React, {useEffect, useState} from "react";
import './ServerIndicator.css';
import {Server, ArrowRepeat} from "react-bootstrap-icons";
import 'react-tooltip/dist/react-tooltip.css';
import {Tooltip} from 'react-tooltip';
import {v4} from "uuid";
import './Server.css';
import {API_URL, getData} from "../../../base";
import {useSelector} from "react-redux";

const ServerIndicator = ({host}) => {
    const [targetInfo, setTargetInfo] = useState([])
    const [targetStatus, setTargetStatus] = useState("N/A");
    const [color, setColor] = useState("#000000");
    const refreshInterval = useSelector(state => {
        const interval = sessionStorage.getItem('refreshInterval');
        if (interval !== null)
            return interval;
        else
            return state.refresh.refreshInterval;
    });

    const [rotateDeg, setRotateDeg] = useState(360);

    const animateRefresh = () => {
        setRotateDeg(prevState => prevState + 360);
        if (rotateDeg > 720)
            setRotateDeg(0);
    };

    const setTargetStatusCallback = async () => {
        const urlRequest = `${API_URL}/api/v1/prom_targets`
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
        setTimeout(animateRefresh, 0);
        setTimeout(setTargetStatusCallback, 0);
    };

    useEffect(() => {
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);
    }, [refreshInterval]);

    const [isOpen, setIsOpen] = useState(false);

    const uuid = v4();

    return(
        <div className="server">
            <div className="ms-1 mt-1">
                <div style={{
                    transform: `rotate(${rotateDeg}deg)`,
                    transition: 'transform 500ms ease',
                }}><ArrowRepeat width="20" height="20"/></div>
            </div>
            <div className="d-flex flex-row justify-content-center mt-1">
                <Server height="32" width="32" color={color} data-ivcs-server-img-attr="server"/>
            </div>
            <div className="text-center mt-2" data-ivcs-server-attr="status">
                {targetStatus}
            </div>
            <div className="text-center mt-2" data-ivcs-server-attr="address">
                {host}
            </div>
            <div className="text-center mt-2" data-ivcs-server-attr="targetInfo">
                <a data-tooltip-id={uuid} onMouseEnter={() => setIsOpen(true)}>Target info</a>
                <div onMouseLeave={() => setIsOpen(false)}>
                    <Tooltip id={uuid} place="bottom" key={10} isOpen={isOpen}>
                        {targetInfo.map(data => {
                            return (
                                <div key={data.labels.instance}>
                                    <div>Label: {data.labels.instance}</div>
                                    <div>Health: {data.health}</div>
                                </div>
                            );
                        })}
                    </Tooltip>
                </div>
            </div>
        </div>
    );
};

export default ServerIndicator;