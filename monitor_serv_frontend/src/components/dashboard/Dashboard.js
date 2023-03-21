import React, {useEffect, useState} from "react";
import ServerCard from "../card/ServerCard";
import CheckSSLCert from "../iva/CheckSSLCert";
import {getData} from "../base";


const Dashboard = () => {
    const [data, setData] = useState([]);
    const [refreshInterval, _] = useState(5000);

    const getTargets = async () => {
        try {
            const url = `${process.env.REACT_APP_BACKEND_URL}/api/targets/all`;
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
        setTimeout(getTargets, 0);
    }

    useEffect(() => {
        getTargetsImmediately();
        const interval1 = setInterval(getTargetsImmediately, refreshInterval);
        return () => clearInterval(interval1);

    }, []);

    return(
        <section className="flex-shrink-0 overflow-auto">
            <div className="d-flex flex-row justify-content-around">
                <div className="ps-2 pe-2">
                    <h4 className="text-center pt-2 pb-2">Мониторинг серверов</h4>
                    <div className="col-md-6 w-100 cards">
                        {data.map(target => {
                            const card = <ServerCard
                                key={target.address + ":" + target.port}
                                id={target.id}
                                address={target.address}
                                port={target.port}
                                refreshInterval={refreshInterval}
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