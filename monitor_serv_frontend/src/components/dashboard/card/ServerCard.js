import React, {useEffect, useState} from "react";
import './Card.css';
import ServerIndicator from '../server/ServerIndicator';
import CpuIndicator from "../server/CpuIndicator";
import MemoryIndicator from "../server/MemoryIndicator";
import DeviceSsdIndicator from "../server/DeviceSsdIndicator";
import AppIndicator from "../server/AppIndicator";
import NetworkIndicator from "../server/NetworkIndicator";
import {ServerDown} from "../server/ServerDown";
import {getData, API_URL} from "../../../base";

const ServerCard = ({id, address, port, refreshInterval}) => {
    const [targetHealth, setTargetHealth] = useState(false);
    const host = `${address}:${port}`;

    const getTargetHealth = async () => {
        const urlRequest = `${API_URL}/api/v1/target_test`
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
                <ServerIndicator key={12} host={host} refreshInterval={refreshInterval}/>
                <div className="server">
                    <CpuIndicator key={13} host={host} refreshInterval={refreshInterval}/>
                    <MemoryIndicator key={14} host={host} refreshInterval={refreshInterval}/>
                    <DeviceSsdIndicator key={15} host={host} refreshInterval={refreshInterval}/>
                    <AppIndicator key={16} host={host} refreshInterval={refreshInterval}/>
                    <NetworkIndicator key={17} host={host} refreshInterval={refreshInterval}/>
                </div>
            </div>
        );
};

export default ServerCard;