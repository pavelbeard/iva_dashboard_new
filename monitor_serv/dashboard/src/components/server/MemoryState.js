import React, {useEffect, useState} from "react";
import {Memory} from "react-bootstrap-icons";
import axios from "axios";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";
import * as query from '../queries';

const MemoryState = ({host, refreshInterval, targetHealth}) => {
    const [memoryStatus, setMemoryStatus] = useState("N/A");
    const [memoryDataTooltip, setMemoryDataTooltip] = useState([]);
    const [color, setColor] = useState("#000000");
    const [iRefreshInterval, setIRefreshInterval] = useState(300);    //innerRefreshInterval

    useEffect(() => {
        const interval = setInterval(() => {
            const url = `/api/v1/prom_data/${host}`;

            axios.get(url, {params: {query: query.system.memory}})
                .then(response => {
                    if (response?.data?.data?.result) {
                        const __memoryDataTooltip__ = response.data.data.result;

                        const availMemPrc = (1 - (
                            parseFloat(__memoryDataTooltip__[0]?.value[1])
                            / parseFloat(__memoryDataTooltip__[5]?.value[1]))) * 100

                        if (0 <= availMemPrc && availMemPrc < 50.0)
                            setColor("#16b616");
                        else if (50.0 <= availMemPrc && availMemPrc < 75.0)
                            setColor("#ff9900")
                        else
                            setColor("#ff0000")

                        setIRefreshInterval(refreshInterval);
                        setMemoryDataTooltip(__memoryDataTooltip__);
                        setMemoryStatus(availMemPrc.toFixed(2) + "%");

                    }
                });

        }, iRefreshInterval);

        return () => clearInterval(interval);

    }, []);

    const uuid = v4();

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <Memory height="24" width="24" color={color} data-ivcs-server-img-attr="memory"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="memory">
                <a data-tooltip-id={uuid}>{memoryStatus}</a>
                <Tooltip id={uuid} place="bottom" key={30}>
                    <table>
                        <thead>
                            <tr>
                                <th>Metric</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            {memoryDataTooltip.map(i => {
                                return(
                                    <tr key={i.metric.__name__}>
                                        <td>{i.metric.__name__}</td>
                                        <td>{parseFloat(i.value[1]).toFixed(2)}GB</td>
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

export default MemoryState;