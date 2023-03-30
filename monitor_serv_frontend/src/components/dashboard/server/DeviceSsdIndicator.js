import React, {useEffect, useState} from "react";
import {DeviceSsd} from "react-bootstrap-icons";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";
import * as query from '../queries';
import {getData, URL} from "../../../base";
import './ScrollableTooltip.css';
import {useSelector} from "react-redux";

const DeviceSsdIndicator = ({host}) => {
    const [deviceSsdUsedSpace, setDeviceSsdUsedSpace] = useState("N/A");
    const [deviceSsdTooltip, setDeviceSsdTooltip] = useState([]);
    const [color, setColor] = useState("#000000");
    const refreshInterval = useSelector(state => {
        const interval = localStorage.getItem('refreshInterval')
        if (interval !== null)
            return interval;
        else
            return state.refresh.refreshInterval;
    });

    //disk io
    const [deviceSsdIO, setDeviceSsdIO] = useState([]);


    const setDeviceSsdData = async () => {
        const urlRequest = URL + `?query=${encodeURI(query.disk.rootSpace)}`
            + `&host=${host}`
            + `&query_range=false`;
        const data = await getData(urlRequest);

        if (data) {
            const __deviceSsdTooltip__ = data.data.result;

            setDeviceSsdTooltip(__deviceSsdTooltip__)

            const totalSpace = parseFloat(__deviceSsdTooltip__[2]?.value[1]);
            const freeSpace = parseFloat(__deviceSsdTooltip__[0]?.value[1]);
            const ssdUsedSpacePrc = (1 - (freeSpace / totalSpace)) * 100;

            if (0 <= ssdUsedSpacePrc && ssdUsedSpacePrc < 50.0)
                setColor("#16b616")
            else if (50.0 <= ssdUsedSpacePrc && ssdUsedSpacePrc < 75.0)
                setColor("#ff9900")
            else
                setColor("#ff0000")

            setDeviceSsdUsedSpace(ssdUsedSpacePrc.toFixed(2) + "%");
        } else {
            setColor("#000000");
            setDeviceSsdUsedSpace("ERR");
        }
    };

    const setDeviceSsdIOCallback = async () => {
        const urlRequest = URL + `?query=${encodeURI(query.disk.io)}`
            + `&host=${host}`
            + `&query_range=false`;
        const data = await getData(urlRequest);

        if (data) {
            const deviceSsdIo = data.data.result;
            setDeviceSsdIO(deviceSsdIo);
        }
        else {
            setDeviceSsdIO([]);
        }
    };

    const setDataImmediately = () => {
        setTimeout(setDeviceSsdData, 0);
        setTimeout(setDeviceSsdIOCallback, 0);
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
            <DeviceSsd height="24" width="24" color={color} data-ivcs-server-img-attr="filespace"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="filespace">
                <a data-tooltip-id={uuid} onMouseEnter={() => setIsOpen(true)}>{deviceSsdUsedSpace}</a>
                <div onMouseLeave={() => setIsOpen(false)}>
                    <Tooltip id={uuid} place="bottom" key={40} isOpen={isOpen}>
                    <div>IO Operations</div>
                    <table>
                        <thead>
                            <tr>
                                <th>Metric</th>
                                <th>Device</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>
                        {deviceSsdIO.map(i => {
                            return (
                                <tr key={i.metric.__name__ + "|" + i.metric.device}>
                                    <td>{i.metric.__name__}</td>
                                    <td>{i.metric.device}</td>
                                    <td>{parseFloat(i.value[1]).toFixed(2)}MB/s</td>
                                </tr>
                            )
                        })}
                        </tbody>
                    </table>
                    <div className="mt-2">Space stats</div>
                        <table>
                            <thead>
                                <tr>
                                    <th>Metric</th>
                                    <th>Device</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                            {deviceSsdTooltip.map(i => {
                                return (
                                    <tr key={i.metric.__name__}>
                                        <td>{i.metric.__name__}</td>
                                        <td>{i.metric.device}</td>
                                        <td>{parseFloat(i.value[1]).toFixed()}GB</td>
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

export default DeviceSsdIndicator;