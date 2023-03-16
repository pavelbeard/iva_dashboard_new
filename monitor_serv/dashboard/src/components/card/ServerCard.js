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
            <ServerState key={12} address={address} port={port} refreshInterval={refreshInterval}/>
            <div className="server">
                <CpuState key={13} address={address} port={port} refreshInterval={refreshInterval}/>
                <MemoryState key={14} address={address} port={port} refreshInterval={refreshInterval}/>
                <DeviceSsdState key={15} address={address} port={port} refreshInterval={refreshInterval}/>
                <AppsState key={16} address={address} port={port} refreshInterval={refreshInterval}/>
                <NetworkState key={17} address={address} port={port} refreshInterval={refreshInterval}/>
            </div>
        </div>
    );
};

export default ServerCard;