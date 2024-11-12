import React, { useEffect, useState } from "react";
import { Memory } from "react-bootstrap-icons";
import * as query from "../queries";
import { URL } from "../../../constants";
import { useSelector } from "react-redux";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import axios from "axios";

const MemoryIndicator = ({ host }) => {
  const [memoryStatus, setMemoryStatus] = useState("N/A");
  const [memoryDataTooltip, setMemoryDataTooltip] = useState([]);
  const [color, setColor] = useState("#000000");
  const refreshInterval = useSelector((state) => {
    const interval = localStorage.getItem("refreshInterval");
    if (interval !== null) return interval;
    else return state.refresh.refreshInterval;
  });

  const setMemoryData = async () => {
    try {
      const urlRequest =
        URL +
        `?query=${encodeURI(query.system.memory)}` +
        `&host=${host}` +
        `&query_range=false`;
      const response = (await axios.get(urlRequest)).data;

      if (response.data) {
        const __memoryDataTooltip__ = response.data.result;

        const availMemPrc =
          (1 -
            parseFloat(__memoryDataTooltip__[0]?.value[1]) /
              parseFloat(__memoryDataTooltip__[5]?.value[1])) *
          100;

        if (0 <= availMemPrc && availMemPrc < 50.0) setColor("#16b616");
        else if (50.0 <= availMemPrc && availMemPrc < 75.0) setColor("#ff9900");
        else setColor("#ff0000");

        setMemoryDataTooltip(__memoryDataTooltip__);
        setMemoryStatus(availMemPrc.toFixed(2) + "%");
      }
    } catch (err) {
      setColor("#000000");
      setMemoryStatus("ERR");
      console.log(`${setMemoryData.name}: что-то тут не так...`);
    }
  };

  const setDataImmediately = () => setTimeout(setMemoryData, 0);

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
            <th>| Value</th>
          </tr>
        </thead>
        <tbody>
          {typeof memoryDataTooltip.map === "function"
            ? memoryDataTooltip.map((i) => {
                return (
                  <tr key={i.metric.__name__}>
                    <td>{i.metric.__name__}</td>
                    <td>| {parseFloat(i.value[1]).toFixed(2)}GB</td>
                  </tr>
                );
              })
            : ""}
        </tbody>
      </table>
    </div>
  );

  return (
    <div className="d-flex flex-row justify-content-start mt-1">
      <Memory
        height="24"
        width="24"
        color={color}
        data-ivcs-server-img-attr="memory"
      />
      <div
        className="ps-2 mt-1"
        data-ivcs-server-attr="memory"
        onMouseLeave={() => setIsOpen(false)}
      >
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
            {memoryStatus}
          </div>
        </OverlayTrigger>
      </div>
    </div>
  );
};

export default MemoryIndicator;
