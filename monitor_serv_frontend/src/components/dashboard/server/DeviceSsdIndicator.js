import React, {useEffect, useState} from "react";
import {DeviceSsd} from "react-bootstrap-icons";
import * as query from '../queries';
import {getData, URL} from "../../../base";
import {useSelector} from "react-redux";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import axios from "axios";

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
        try {
            const urlRequest = URL + `?query=${encodeURI(query.disk.rootSpace)}`
                + `&host=${host}`
                + `&query_range=false`;
            const response = (await axios.get(urlRequest)).data;

            if (response.data) {
                const __deviceSsdTooltip__ = response.data.result;

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
            }
        } catch(err) {
            setColor("#000000");
            setDeviceSsdUsedSpace("ERR");
            console.log(`${this.name}: что-то тут не так...`);
        }
    };

    const setDeviceSsdIOCallback = async () => {
        try {
            const urlRequest = URL + `?query=${encodeURI(query.disk.io)}`
                + `&host=${host}`
                + `&query_range=false`;
            const response = (await axios.get(urlRequest)).data;

            if (response.data) {
                const deviceSsdIo = response.data.result;
                setDeviceSsdIO(deviceSsdIo);
            }
        } catch (err) {
            setDeviceSsdIO([]);
            console.log(`${this.name}: что-то тут не так...`);
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

    const popover = (
        <div className="bg-dark text-white rounded p-2 tooltip">
            <div className="tooltip-text">IO Operations</div>
            <table className="tooltip-text">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>| Device</th>
                        <th>| Value</th>
                    </tr>
                </thead>
                <tbody>
                {deviceSsdIO.map(i => {
                    return (
                        <tr key={i.metric.__name__ + "|" + i.metric.device}>
                            <td>{i.metric.__name__}</td>
                            <td>| {i.metric.device}</td>
                            <td>| {parseFloat(i.value[1]).toFixed(2)}MB/s</td>
                        </tr>
                    )
                })}
                </tbody>
            </table>
            <div className="mt-2 tooltip-text">Space stats</div>
            <table className="tooltip-text">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>| Device</th>
                        <th>| Value</th>
                    </tr>
                </thead>
                <tbody>
                {typeof deviceSsdTooltip.map === "function"
                    ? deviceSsdTooltip.map(i => {
                    return (
                        <tr key={i.metric.__name__}>
                            <td>{i.metric.__name__}</td>
                            <td>| {i.metric.device}</td>
                            <td>| {parseFloat(i.value[1]).toFixed()}GB</td>
                        </tr>
                    )
                }) : ""}
                </tbody>
            </table>
        </div>
    );

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <DeviceSsd height="24" width="24" color={color} data-ivcs-server-img-attr="filespace"/>
            <div className="ps-2 mt-1" data-ivcs-server-attr="filespace"
                 onMouseLeave={() => setIsOpen(false)}>
                <OverlayTrigger
                    onToggle={() => setIsOpen(true)}
                    show={isOpen}
                    placement="bottom"
                    overlay={popover}>
                    <div onMouseEnter={() => setIsOpen(true)}
                       className={`${isOpen ? 'indicator' : 'text-decoration-none text-dark'}`}>
                        {deviceSsdUsedSpace}
                    </div>
                </OverlayTrigger>
            </div>
        </div>
    );
};

export default DeviceSsdIndicator;