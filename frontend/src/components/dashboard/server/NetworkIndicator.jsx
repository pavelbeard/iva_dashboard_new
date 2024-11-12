import axios from "axios";
import React, { useEffect, useState } from "react";
import { Ethernet } from "react-bootstrap-icons";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import { useSelector } from "react-redux";

import { URL } from "../../../constants";
import * as query from "../queries";

const NetworkIndicator = ({ host }) => {
  const [netStatus, setNetStatus] = useState("N/A");
  const [netDataTooltip, setNetDataTooltip] = useState([]);
  const [color, setColor] = useState("#000000");
  const refreshInterval = useSelector((state) => {
    const interval = localStorage.getItem("refreshInterval");
    if (interval !== null) return interval;
    else return state.refresh.refreshInterval;
  });

  const getNetworkData = async () => {
    try {
      const urlRequest =
        URL +
        `?query=${encodeURI(query.network.throughput)}` +
        `&host=${host}` +
        `&query_range=false`;
      const response = (await axios.get(urlRequest)).data;

      if (response.data) {
        setNetStatus("UP");

        const __netDataTooltip__ = response.data.result;

        setNetDataTooltip(__netDataTooltip__);
        setColor("#16b616");
      }
    } catch (err) {
      setColor("#000000");
      setNetStatus("ERR");
      console.log(`${getNetworkData.name}: что-то тут не так...`);
    }
  };

  const setDataImmediately = () => {
    setTimeout(getNetworkData, 0);
  };

  useEffect(() => {
    setDataImmediately();
    const interval = setInterval(setDataImmediately, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  const [isOpen, setIsOpen] = useState(false);

  const popover = (
    <div className="bg-dark text-white rounded p-2 tooltip">
      <table className="tooltip-text">
        <thead>
          <tr>
            <th>Metric</th>
            <th>Device</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {typeof netDataTooltip.map === "function"
            ? netDataTooltip.map((i) => {
                return (
                  <tr key={i.metric.__name__ + "|" + i.metric.device}>
                    <td>{i.metric.__name__}</td>
                    <td>{i.metric.device}</td>
                    <td>{parseFloat(i.value[1]).toFixed(2)} mbps</td>
                  </tr>
                );
              })
            : ""}
        </tbody>
      </table>
    </div>
  );

  return (
    <div
      className="d-flex flex-row justify-content-start mt-1"
      onMouseLeave={() => setIsOpen(false)}
    >
      <Ethernet
        height="24"
        width="24"
        color={color}
        data-ivcs-server-img-attr="net"
      />
      <div className="ps-2 mt-1" data-ivcs-server-attr="net">
        <OverlayTrigger
          onToggle={() => setIsOpen(true)}
          show={isOpen}
          placement="bottom"
          overlay={popover}
        >
          <div
            className={`${
              isOpen ? "indicator" : "text-decoration-none text-dark"
            }`}
          >
            {netStatus}
          </div>
        </OverlayTrigger>
      </div>
    </div>
  );
};

export default NetworkIndicator;
