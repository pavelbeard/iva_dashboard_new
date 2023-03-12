import React from "react";
import {DeviceSsd} from "react-bootstrap-icons";

const DeviceSsdState = () => {
    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <DeviceSsd height="24" width="24" color="#000000" data-ivcs-server-img-attr="filespace"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="filespace">N/A</div>
        </div>
    );
};

export default DeviceSsdState;