import React, {useEffect, useState} from "react";
import {Ethernet} from "react-bootstrap-icons";
import axios from "axios";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";

const NetworkState = ({host, refreshInterval, targetHealth}) => {
    const [netStatus, setNetStatus] = useState("N/A");
    const [netDataTooltip, setNetDataTooltip] = useState([]);
    const [color, setColor] = useState("#000000");
    const [iRefreshInterval, setIRefreshInterval] = useState(1000);    //innerRefreshInterval

    useEffect(() => {
        const interval = setInterval(() => {
            const query = 'query?query=label_keep(('
                + 'alias((rate(node_network_receive_bytes_total) * 8 / 1024), "RX"),'
                + 'alias((rate(node_network_transmit_bytes_total) * 8 / 1024), "TX")'
                + '), "__name__", "device")'

            const url = `/api/v1/prom_data/${host}`;
            axios.get(url, {params: {query: encodeURI(query)}})
                .then(response => {
                    if (response?.data?.data?.result) {
                        setNetStatus("UP");

                        const __netDataTooltip__ = response.data.data.result;

                        setNetDataTooltip(__netDataTooltip__);
                        setColor("#16b616")
                        setIRefreshInterval(refreshInterval);
                    }
                });
        }, iRefreshInterval);

        return () => clearInterval(interval);
    }, []);

    const uuid = v4();

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <Ethernet height="24" width="24" color={color} data-ivcs-server-img-attr="net"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="net">
                <a data-tooltip-id={uuid}>{netStatus}</a>
                <Tooltip id={uuid} place="bottom" key={60}>
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
                                     return(
                                         <tr key={i.metric.__name__ + "|" + i.metric.device}>
                                             <td>{i.metric.__name__}</td>
                                             <td>{i.metric.device}</td>
                                             <td>{parseFloat(i.value[1]).toFixed(2)} mbps</td>
                                         </tr>
                                     )
                                })}
                  !          </tbody>
                        </table>
                    </div>
                </Tooltip>
            </div>
        </div>
    );
};

export default NetworkState;