import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {auditLogEvent, pingApi, pingIvcsApi} from "../slices/serverSlice";
import {parseInfo} from "../components/dashboard/iva/journalFunctions";

const StatusBar = () => {
    const dispatch = useDispatch()
    const {apiStatus, ivcsApiStatus, auditLogLastEvents} = useSelector(state => state.serverManager);
    const isAuthenticated = useSelector(state => state.auth.isAuthenticated);

    const auditLogEventsColor = errorType => {
        switch (errorType) {
            case "BLOCKED_ACCESS_FROM_IP":
            case "BLOCKED_ACCESS_FROM_PROFILE":
                return "#ff0000";
            case "INVALID_CREDENTIALS":
            case "INCORRECT_EVENT_ID":
                return "#ff9900";
            default:
                return "#fff";
        }

    };

    const setStatusImmediately = () => {
        setTimeout(dispatch, 0, pingApi());
        setTimeout(dispatch, 0, pingIvcsApi());
        setTimeout(dispatch, 0, auditLogEvent({secureAudit: true, severity: 2}));
    };

    useEffect(() => {
        setStatusImmediately();
        const interval = setInterval(setStatusImmediately,5000);
        return () => clearInterval(interval);
    }, [apiStatus, ivcsApiStatus]);

    const lastWarningEvents = () => {
        try {
            const userIp = auditLogLastEvents[0]['user_ip'];
            let errorType = parseInfo(JSON.parse(auditLogLastEvents[0]['info_json']));
            let style;
            const infoJson = JSON.parse(auditLogLastEvents[0]['info_json']);

            if (infoJson?.accessErrorType) {
                style = auditLogEventsColor(infoJson.accessErrorType);
            } else if (infoJson?.username && infoJson?.reason) {
                style = auditLogEventsColor(infoJson.reason);
            }

            return [userIp, errorType, style];
        } catch (err) {
            return ["❌", "", ""]
        }
    };

    const [lastWarningEvent, reason, color] = lastWarningEvents();

    if (isAuthenticated) {
        return(
            <div className="container-fluid bg-info bg-opacity-25 d-flex flex-row pb-2">
                <div className="text-white">
                    <div className="d-flex">
                        <div className="status-bar-table">
                            <div>API Статус:</div><div>{apiStatus}</div>
                            {/*<div>IVCS API Статус:</div><div>{ivcsApiStatus}</div>*/}
                        </div>
                    </div>
                </div>
                <div className="text-white">
                    <div className="d-flex">
                        <div>Аудит безопасности:</div>
                        <div className="ms-2 status-bar-table-events">
                            <div>IP:</div><div style={{color: color}}>{lastWarningEvent}</div>
                            <div>Причина:</div><div style={{color: color}}>{reason}</div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return <></>;
};

export default StatusBar;