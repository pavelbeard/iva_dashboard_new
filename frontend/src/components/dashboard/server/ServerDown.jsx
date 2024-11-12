import React from "react";
import {
  AppIndicator,
  X,
  Cpu,
  DeviceSsd,
  Ethernet,
  Memory,
  WindowStack,
  DatabaseFillDown,
} from "react-bootstrap-icons";

export const ServerDown = ({ host }) => {
  return (
    <div className="dashboard-card" key={host}>
      <div className="server">
        <div className="ms-1 mt-1">
          <div>
            <X width="20" height="20" />
          </div>
        </div>
        <div className="d-flex flex-row justify-content-center mt-3">
          <DatabaseFillDown
            height="32"
            width="32"
            color={"#ff0000"}
            data-ivcs-server-img-attr="server"
          />
        </div>
        <div className="text-center mt-2" data-ivcs-server-attr="status">
          none
        </div>
        <div className="text-center mt-2" data-ivcs-server-attr="address">
          {host}
        </div>
      </div>
      <div className="server bg-danger ps-1 rounded-end bg-opacity-25">
        <div className="d-flex flex-row justify-content-start mt-3">
          <Cpu
            height="24"
            width="24"
            color={"#000000"}
            data-ivcs-server-img-attr="cpu"
          />
          <div className="ps-2 mt-1" data-ivcs-server-attr="cpu">
            N/A
          </div>
        </div>
        <div className="d-flex flex-row justify-content-start mt-1">
          <Memory
            height="24"
            width="24"
            color={"#000000"}
            data-ivcs-server-img-attr="memory"
          />
          <div className="ps-2 mt-1" data-ivcs-server-attr="memory">
            N/A
          </div>
        </div>
        <div className="d-flex flex-row justify-content-start mt-1">
          <DeviceSsd
            height="24"
            width="24"
            color={"#000000"}
            data-ivcs-server-img-attr="filespace"
          />
          <div className="ps-2 mt-1" data-ivcs-server-attr="filespace">
            N/A
          </div>
        </div>
        <div className="d-flex flex-row justify-content-start mt-1">
          <AppIndicator
            height="24"
            width="24"
            color={"#000000"}
            data-ivcs-server-img-attr="apps"
          />
          <div className="ps-2 mt-1" data-ivcs-server-attr="apps">
            N/A
          </div>
        </div>
        <div className="d-flex flex-row justify-content-start mt-1">
          <Ethernet
            height="24"
            width="24"
            color={"#000000"}
            data-ivcs-server-img-attr="net"
          />
          <div className="ps-2 mt-1" data-ivcs-server-attr="net">
            N/A
          </div>
        </div>
        <div className="d-flex flex-row justify-content-start mt-1">
          <WindowStack
            height="24"
            width="24"
            color={"#000000"}
            data-ivcs-server-img-attr="net"
          />
          <div className="ps-2 mt-1" data-ivcs-server-attr="net">
            N/A
          </div>
        </div>
      </div>
    </div>
  );
};
