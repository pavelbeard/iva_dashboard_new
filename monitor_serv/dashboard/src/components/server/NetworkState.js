import React, {useEffect, useState} from "react";
import {Ethernet} from "react-bootstrap-icons";
import axios from "axios";

const NetworkState = ({address, port, refreshInterval}) => {
    const [appsCount, setAppsCount] = useState();
    const [appsDataTooltip, setAppsDataTooltip] = useState();

    useEffect(() => {
        const interval = address && port ? setInterval(() => {
            const querylist = JSON.stringify([
                {label: "throughputRX", query: "query?query=node_network_receive_bytes_total"},
                {label: "throughputTX", query: "query?query=node_network_transmit_bytes_total"},
                {label: "errorsRX", query: "query?query=node_network_receive_errs_total"},
                {label: "errorsTX", query: "query?query=node_network_transmit_errs_total"},
                {label: "packetsRX", query: "query?query=node_network_receive_packets_total"},
                {label: "packetsTX", query: "query?query=node_network_transmit_packets_total"},
                {label: "netInfo", query: "query?query=node_network_info"},
            ])
            const host = `${address}:${port}`;
            const url = `/api/v1/net_data/${host}`;
            axios.get(url, {params: {querylist: querylist}})
                .then(response => {
                    if (response.data) {
                        const parsedData = JSON.parse(response.data);



                        setAppsDataTooltip(parsedData);
                    }
                });
        }, refreshInterval) : 5000;

        return () => clearInterval(interval);
    }, [])

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <Ethernet height="24" width="24" color="#000000" data-ivcs-server-img-attr="net"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="net">N/A</div>
        </div>
    );
};

export default NetworkState;