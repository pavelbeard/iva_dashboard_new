import React, {useEffect, useState} from "react";
import {AppIndicator as App } from "react-bootstrap-icons";
import {sum, URL} from "../../../base";
import {useSelector} from "react-redux";
import * as query from '../queries'

import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import axios from "axios";
import {Link} from "react-router-dom";

const ThreadAppIndicator = ({host}) => {
    const [threads, setThreadsCount] = useState("N/A");
    const [threadsDataTooltip, setThreadsDataTooltip] = useState([]);
    const [color, setColor] = useState("#000000");
    const [hoverColor, setHoverColor] = useState();
    const refreshInterval = useSelector(state => state.refresh.refreshInterval);

    const getAppsData = async () => {
        try {
            const urlRequest = URL + `?query=${encodeURI(query.modules.states)}`
            + `&host=${host}`
            + `&query_range=false`;
            const response = (await axios.get(urlRequest)).data;

            if (response.data) {
                const __appsDataTooltip__ = response.data.result;

                setThreadsDataTooltip(__appsDataTooltip__);

                const threadsCount = sum(__appsDataTooltip__.map(i => {
                    return parseInt(i.value[1]);
                }));

                setColor("#ff00f2");

                setThreadsCount(threadsCount);
            }
        } catch(err) {
            setColor("#000000");
            setThreadsCount("ERR");
            console.log(`${this.name}: что-то тут не так...`);
        }
    }

    const colorizeState = state => {
        switch (state) {
            case 'Zombie':
                return "#3b9a4d";
            case 'Sleeping':
                return "#943094";
            case 'Running':
                return "#11ff00";
            case 'Other':
                return "#00bbff";
            case 'Waiting':
                return "#ff9900";
        }
    }

    const setDataImmediately = () => {
        setTimeout(getAppsData, 0);
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
                    <th>№</th>
                    <th>| Process name</th>
                    <th>| State</th>
                    <th>| Threads count</th>
                </tr>
                </thead>
                <tbody>
                {typeof threadsDataTooltip.map === "function"
                    ? threadsDataTooltip.map((i, num = 1) => {
                    return (
                        <tr key={i.metric.__name__ + i.metric.groupname + i.metric.state}>
                            <td>{num}</td>
                            <td>| {i.metric.groupname}</td>
                            <td style={{color: colorizeState(i.metric.state)}}>
                                | {i.metric.state}</td>
                            <td>| {i.value[1]}</td>
                        </tr>
                    )
                }) : ""}
                </tbody>
            </table>
        </div>
    );

    return(
        <div className="d-flex flex-row justify-content-start mt-1"
             onMouseLeave={() => setIsOpen(false)}>
            <Link to="/charts">
                <App height="24" width="24" color={hoverColor || color} data-ivcs-server-img-attr="apps"
                        onMouseEnter={() => setHoverColor("#fff")}
                        onMouseLeave={() => setHoverColor(undefined)}
                />
            </Link>
            <div className="ps-2 mt-1" data-ivcs-server-attr="apps">
                <OverlayTrigger
                    onToggle={() => setIsOpen(true)}
                    show={isOpen}
                    placement="bottom"
                    overlay={popover}>
                    <div className={`${isOpen ? 'indicator' : 'text-decoration-none text-dark'}`}>
                        {threads}
                    </div>
                </OverlayTrigger>
            </div>
        </div>
    );
};

export default ThreadAppIndicator;