import React, {useEffect, useState} from "react";
import ServerCard from "../components/dashboard/card/ServerCard";
import CheckSSLCert from "../components/dashboard/iva/CheckSSLCert";
import {API_URL, getData} from "../base";
import './Containers.css';
import {useDispatch, useSelector} from "react-redux";
import {getServers} from "../slices/serverSlice";


const Dashboard = () => {
    document.title = "Инфопанель | Главная";

    const [data, setData] = useState([]);
    const dispatch = useDispatch();
    const refreshInterval = useSelector(state => {
        const interval = localStorage.getItem('refreshInterval')
        if (interval !== null)
            return interval;
        else
            return state.refresh.refreshInterval;
    });
    const servers = useSelector(state => state.serverManager.servers);

    const getTargets = async () => {
        try {
            const url = `${API_URL}/api/targets/all`;
            const data = await getData(url);

            if (data) {
                setData(data);
            }

        } catch (e) {
            console.log(e);
            setData([]);
        }
    };

    const getTargetsImmediately = () => {
        // console.log(refreshInterval)
        // setTimeout(getTargets, 0);
        dispatch();
        setData(servers);
    }

    useEffect(() => {
        dispatch(getServers())
        const interval1 = setInterval(dispatch, refreshInterval, getServers());
        return () => clearInterval(interval1);

    }, [refreshInterval]);

    return(
        <section className="flex-shrink-0 overflow-auto">
            <div className="d-flex flex-row justify-content-around">
                <div className="ps-2 pe-2">
                    <h4 className="text-center pt-2 pb-2">Мониторинг серверов</h4>
                    <div className="col-md-6 w-100 cards">
                        {servers.map(target => {
                            const card = <ServerCard
                                key={target.address + ":" + target.port}
                                id={target.id}
                                address={target.address}
                                port={target.port}

                            />;
                            return (card);
                        })}
                    </div>
                </div>
                <div className="ps-2 pe-2">
                    <h4 className="text-center pt-2 pb-2">Мониторинг ВКС IVA</h4>
                    <div className="col-md-6 w-100 cards">
                        <CheckSSLCert key={1000023} refreshInterval={refreshInterval}/>
                        {/*<ServerCard/>*/}
                        {/*<ServerCard/>*/}
                        {/*<ServerCard/>*/}
                        {/*<ServerCard/>*/}
                        {/*<ServerCard/>*/}
                        {/*<ServerCard/>*/}
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Dashboard;