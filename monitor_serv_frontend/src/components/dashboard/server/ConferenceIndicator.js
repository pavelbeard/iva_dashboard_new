import {useDispatch, useSelector} from "react-redux";
import {WindowStack} from "react-bootstrap-icons";
import React, {useEffect, useState} from "react";
import {getConfData} from "../../../slices/indicatorSlice";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";

const ConferenceIndicator = () => {
    const dispatch = useDispatch();
    const conferenceData = useSelector(state => state.indicatorManager.conferenceData);
    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    const [isOpen, setIsOpen] = useState(false);
    const color = "#ff0cdc";

    useEffect(() =>{
        const interval = setInterval(() => {
            dispatch(getConfData())
        }, refreshInterval);
        return () => clearInterval(interval);
    })

    const popover = (
        <div className="bg-dark text-white rounded p-2 tooltip">
            <table className="tooltip-text">
                <thead>
                <tr>
                    <th>Conference name</th>
                    <th>| User count</th>
                </tr>
                </thead>
                <tbody>
                {typeof conferenceData.map === "function" ?
                    conferenceData.map(i => {
                    return (
                        <tr key={i.metric.__name__ + "|" + i.metric.device}>
                            <td>{i.metric.__name__}</td>
                            <td>| {i.metric.device}</td>
                        </tr>
                    )
                }) : ""}
                </tbody>
            </table>
        </div>
    );

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <WindowStack height="24" width="24" color={color} data-ivcs-server-img-attr="net"/>
            <div className="ps-2 mt-1" data-ivcs-server-attr="net"
                 onMouseLeave={() => setIsOpen(false)}>
                <OverlayTrigger
                    onToggle={() => setIsOpen(true)}
                    show={isOpen}
                    placement="bottom"
                    overlay={popover}>
                    <div className={`${isOpen ? 'indicator' : 'text-decoration-none text-dark'}`}>
                        {conferenceData.length}
                    </div>
                </OverlayTrigger>
            </div>
        </div>
    )
};

export default ConferenceIndicator;