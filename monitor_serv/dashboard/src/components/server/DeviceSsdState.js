import React, {useEffect, useState} from "react";
import {DeviceSsd} from "react-bootstrap-icons";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";
import axios from "axios";

const DeviceSsdState = ({address, port, refreshInterval}) => {
    const [deviceSsdUsedSpace, setDeviceSsdUsedSpace] = useState("N/A");
    const [deviceSsdTooltip, setDeviceSsdTooltip] = useState();
    const [color, setColor] = useState("#000000");
    const [iRefreshInterval, setIRefreshInterval] = useState(300);    //innerRefreshInterval

    //disk io
    const [deviceSsdIO, setDeviceSsdIO] = useState();

    const setDefault = () => {
        setDeviceSsdUsedSpace("N/A");
        setDeviceSsdTooltip(undefined);
        setDeviceSsdIO(undefined);
        setColor("#000000");
        setIRefreshInterval(5000);
    };

    useEffect(() => {
        try {
            const interval = address && port ? setInterval(() => {
                const query = 'query?query=label_keep(' +
                    'label_match(' +
                    '(alias(node_filesystem_size_bytes / 1073741824, "Total"),' +
                    'alias((node_filesystem_size_bytes-node_filesystem_free_bytes) / 1073741824, "Used"), ' +
                    'alias((node_filesystem_free_bytes-node_filesystem_avail_bytes) / 1073741824, "Reserved"), ' +
                    'alias(node_filesystem_avail_bytes / 1073741824, "Free")), ' +
                    '"mountpoint", "/|/etc/hosts"), "__name__", "device")';

                const query1 = 'query?query=' +
                    'label_keep(' +
                    '(alias(rate(node_disk_read_bytes_total) / 1048576, "Reads"),' +
                    'alias(rate(node_disk_written_bytes_total) / 1048576, "Writes")), "__name__", "device")'

                const host = `${address}:${port}`;
                const url = `/api/v1/prom_data/${host}`;
                axios.get(url, {params: {query: encodeURI(query)}})
                    .then(response => {
                        if (response.data) {
                            setDeviceSsdTooltip(response.data)

                            const totalSpace = parseFloat(response.data.data.result[2].value[1]);
                            const freeSpace = parseFloat(response.data.data.result[0].value[1]);
                            const ssdUsedSpacePrc = (1 - (freeSpace / totalSpace)) * 100;

                            if (0 <= ssdUsedSpacePrc && ssdUsedSpacePrc < 50.0)
                                setColor("#16b616")
                            else if (50.0 <= ssdUsedSpacePrc && ssdUsedSpacePrc < 75.0)
                                setColor("#ff9900")
                            else
                                setColor("#ff0000")

                            setIRefreshInterval(refreshInterval);
                            setDeviceSsdUsedSpace(ssdUsedSpacePrc.toFixed(2) + "%");
                        }
                    }).catch(err => {
                    console.log(err);
                    setDefault();
                });

                axios.get(url, {params: {query: encodeURI(query1)}})
                    .then(response => {
                        if (response.data) {
                            setDeviceSsdIO(response.data);
                        }
                    }).catch(err => {
                    console.log(err);
                    setDefault();
                })

            }, iRefreshInterval) : 500;

            return () => clearInterval(interval);
        } catch (e) {
            console.log(e);
            setDefault();
        }
    }, []);

    const uuid = v4();

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <DeviceSsd height="24" width="24" color={color} data-ivcs-server-img-attr="filespace"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="filespace">
                <a data-tooltip-id={uuid}>{deviceSsdUsedSpace}</a>
                <Tooltip id={uuid} place="bottom" key={40}>
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
                        {deviceSsdIO === undefined || deviceSsdIO.data === undefined ? "N/A"
                            : deviceSsdIO.data.result.map(i => {
                            return(
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
                            {deviceSsdTooltip === undefined || deviceSsdTooltip.data === undefined ? "N/A"
                                : deviceSsdTooltip.data.result.map(i => {
                                return(
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
    );
};

export default DeviceSsdState;