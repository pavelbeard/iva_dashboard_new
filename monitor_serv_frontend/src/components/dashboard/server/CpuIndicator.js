import React, {useEffect, useState} from "react";
import {Cpu} from "react-bootstrap-icons";
import axios from "axios";
import * as query from '../queries'
import {URL} from "../../../base";
import {useSelector} from "react-redux";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import {Link} from "react-router-dom";

const CpuIndicator = ({host}) => {
    const [cpuLoad, setCpuLoad] = useState("N/A");
    const [cpuDataTooltip, setCpuDataTooltip] = useState([]);
    const [cpuCoresCount, setCpuCoresCount] = useState(0);
    const [cpuCoresLabel, setCpuCoresLabel] = useState([]);
    const [color, setColor] = useState("#000000");
    const [hoverColor, setHoverColor] = useState();
    const refreshInterval = useSelector(state => state.refresh.refreshInterval);

    const setCpuData = async () => {
        try {
            const urlRequest = URL + `?query=${encodeURI(query.system.cpuData)}`
                + `&host=${host}`
                + `&query_range=false`;
            const response = (await axios.get(urlRequest)).data;

            if (response.data) {
                const __cpuDataTooltip__ = response.data.result;
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
        } catch (err) {
            setCpuLoad("ERR");
            setColor("#000000");
            setCpuDataTooltip([]);
            console.log(`${setCpuData.name} что-то тут не так...`)
        }
    };

    const setCpuCores = async () => {
        try {
            const urlRequest = URL + `?query=${encodeURI(query.system.cpuCores)}`
                + `&host=${host}`
                + `&query_range=false`;
            const response = (await axios.get(urlRequest)).data;

            if (response.data) {
                const __cpuCoresData__ = response.data.result;
                setCpuCoresCount(__cpuCoresData__[0]?.value[1]);
                setCpuCoresLabel(__cpuCoresData__[0]?.metric.__name__);
            }
        } catch (err) {
            setCpuCoresCount("ERR");
            console.log(`${setCpuCores.name} что-то тут не так...`)
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

    const popover = (
        <div className="bg-dark text-white rounded p-2 tooltip">
            <table className="tooltip-text">
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
            <table className="tooltip-text">
                <thead>
                    <tr>
                        <th>mode</th>
                        <th>| value</th>
                    </tr>
                </thead>
                <tbody>
                {typeof cpuDataTooltip.map === "function"
                    ? cpuDataTooltip.map(i => {
                    return (
                        <tr key={i.metric.mode}>
                            <td>{i.metric.mode}</td>
                            <td>| {parseFloat(i.value[1]).toFixed(2)}</td>
                        </tr>
                    )
                }) : ""}
                </tbody>
            </table>
        </div>
    );

    return(
        <div className="d-flex flex-row justify-content-start mt-1"
             onMouseLeave={() => setIsOpen(false)}>
            <Link to="/charts">
                <Cpu height="24" width="24" color={hoverColor || color}
                    onMouseEnter={() => setHoverColor("#fff")}
                    onMouseLeave={() => setHoverColor(undefined)}/>
            </Link>
            <div className="ps-2 mt-1" data-ivcs-server-attr="cpu"
            onMouseLeave={() => setIsOpen(false)}>
                <OverlayTrigger
                    onToggle={() => setIsOpen(true)}
                    show={isOpen}
                    placement="bottom"
                    overlay={popover}>
                    <div className={`${isOpen ? 'indicator' : 'text-decoration-none text-dark'}`}>
                        {cpuLoad}
                    </div>
                </OverlayTrigger>
            </div>
        </div>
    );
};

export default CpuIndicator;