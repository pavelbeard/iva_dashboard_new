import React, {useEffect, useState} from "react";
import './Card.css';
import ServerIndicator from '../server/ServerIndicator';
import CpuIndicator from "../server/CpuIndicator";
import MemoryIndicator from "../server/MemoryIndicator";
import DeviceSsdIndicator from "../server/DeviceSsdIndicator";
import ThreadAppIndicator from "../server/ThreadAppIndicator";
import NetworkIndicator from "../server/NetworkIndicator";
import ConferenceIndicator from "../server/ConferenceIndicator";
import {ServerDown} from "../server/ServerDown";
import {API_URL, parse} from "../../../base";
import {useSelector} from "react-redux";
import AppIndicator from "../server/AppIndicator";
import axios from "axios";
import {setAuthenticationState} from "../../../slices/authSlice";

const ServerCard = ({id, address, port}) => {
    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    const [targetHealth, setTargetHealth] = useState(false);
    const [role, setRole] = useState('NONE');
    const host = `${address}:${port}`;

    const getTargetHealth = async () => {
        try {
            const urlRequest = `${API_URL}/api/v1/target_test`
                + `?host=${host}`;
            const response = (await axios.get(urlRequest)).data;

            if (response.status) {
                setTargetHealth(response.status === 'success');

                setRole(parse(host) || "NONE")
            }
        } catch (err) {
            setTargetHealth(false);
            // setAuthenticationState({isAuthenticated: false});
            console.log(`${getTargetHealth.name}: что-то тут не так...`);
        }
    };

    const checkTargetImmediately = () => {
        setTimeout(getTargetHealth,  0);
    };

    useEffect(() => {
        checkTargetImmediately();
        const interval = setInterval(checkTargetImmediately, refreshInterval)
        return () => clearInterval(interval);
    }, [refreshInterval]);

    const conferenceIndicator = <ConferenceIndicator key={18} host={host} />

    if (!targetHealth)
        return (
            <ServerDown host={host}/>
        );
    else
        return (
            <div className="dashboard-card" id={id}>
                <ServerIndicator id={id} key={12} host={host}/>
                <div className="server bg-success ps-1 rounded-end bg-opacity-25">
                    <CpuIndicator key={13} host={host} />
                    <MemoryIndicator key={14} host={host} />
                    <DeviceSsdIndicator key={15} host={host} />
                    <ThreadAppIndicator key={16} host={host} />
                    <AppIndicator id={id} key={19} host={host} />
                    <NetworkIndicator key={17} host={host} />
                    {role === 'MEDIA' ? conferenceIndicator : ""}
                </div>
            </div>
        );
};

export default ServerCard;