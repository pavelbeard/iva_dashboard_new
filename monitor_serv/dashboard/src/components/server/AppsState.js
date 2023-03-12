import React from "react";
import {AppIndicator} from "react-bootstrap-icons";

const AppsState = () => {
    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <AppIndicator height="24" width="24" color="#000000" data-ivcs-server-img-attr="apps"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="apps">N/A</div>
        </div>
    );
};

export default AppsState;