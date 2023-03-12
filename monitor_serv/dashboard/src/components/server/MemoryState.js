import React from "react";
import {Memory} from "react-bootstrap-icons";

const MemoryState = () => {
    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <Memory height="24" width="24" color="#000000" data-ivcs-server-img-attr="memory"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="memory">N/A</div>
        </div>
    );
};

export default MemoryState;