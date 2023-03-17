import React, {useEffect, useState} from "react";
import './Card.css';
import ServerState from '../server/ServerState';
import CpuState from "../server/CpuState";
import MemoryState from "../server/MemoryState";
import DeviceSsdState from "../server/DeviceSsdState";
import AppsState from "../server/AppsState";
import NetworkState from "../server/NetworkState";
import {v4} from "uuid";
import axios from "axios";
import {AppIndicator, Cpu, DeviceSsd, Ethernet, Memory, Server} from "react-bootstrap-icons";
import {Tooltip} from "react-tooltip";
import {ServerDown} from "../server/ServerDown";

const ServerCard = ({id, address, port, refreshInterval}) => {
    const [targetHealth, setTargetHealth] = useState(false);
    const host = `${address}:${port}`;

    const getTargetHealth = async () => {
        return await axios.get(`/api/v1/target_test/${host}`)
            .then(response => response.data);
    }

    useEffect(() => {
        setTimeout(async () => {
            const targetHealth = await getTargetHealth();
            setTargetHealth(targetHealth.status === 'success');
        }, refreshInterval);
    });

    if (!targetHealth)
        return (
            <ServerDown host={host}/>
        );
    else
        return (
            <div className="dashboard-card" id={id}>
                <ServerState key={12}
                             host={host}
                             refreshInterval={refreshInterval}
                             targetHealth={targetHealth}/>
                <div className="server">
                    <CpuState key={13}
                              host={host}
                              refreshInterval={refreshInterval}
                              targetHealth={targetHealth}/>
                    <MemoryState key={14}
                                 host={host}
                                 refreshInterval={refreshInterval}
                                 targetHealth={targetHealth}/>
                    <DeviceSsdState key={15}
                                    host={host}
                                    refreshInterval={refreshInterval}
                                    targetHealth={targetHealth}/>
                    <AppsState key={16}
                               host={host}
                               refreshInterval={refreshInterval}
                               targetHealth={targetHealth}/>
                    <NetworkState key={17}
                                  host={host}
                                  refreshInterval={refreshInterval}
                                  targetHealth={targetHealth}/>
                </div>
            </div>
        );
};

export default ServerCard;