import axios from "axios";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { API_URL } from "../../constants";
import ServerCard from "../dashboard/card/ServerCard";
import CheckSSLCert from "../dashboard/iva/CheckSSLCert";
import EventsJournal from "../dashboard/iva/EventsJournal";
import "./Containers.css";

const Dashboard = () => {
  document.title = "Инфопанель | Главная";

  const refreshInterval = useSelector((state) => state.refresh.refreshInterval);
  const [commonServers, setCommonServers] = useState([]);

  const scanServers = async () => {
    try {
      const urlRequest = `${API_URL}/api/targets/all`;
      const response = (await axios.get(urlRequest)).data;

      if (response) {
        setCommonServers(response);
      }
    } catch (err) {
      setCommonServers([]);
    }
  };

  const setDataImmediately = () => {
    setTimeout(scanServers, 0);
  };

  useEffect(() => {
    localStorage["currentPage"] = JSON.stringify({ page: "/dashboard" });
    setDataImmediately();
    const interval1 = setInterval(setDataImmediately, refreshInterval);
    return () => clearInterval(interval1);
  }, [refreshInterval]);

  const servers = (
    <div className="ps-2 pe-2">
      <h4 className="text-center pt-2 pb-2">Мониторинг серверов</h4>
      <div className="col-md-6 w-100 cards">
        {commonServers.map((target) => {
          const card = (
            <ServerCard
              key={target.address + ":" + target.port}
              id={target.id}
              address={target.address}
              port={target.port}
            />
          );
          return card;
        })}
      </div>
    </div>
  );
  const ivcs = (
    <div className="ps-2 pe-2">
      <h4 className="text-center pt-2 pb-2">Мониторинг ВКС IVA</h4>
      <div className="col-md-6 w-100 cards">
        <CheckSSLCert />
        <EventsJournal />
        {/*<ServerCard/>*/}
        {/*<ServerCard/>*/}
        {/*<ServerCard/>*/}
        {/*<ServerCard/>*/}
        {/*<ServerCard/>*/}
      </div>
    </div>
  );

  return (
    <section className="flex-shrink-0 overflow-auto">
      <div className="d-flex flex-row justify-content-around">
        {servers}
        {ivcs}
      </div>
    </section>
  );
};

export default Dashboard;
