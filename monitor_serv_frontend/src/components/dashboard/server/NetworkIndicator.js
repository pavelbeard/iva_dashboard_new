import React, {useEffect, useState} from "react";
import {Ethernet} from "react-bootstrap-icons";
import axios from "axios";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";
import * as query from '../../queries';
import {getData, URL} from "../../../base";

const NetworkIndicator = ({host, refreshInterval, targetHealth}) => {
    const [netStatus, setNetStatus] = useState("N/A");
    const [netDataTooltip, setNetDataTooltip] = useState([]);
    const [color, setColor] = useState("#000000");

    const getNetworkData = async () => {
        const urlRequest = URL + `?query=${encodeURI(query.network.throughput)}`
            + `&host=${host}`
            + `&query_range=false`;
        const data = await getData(urlRequest);

        if (data) {
            setNetStatus("UP");

            const __netDataTooltip__ = data.data.result;

            setNetDataTooltip(__netDataTooltip__);
            setColor("#16b616")
        } else {
            setColor("#000000");
            setNetStatus("ERR");
        }
    };

    const setDataImmediately = () => {
        setTimeout(getNetworkData, 0);
    };


    useEffect(() => {
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);
    }, []);

    const [isOpen, setIsOpen] = useState(false);

    const uuid = v4();

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <Ethernet height="24" width="24" color={color} data-ivcs-server-img-attr="net"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="net">
                <a data-tooltip-id={uuid} onMouseEnter={() => setIsOpen(true)}>{netStatus}</a>
                <div onMouseLeave={() => setIsOpen(false)}>
                    <Tooltip id={uuid} place="bottom" key={60} isOpen={isOpen}>
                        <div>
                            <table>
                                <thead>
                                <tr>
                                    <th>Metric</th>
                                    <th>Device</th>
                                    <th>Value</th>
                                </tr>
                                </thead>
                                <tbody>
                                {netDataTooltip.map(i => {
                                    return (
                                        <tr key={i.metric.__name__ + "|" + i.metric.device}>
                                            <td>{i.metric.__name__}</td>
                                            <td>{i.metric.device}</td>
                                            <td>{parseFloat(i.value[1]).toFixed(2)} mbps</td>
                                        </tr>
                                    )
                                })}
                                </tbody>
                            </table>
                        </div>
                    </Tooltip>
                </div>
            </div>
        </div>
    );
};

export default NetworkIndicator;