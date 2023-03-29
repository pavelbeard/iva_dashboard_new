import React, {useEffect, useState} from "react";
import {Memory} from "react-bootstrap-icons";
import axios from "axios";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";
import * as query from '../../queries';
import {getData, URL} from "../../../base";
import {useSelector} from "react-redux";

const MemoryIndicator = ({host}) => {
    const [memoryStatus, setMemoryStatus] = useState("N/A");
    const [memoryDataTooltip, setMemoryDataTooltip] = useState([]);
    const [color, setColor] = useState("#000000");
    const refreshInterval = useSelector(state => {
        const interval = sessionStorage.getItem('refreshInterval')
        if (interval !== null)
            return interval;
        else
            return state.refresh.refreshInterval;
    });

    const setMemoryData = async () => {
        const urlRequest = URL + `?query=${encodeURI(query.system.memory)}`
            + `&host=${host}`
            + `&query_range=false`;
        const data = await getData(urlRequest);

        if (data) {
            const __memoryDataTooltip__ = data.data.result;

            const availMemPrc = (1 - (
                parseFloat(__memoryDataTooltip__[0]?.value[1])
                / parseFloat(__memoryDataTooltip__[5]?.value[1]))) * 100

            if (0 <= availMemPrc && availMemPrc < 50.0)
                setColor("#16b616");
            else if (50.0 <= availMemPrc && availMemPrc < 75.0)
                setColor("#ff9900")
            else
                setColor("#ff0000")

            setMemoryDataTooltip(__memoryDataTooltip__);
            setMemoryStatus(availMemPrc.toFixed(2) + "%");
        } else {
            setColor("#000000");
            setMemoryStatus("ERR");
        }
    }

    const setDataImmediately = () => setTimeout(setMemoryData, 0);

    useEffect(() => {
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);

    }, [refreshInterval]);

    const [isOpen, setIsOpen] = useState(false);

    const uuid = v4();

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <Memory height="24" width="24" color={color} data-ivcs-server-img-attr="memory"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="memory">
                <a data-tooltip-id={uuid} onMouseEnter={() => setIsOpen(true)}>{memoryStatus}</a>
                <div onMouseLeave={() => setIsOpen(false)}>
                    <Tooltip id={uuid} place="bottom" key={30} isOpen={isOpen}>
                        <table>
                            <thead>
                            <tr>
                                <th>Metric</th>
                                <th>Value</th>
                            </tr>
                            </thead>
                            <tbody>
                            {memoryDataTooltip.map(i => {
                                return (
                                    <tr key={i.metric.__name__}>
                                        <td>{i.metric.__name__}</td>
                                        <td>{parseFloat(i.value[1]).toFixed(2)}GB</td>
                                    </tr>
                                )
                            })}
                            </tbody>
                        </table>
                    </Tooltip></div>
            </div>
        </div>
    );
};

export default MemoryIndicator;