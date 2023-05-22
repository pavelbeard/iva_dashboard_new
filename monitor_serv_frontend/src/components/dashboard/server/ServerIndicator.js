import React, {useEffect, useState} from "react";
import {DatabaseFillUp, ArrowRepeat, DatabaseFillDown} from "react-bootstrap-icons";
import {API_URL} from "../../../base";
import {useSelector} from "react-redux";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";

import './Server.css';
import axios from "axios";
import AppList from "./AppList";
import RoleIndicator from "./RoleIndicator";
import {Link} from "react-router-dom";

const ServerIndicator = ({id, host}) => {
    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    const [targetInfo, setTargetInfo] = useState([])
    const [targetStatus, setTargetStatus] = useState("N/A");
    const [color, setColor] = useState("#000000");
    const [hoverColor, setHoverColor] = useState();
    const [rotateEvent, setRotateEvent] = useState(false);

    const animateRefresh = () => {
        setRotateEvent(true);
        setTimeout(setRotateEvent, 400, false);
    };

    const setTargetStatusCallback = async () => {
        try {
            const urlRequest = `${API_URL}/api/v1/prom_targets`
                + `?host=${host}`;
            const response = (await axios.get(urlRequest)).data;

            if (response.data) {
                setTargetStatus("UP");

                const __targetInfo___ = response.data.activeTargets;

                setTargetInfo(__targetInfo___);
                setColor("#16b616");
            }
        } catch (err) {
            setColor("#000000")
            setTargetStatus("ERR");
            console.log(`${setTargetStatusCallback.name}: что-то тут не так...`);
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

    const popover = (
        <div className="bg-dark text-white rounded p-2 tooltip">
            <table className="tooltip-text">
                <thead>
                    <tr>
                       <th>Label:</th>
                       <th>| Health:</th>
                    </tr>
                </thead>
                <tbody>
                    {typeof targetInfo.map === "function"
                        ? targetInfo.map((data, n=0) => {
                        return (
                            <tr key={data.labels.instance + `${n}`}>
                                <td>{data.labels.instance}</td>
                                <td>| {data.health}</td>
                            </tr>
                        );
                    }) : ""}
                </tbody>
            </table>
        </div>
    );

    const up = <Link to="/charts">
        <DatabaseFillUp height="32" width="32" color={hoverColor || color} data-ivcs-server-img-attr="server"
                        onMouseEnter={() => setHoverColor("#fff")}
                        onMouseLeave={() => setHoverColor(undefined)}
        />
    </Link>
    const down = <DatabaseFillDown height="32" width="32" color={color} data-ivcs-server-img-attr="server"/>


    return(
        <div className="server">
            <div className="ms-1 mt-1" style={{width: "20px"}}>
                <div className={`${rotateEvent ? 'spin' : ''}`}>
                    <ArrowRepeat width="20" height="20"/>
                </div>
            </div>
            <div className="d-flex flex-row justify-content-center mt-1">
                {targetStatus === "UP" ? up : down }
            </div>
            <div className="text-center mt-1" data-ivcs-server-attr="status"
                 onMouseLeave={() => setIsOpen(false)}>
                <OverlayTrigger
                    onToggle={() => setIsOpen(true)}
                    show={isOpen}
                    placement="bottom"
                    overlay={popover}>
                    <div className={`${isOpen ? 'indicator' : 'text-decoration-none text-dark'}`}>
                        <RoleIndicator host={host}/>
                    </div>
                </OverlayTrigger>
            </div>
            <div className="text-center mt-1" data-ivcs-server-attr="address">
                {host}
            </div>
            <AppList id={id}/>
        </div>
    );
};

export default ServerIndicator;