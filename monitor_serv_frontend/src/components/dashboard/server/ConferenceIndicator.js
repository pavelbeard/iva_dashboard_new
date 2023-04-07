import {useSelector} from "react-redux";
import {WindowStack} from "react-bootstrap-icons";
import React, {useEffect, useState} from "react";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import axios from "axios";
import {IVCS_API_URL} from "../../../base";

const ConferenceIndicator = () => {
    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    const [conferenceData, setConferenceData] = useState([]);
    const [conferenceCount, setConferenceCount] = useState(0);
    const [isOpen, setIsOpen] = useState(false);
    const [color, setColor] = useState("#000000");

    const getConferences = async () => {
        try {
            const urlRequest = `${IVCS_API_URL}/api/ivcs/conference_data`
            const response = (await axios.get(urlRequest)).data;

            if (response) {
                setConferenceData(response);
                setConferenceCount(response.length);
            }

            setColor("#ff0cdc");
        } catch (err) {
            setColor("#000");
            setConferenceCount(0);
        }
    };

    const setDataImmediately = () => {
        setTimeout(getConferences, 0)
    }

    useEffect(() =>{
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);
    }, [])

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
                    conferenceData.map((i, n = 0) => {
                    return (
                        <tr key={i.parent__name+ "|"
                            + i.conferencesessionactivitystatistic__user_count
                            + "|"
                            + `${n}` }>
                            <td>{i.parent__name}</td>
                            <td>| {i.conferencesessionactivitystatistic__user_count}</td>
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
                        {conferenceCount}
                    </div>
                </OverlayTrigger>
            </div>
        </div>
    )
};

export default ConferenceIndicator;