import React, {useEffect, useState} from "react";
import {Cpu} from "react-bootstrap-icons";
import axios from "axios";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";
import * as query from '../../queries'
import {getData, URL} from "../../../base";
import './ScrollableTooltip.css';

const CpuIndicator = ({host, refreshInterval}) => {
    const [cpuLoad, setCpuLoad] = useState("N/A");
    const [cpuDataTooltip, setCpuDataTooltip] = useState([]);
    const [cpuCoresCount, setCpuCoresCount] = useState(0);
    const [cpuCoresLabel, setCpuCoresLabel] = useState([]);
    const [color, setColor] = useState("#000000");

    const setCpuData = async () => {
        const urlRequest = URL + `?query=${encodeURI(query.system.cpuData)}`
            + `&host=${host}`
            + `&query_range=false`;
        const data = await getData(urlRequest);

        if (data) {
            const __cpuDataTooltip__ = data.data.result;
            const idle = parseFloat(__cpuDataTooltip__[0]?.value[1]);
            let __cpuLoad__ = (100 - idle).toFixed(2);

            if (0 <= __cpuLoad__ && __cpuLoad__ < 50.0)
                setColor("#16b616")
            else if (50.0 <= __cpuLoad__ && __cpuLoad__ < 75.0)
                setColor("#ff9900")
            else if (75.0 <= __cpuLoad__ && __cpuLoad__ <= 100.0)
                setColor("#ff0000")
            else
                __cpuLoad__ = 0;

            setColor("#16b616");
            setCpuDataTooltip(__cpuDataTooltip__);
            setCpuLoad(__cpuLoad__ + "%");
        }
        else {
            setCpuLoad("ERR");
            setColor("#000000");
            setCpuDataTooltip([]);
        }
    };

    const setCpuCores = async () => {
        const urlRequest = URL + `?query=${encodeURI(query.system.cpuCores)}`
            + `&host=${host}`
            + `&query_range=false`;
        const data = await getData(urlRequest);

        if (data) {
            const __cpuCoresData__ = data.data.result;
            setCpuCoresCount(__cpuCoresData__[0]?.value[1]);
            setCpuCoresLabel(__cpuCoresData__[0]?.metric.__name__);
        }
        else {
            setCpuCoresCount("ERR");
        }
    };

    const setDataImmediately = () => {
        setTimeout(setCpuData, 0);
        setTimeout(setCpuCores, 0);
    }

    useEffect(() => {
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);

    }, [refreshInterval]);

    const [isOpen, setIsOpen] = useState(false);

    const uuid = v4()

    return(
        <div className="d-flex flex-row justify-content-start mt-3">
            <Cpu height="24" width="24" color={color} data-ivcs-server-img-attr="cpu"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="cpu">
                <a data-tooltip-id={uuid} onMouseEnter={() => setIsOpen(true)}>{cpuLoad}</a>
                <div onMouseLeave={() => setIsOpen(false)}>
                    <Tooltip id={uuid} place="bottom" key={20}  isOpen={isOpen}>
                        <table>
                            <thead>
                                <tr>
                                    <th>{cpuCoresLabel}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>{cpuCoresCount}</td>
                                </tr>
                            </tbody>
                        </table>
                        <table>
                            <thead>
                                <tr>
                                    <th>mode</th>
                                    <th>value</th>
                                </tr>
                            </thead>
                            <tbody>
                            {cpuDataTooltip.map(i => {
                                return (
                                    <tr key={i.metric.mode}>
                                        <td>{i.metric.mode}</td>
                                        <td>{parseFloat(i.value[1]).toFixed(2)}</td>
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

export default CpuIndicator;