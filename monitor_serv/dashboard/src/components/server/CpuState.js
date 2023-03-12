import React, {useState} from "react";
import {Cpu} from "react-bootstrap-icons";

const CpuState = ({address, port, refreshInterval}) => {
    const [cpuStatus, setCpuStatus] = useState("N/A");
    const [color, setColor] = useState("#000000");

    return(
        <div className="d-flex flex-row justify-content-start mt-3">
            <Cpu height="24" width="24" color={color} data-ivcs-server-img-attr="cpu"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="cpu">N/A</div>
        </div>
    );
};

export default CpuState;