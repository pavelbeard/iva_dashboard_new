import React from "react";
import {Ethernet} from "react-bootstrap-icons";

const NetworkState = () => {
    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <Ethernet height="24" width="24" color="#000000" data-ivcs-server-img-attr="net"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="net">N/A</div>
        </div>
    );
};

export default NetworkState;