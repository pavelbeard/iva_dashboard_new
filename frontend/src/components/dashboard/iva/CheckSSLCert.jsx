import React, { useEffect, useState } from "react";
import "../card/Card.css";
import { ShieldCheck, ShieldExclamation, ShieldX } from "react-bootstrap-icons";
import { API_URL } from "../../../constants";
import { useSelector } from "react-redux";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import axios from "axios";

const CheckSSLCert = () => {
  const refreshInterval = useSelector((state) => state.refresh.refreshInterval);
  const [sslCertStatus, setSslCertStatus] = useState();
  const [sslCertRemainingDays, setSslCertRemainingDays] = useState();
  const [sslIssuer, setSslIssuer] = useState();
  const [sslCertValidFrom, setSslCertValidFrom] = useState();
  const [sslCertValidTo, setSslCertValidTo] = useState();
  const [errors, setErrors] = useState("");
  const [color, setColor] = useState("#000000");

  const setSslData = async () => {
    try {
      const urlRequest = `${API_URL}/api/v1/sslcert`;
      const response = (await axios.get(urlRequest)).data;

      if (response) {
        const validFrom =
          response.validFrom !== "" ? new Date(response.validFrom) : "";
        const validTo =
          response.validTo !== "" ? new Date(response.validTo) : "";

        setErrors(response.errors === undefined ? "" : response.errors);

        const sslIssuer = response.issuer;
        const remainingDays = response.daysRemaining;

        if (remainingDays > 90) {
          setSslCertStatus("OK");
          setColor("#16b616");
        } else if (21 <= remainingDays && remainingDays < 90) {
          setSslCertStatus("WARN");
          setColor("#ff9900");
        } else {
          setSslCertStatus("DANGER");
          setColor("#ff0000");
        }

        setSslCertValidFrom(
          validFrom !== "" ? validFrom.toDateString() : "N/A",
        );
        setSslCertValidTo(validTo !== "" ? validTo.toDateString() : "N/A");
        setSslIssuer(sslIssuer);

        setSslCertRemainingDays(remainingDays);
      }
    } catch (err) {
      console.log(`${setSslData.name}: что-то тут не так...`);
    }
  };

  const [blink, setBlink] = useState(false);

  const blinkSslErr = () => {
    setBlink(!blink);
    const errElem = document.querySelector('[data-err="cert"]');
    errElem.style.color = blink ? "#ff0000aa" : "#00000066";
    errElem.style.fontWeight = blink ? 500 : 300;
  };

  useEffect(() => {
    const interval = setInterval(blinkSslErr, 500);
    return () => clearInterval(interval);
  }, []);

  const setDataImmediately = () => {
    setTimeout(setSslData, 0);
  };

  useEffect(() => {
    setDataImmediately();
    const interval = setInterval(setDataImmediately, refreshInterval);
    return () => clearInterval(interval);
  }, []);

  /*

    * */
  const popover = (
    <div className="bg-dark text-white rounded p-2 tooltip">
      <div className="tooltip-text">
        Осталось дней: {sslCertRemainingDays || 0}
      </div>
    </div>
  );

  const getShield = () => {
    let shield;
    if (sslCertStatus === "OK")
      shield = <ShieldCheck height={32} width={32} color={color} />;
    else if (sslCertStatus === "WARN")
      shield = <ShieldExclamation height={32} width={32} color={color} />;
    else shield = <ShieldX height={32} width={32} color={color} />;

    return shield;
  };

  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="dashboard-card iva">
      <div className="iva" onMouseLeave={() => setIsOpen(false)}>
        <div className="d-flex flex-row justify-content-center mt-3">
          {sslCertStatus === undefined ? (
            <ShieldX height={32} width={32} color={color} />
          ) : (
            getShield()
          )}
        </div>
        <div className="text-center mt-2" onMouseLeave={() => setIsOpen(false)}>
          <OverlayTrigger
            onToggle={() => setIsOpen(true)}
            placement="bottom"
            overlay={popover}
          >
            <div
              className={`${
                isOpen ? "indicator" : "text-decoration-none text-dark"
              }`}
            >
              {sslCertStatus || "N/A"}
            </div>
          </OverlayTrigger>
        </div>
        <div className="text-center mt-2">Мониторинг</div>
        <div className="text-center">сертификата</div>
        <div className="text-center"> WEB-RTC</div>
        <div
          className="text-center"
          data-err="cert"
          style={{
            transition: ".2s",
            margin: "20px",
            width: "80px",
          }}
        >
          {errors}
        </div>
      </div>
      <div className="iva">
        <div className="mt-3">
          <div>Провайдер:</div>
          <div className="mt-1 pe-2 iva-left-part">{sslIssuer || "N/A"}</div>
          <div>Выдан:</div>
          <div className="mt-1 pe-2 iva-left-part">
            {sslCertValidFrom || "N/A"}
          </div>
          <div>Действует до:</div>
          <div className="mt-1 pe-2">{sslCertValidTo || "N/A"}</div>
        </div>
      </div>
    </div>
  );
};

export default CheckSSLCert;
