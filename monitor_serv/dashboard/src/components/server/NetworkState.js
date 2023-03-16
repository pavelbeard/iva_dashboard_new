import React, {useEffect, useState} from "react";
import {Ethernet} from "react-bootstrap-icons";
import axios from "axios";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";

const NetworkState = ({address, port, refreshInterval}) => {
    const [netStatus, setNetStatus] = useState("N/A");
    const [netStatusTooltip, setNetStatusTooltip] = useState();
    const [netDataTooltip, setNetDataTooltip] = useState();
    const [color, setColor] = useState("#000000");
    const [iRefreshInterval, setIRefreshInterval] = useState(300);    //innerRefreshInterval


    useEffect(() => {
        const interval = address && port ? setInterval(() => {
            const querylist = JSON.stringify([
                {label: "throughputRX", query: "query?query=node_network_receive_bytes_total{device='eth0'}"},
                {label: "throughputTX", query: "query?query=node_network_transmit_bytes_total{device='eth0'}"},
                {label: "errorsRX", query: "query?query=node_network_receive_errs_total{device='eth0'}"},
                {label: "errorsTX", query: "query?query=node_network_transmit_errs_total{device='eth0'}"},
                {label: "packetsRX", query: "query?query=node_network_receive_packets_total{device='eth0'}"},
                {label: "packetsTX", query: "query?query=node_network_transmit_packets_total{device='eth0'}"},
                {label: "netInfo", query: "query?query=node_network_info{device='eth0'}"},
            ]);

            const host = `${address}:${port}`;
            const url = `/api/v1/net_data/${host}`;
            axios.get(url, {params: {querylist: querylist}})
                .then(response => {
                    if (response.data) {
                        const parsedData = JSON.parse(response.data);
                        const deviceStatus = parsedData[6].value[0].metric.operstate.toUpperCase();
                        setNetStatus(deviceStatus);
                        setColor("#16b616")
                        setNetDataTooltip(parsedData.slice(0, -1));
                        setNetStatusTooltip(parsedData.slice(-2, -1));
                        setIRefreshInterval(refreshInterval);

                    }
                }).catch(err => {
                    setColor("#000000");
                    setNetDataTooltip();
                    setNetStatusTooltip();
                    setNetStatus("N/A");
            });
        }, iRefreshInterval) : 5000;

        return () => clearInterval(interval);
    }, [])

    const uuid = v4();

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <Ethernet height="24" width="24" color={color} data-ivcs-server-img-attr="net"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="net">
                <a data-tooltip-id={uuid}>{netStatus}</a>
                <Tooltip id={uuid} place="bottom" key={60}>
                    {netDataTooltip === undefined ? "N/A" : netDataTooltip.map(i => {
                        return(
                            <div key={i.value[0].metric.__name__}>
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Metric</th>
                                            <th>Device</th>
                                            <th>Value</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>{i.value[0].metric.__name__}</td>
                                            <td>{i.value[0].metric.device}</td>
                                            <td>{i.value[0].value}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        )
                    })}
                </Tooltip>
            </div>
        </div>
    );
};

export default NetworkState;