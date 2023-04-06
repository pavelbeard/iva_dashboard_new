import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {pingApi, pingIvcsApi} from "../slices/serverSlice";

const StatusBar = () => {
    const dispatch = useDispatch()
    const apiStatus = useSelector(state => state.serverManager.apiStatus);
    const ivcsApiStatus = useSelector(state => state.serverManager.ivcsApiStatus);
    const isAuthenticated = useSelector(state => state.auth.isAuthenticated);

    const setStatusImmediately = () => {
        setTimeout(dispatch, 0, pingApi());
        setTimeout(dispatch, 0, pingIvcsApi());
    }

    useEffect(() => {
        setStatusImmediately();
        const interval = setInterval(setStatusImmediately,5000);
        return () => clearInterval(interval);
    }, [apiStatus, ivcsApiStatus])

    if (isAuthenticated) {
        return(
            <div className="container-fluid bg-info bg-opacity-25 d-flex flex-row">
                <div className="text-white">
                    <div>API Status: {apiStatus}</div>
                    <div>IVCS API Status: {ivcsApiStatus}</div>
                </div>
                <div className="ms-3 text-white">
                    <div>Knocking IP: 127.0.0.1</div>
                    <div>X</div>
                </div>
            </div>
        );
    }

    return <></>;
};

export default StatusBar;