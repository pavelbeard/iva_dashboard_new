import React, {useState} from "react";
import './Card.css';
import ServerState from '../server/ServerState';
import CpuState from "../server/CpuState";
import MemoryState from "../server/MemoryState";
import DeviceSsdState from "../server/DeviceSsdState";
import AppsState from "../server/AppsState";
import NetworkState from "../server/NetworkState";

const ServerCard = ({id, address, port, refreshInterval}) => {
    const data = {data: []};

    // fetch(`http://${address}:${port}/api/v1/query`)

    return (
        <div className="dashboard-card server" id={id}>
            <ServerState key={120} address={address} port={port} refreshInterval={refreshInterval}/>
            <div>
                <CpuState key={130}/>
                <MemoryState key={140}/>
                <DeviceSsdState key={150}/>
                <AppsState key={160}/>
                <NetworkState key={170}/>
            </div>
        </div>
    );
};

export default ServerCard;