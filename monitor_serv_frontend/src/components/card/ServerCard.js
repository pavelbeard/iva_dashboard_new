import React, {useEffect, useState} from "react";
import './Card.css';
import ServerState from '../server/ServerState';
import CpuState from "../server/CpuState";
import MemoryState from "../server/MemoryState";
import DeviceSsdState from "../server/DeviceSsdState";
import AppsState from "../server/AppsState";
import NetworkState from "../server/NetworkState";
import {ServerDown} from "../server/ServerDown";
import {getData} from "../base";

const ServerCard = ({id, address, port, refreshInterval}) => {
    const [targetHealth, setTargetHealth] = useState(false);
    const host = `${address}:${port}`;

    const getTargetHealth = async () => {
        const urlRequest = `${process.env.REACT_APP_BACKEND_URL}/api/v1/target_test`
            + `?host=${host}`;
        const data = await getData(urlRequest);

        if (data) {
            setTargetHealth(data.status === 'success');
        }
    }

    const checkTargetImmediately = () => {
        setTimeout(getTargetHealth,  0);
    };

    useEffect(() => {
        checkTargetImmediately();
        const interval = setInterval(checkTargetImmediately, refreshInterval)
        return () => clearInterval(interval);
    }, []);

    if (!targetHealth)
        return (
            <ServerDown host={host}/>
        );
    else
        return (
            <div className="dashboard-card" id={id}>
                <ServerState key={12} host={host} refreshInterval={refreshInterval}/>
                <div className="server">
                    <CpuState key={13} host={host} refreshInterval={refreshInterval}/>
                    <MemoryState key={14} host={host} refreshInterval={refreshInterval}/>
                    <DeviceSsdState key={15} host={host} refreshInterval={refreshInterval}/>
                    <AppsState key={16} host={host} refreshInterval={refreshInterval}/>
                    <NetworkState key={17} host={host} refreshInterval={refreshInterval}/>
                </div>
            </div>
        );
};

export default ServerCard;