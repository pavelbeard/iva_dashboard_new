import React, {useEffect, useState} from "react";
import './Card.css';
import ServerState from '../server/ServerState';
import CpuState from "../server/CpuState";
import MemoryState from "../server/MemoryState";
import DeviceSsdState from "../server/DeviceSsdState";
import AppsState from "../server/AppsState";
import NetworkState from "../server/NetworkState";
import {v4} from "uuid";

const ServerCard = ({id, address, port, refreshInterval}) => {

    return (
        <div className="dashboard-card" id={id}>
            <ServerState key={2484242} address={address} port={port} refreshInterval={refreshInterval}/>
            <div className="server">
                <CpuState key={434873} address={address} port={port} refreshInterval={refreshInterval}/>
                <MemoryState key={34658767} address={address} port={port} refreshInterval={refreshInterval}/>
                <DeviceSsdState key={3435786} address={address} port={port} refreshInterval={refreshInterval}/>
                <AppsState key={354867}/>
                <NetworkState key={3424030} address={address} port={port} refreshInterval={refreshInterval}/>
            </div>
        </div>
    );
};

export default ServerCard;