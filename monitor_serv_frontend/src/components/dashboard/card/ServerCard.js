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
import {useSelector} from "react-redux";

const ServerCard = ({id, address, port}) => {
    const [targetHealth, setTargetHealth] = useState(false);
    const refreshInterval = useSelector(state => {
        const interval = sessionStorage.getItem('refreshInterval')
        if (interval !== null)
            return interval;
        else
            return state.refresh.refreshInterval;
    });
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
    }, [refreshInterval]);

    if (!targetHealth)
        return (
            <ServerDown host={host}/>
        );
    else
        return (
            <div className="dashboard-card" id={id}>
                <ServerIndicator key={12} host={host} />
                <div className="server">
                    <CpuIndicator key={13} host={host} />
                    <MemoryIndicator key={14} host={host} />
                    <DeviceSsdIndicator key={15} host={host} />
                    <AppIndicator key={16} host={host} />
                    <NetworkIndicator key={17} host={host} />
                </div>
            </div>
        );
};

export default ServerCard;