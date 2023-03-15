import React, {useEffect, useState} from "react";
import ServerCard from "../card/ServerCard";
import axios from "axios";
import CheckSSLCert from "../iva/CheckSSLCert";
import {v4} from "uuid";


const Dashboard = () => {
    const [data, setData] = useState([]);
    const [refreshInterval, _] = useState(3000);

    const getTargets = () => {
        axios("/api/v1/targets")
            .then(response => {
                setData(response.data);
            }).catch(err => {
                console.log(err);
                setData([]);
            });
    };


    useEffect(() => {
        getTargets();
        const interval1 = setInterval(getTargets, refreshInterval);

        return () => clearInterval(interval1);

    }, []);

    const randomKey = () => {
        return Math.random() * (1_000_000_000 - 1) + 1;
    };

    return(
        <section className="flex-shrink-0 overflow-auto">
            <div className="d-flex flex-row justify-content-around">
                <div className="ps-2 pe-2">
                    <h4 className="text-center pt-2 pb-2">Мониторинг серверов</h4>
                    <div className="col-md-6 w-100 cards">
                        {data.map((target, i=0) => {
                            const card = <ServerCard
                                key={i}
                                id={target.id}
                                address={target.address}
                                port={target.port}
                                refreshInterval={refreshInterval}
                            />;
                            i++;
                            return (card);
                        })}
                    </div>
                </div>
                <div className="ps-2 pe-2">
                    <h4 className="text-center pt-2 pb-2">Мониторинг ВКС IVA</h4>
                    <div className="col-md-6 w-100 cards">
                        <CheckSSLCert key={1000023} refreshInterval={refreshInterval}/>
                        <ServerCard/>
                        <ServerCard/>
                        <ServerCard/>
                        <ServerCard/>
                        <ServerCard/>
                        <ServerCard/>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Dashboard;