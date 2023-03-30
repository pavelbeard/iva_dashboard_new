import React, {useEffect, useState} from "react";
import {AppIndicator as App } from "react-bootstrap-icons";
import {Tooltip} from "react-tooltip";
import {v4} from "uuid";
import * as query from '../queries'
import {getData, sum, URL} from "../../../base";
import './ScrollableTooltip.css';
import {useSelector} from "react-redux";

const AppIndicator = ({host}) => {
    const [threads, setThreadsCount] = useState("N/A");
    const [appsDataTooltip, setAppsDataTooltip] = useState([]);
    const [color, setColor] = useState("#000000");
    const refreshInterval = useSelector(state => {
        const interval = localStorage.getItem('refreshInterval')
        if (interval !== null)
            return interval;
        else
            return state.refresh.refreshInterval;
    });

    const getAppsData = async () => {
        const urlRequest = URL + `?query=${encodeURI(query.modules.states)}`
            + `&host=${host}`
            + `&query_range=false`;
        const data = await getData(urlRequest);

        if (data) {
            const __appsDataTooltip__ = data.data.result;

            setAppsDataTooltip(__appsDataTooltip__);

            const threadsCount = sum(__appsDataTooltip__.map(i => {
                return parseInt(i.value[1]);
            }));

            setColor("#ff00f2");

            setThreadsCount(threadsCount);
        } else {
            setColor("#000000");
            setThreadsCount("ERR");
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

    const uuid = v4();

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <App height="24" width="24" color={color} data-ivcs-server-img-attr="apps"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="apps">
                <a data-tooltip-id={uuid} onMouseEnter={() => setIsOpen(true)}>{threads}</a>
                <div onMouseLeave={() => setIsOpen(false)}>
                    <Tooltip id={uuid} place="bottom" isOpen={isOpen}>
                    <table>
                        <thead>
                        <tr>
                            <th>№</th>
                            <th>Process name</th>
                            <th>State</th>
                            <th>Threads count</th>
                        </tr>
                        </thead>
                        <tbody>
                            {appsDataTooltip.map((i, num = 1) => {
                                return (
                                    <tr key={i.metric.__name__ + i.metric.groupname + i.metric.state}>
                                        <td>{num}</td>
                                        <td>{i.metric.groupname}</td>
                                        <td style={{color: colorizeState(i.metric.state)}}>
                                            {i.metric.state}</td>
                                        <td>{i.value[1]}</td>
                                    </tr>
                                )
                            })}
                            </tbody>
                        </table>
                    </Tooltip>
                </div>
            </div>
        </div>
    );
};

export default AppIndicator;