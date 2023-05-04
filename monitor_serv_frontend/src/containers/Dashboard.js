import React, {useEffect, useState} from "react";
import ServerCard from "../components/dashboard/card/ServerCard";
import CheckSSLCert from "../components/dashboard/iva/CheckSSLCert";
import {useDispatch, useSelector} from "react-redux";

import './Containers.css';
import {API_URL} from "../base";
import axios from "axios";
import EventsJournal from "../components/dashboard/iva/EventsJournal";
import {getServers} from "../slices/serverSlice";


const Dashboard = () => {
    document.title = "Инфопанель | Главная";

    const dispatch = useDispatch();
    const commonServers = useSelector(state => state.serverManager.serversList);
    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    // const [commonServers, setCommonServers] = useState([]);

    // const scanServers = async () => {
    //     dispatch(getServers())
        // try {
        //     const urlRequest = `${API_URL}/api/targets/all`;
        //     const response = (await axios.get(urlRequest)).data;
        //
        //     if (response) {
        //         setCommonServers(response);
        //     }
        //
        // } catch (err) {
        //     setCommonServers([]);
        // }
    // }

    const setDataImmediately = () => {
        setTimeout(dispatch, 0, getServers());
    };

    useEffect(() => {
        localStorage['currentPage'] = JSON.stringify({page: "/dashboard"});
        setDataImmediately();
        const interval1 = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval1);

    }, [refreshInterval]);

    const servers = (
        <div className="ps-2 pe-2">
            <h4 className="text-center pt-2 pb-2">Мониторинг серверов</h4>
            <div className="col-md-6 w-100 cards">
                {typeof commonServers.map === "function" ? commonServers.map(target => {
                    const card = <ServerCard
                        key={target.address + ":" + target.port}
                        id={target.id}
                        address={target.address}
                        port={target.port}
                    />;
                    return (card);
                }) : ""}
            </div>
        </div>
    );
    const ivcs = (
        <div className="ps-2 pe-2">
            <h4 className="text-center pt-2 pb-2">Мониторинг ВКС IVA</h4>
            <div className="col-md-6 w-100 cards">
                <CheckSSLCert/>
                <EventsJournal/>
                {/*<ServerCard/>*/}
                {/*<ServerCard/>*/}
                {/*<ServerCard/>*/}
                {/*<ServerCard/>*/}
                {/*<ServerCard/>*/}
            </div>
        </div>
    );

    return(
        <section className="flex-shrink-0 overflow-auto">
            <div className="d-flex flex-row justify-content-around">
                {servers}
                {ivcs}
            </div>
        </section>
    );
};

export default Dashboard;