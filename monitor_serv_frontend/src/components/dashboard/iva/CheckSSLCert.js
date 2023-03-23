import React, {useEffect, useState} from 'react'
import '../card/Card.css';
import {ShieldCheck, ShieldExclamation, ShieldX} from "react-bootstrap-icons";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";
import {API_URL, getData} from '../../../base'

const CheckSSLCert = ({refreshInterval}) => {
    const [sslCertStatus, setSslCertStatus] = useState();
    const [sslCertRemainingDays, setSslCertRemainingDays] = useState();
    const [sslIssuer, setSslIssuer] = useState();
    const [sslCertValidFrom, setSslCertValidFrom] = useState();
    const [sslCertValidTo, setSslCertValidTo] = useState();
    const [errors, setErrors] = useState("");
    const [color, setColor] = useState("#000000")

    const setSslData = async () => {
        const data = await getData(`${API_URL}/api/v1/sslcert`);

        if (data) {
            const oneDay = 1000 * Math.pow(60, 2) * 24;
            const validFrom = data.validFrom !== "" ? new Date(data.validFrom) : "";
            const validTo = data.validTo !== "" ? new Date(data.validTo) : "";

            setErrors(data.errors === undefined ? "" : data.errors);

            const sslIssuer = data.issuer.organizationName;
            const remainingDays = Math.round((validTo-validFrom)/oneDay);

            if (remainingDays > 90) {
                setSslCertStatus("OK");
                setColor("#16b616");
            }
            else if (21 <= remainingDays && remainingDays < 90 ) {
                setSslCertStatus("WARN");
                setColor("#ff9900");
            } else {
                setSslCertStatus("DANGER");
                setColor("#ff0000");
            }

            setSslCertValidFrom(validFrom  !== "" ? validFrom.toDateString() : "N/A");
            setSslCertValidTo(validTo !== "" ? validTo.toDateString() : "N/A");
            setSslIssuer(sslIssuer)

            setSslCertRemainingDays(remainingDays);
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
    })

    const setDataImmediately = () => {
        setTimeout(setSslData, 0);
    };

    useEffect(() => {
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval)
    }, []);

    const uuid = v4();

    const getShield = () => {
        let shield;
        if (sslCertStatus === "OK")
            shield = <ShieldCheck height={32} width={32} color={color}/>;
        else if (sslCertStatus === "WARN")
            shield = <ShieldExclamation height={32} width={32} color={color}/>
        else
            shield = <ShieldX height={32} width={32} color={color}/>

        return(shield);
    };

    return(
        <div className="dashboard-card iva">
            <div className="iva">
                <div className="d-flex flex-row justify-content-center mt-3">
                    {sslCertStatus === undefined ? <ShieldX height={32} width={32} color={color}/>: getShield()}
                </div>
                <div className="text-center mt-2">
                    <a data-tooltip-id={uuid}>{sslCertStatus || "N/A"}</a>
                    <Tooltip id={uuid} place="bottom">
                        <div>
                            <div>Осталось дней: {sslCertRemainingDays || 0}</div>
                        </div>
                    </Tooltip>
                </div>
                <div className="text-center mt-2">Мониторинг</div>
                <div className="text-center">сертификата</div>
                <div className="text-center"> WEB-RTC</div>
                <div className="text-center" data-err="cert" style={{
                    transition: ".2s",
                    margin: "20px",
                    width: "80px"
                }}>{errors}</div>
            </div>
            <div className="iva">
                <div className="mt-3">
                    <div>Провайдер:</div>
                    <div className="mt-1 pe-2 iva-left-part">{sslIssuer || "N/A"}</div>
                    <div>Выдан:</div>
                    <div className="mt-1 pe-2 iva-left-part">{sslCertValidFrom || "N/A"}</div>
                    <div>Действует до:</div>
                    <div className="mt-1 pe-2">{sslCertValidTo || "N/A"}</div>
                </div>
            </div>

        </div>
    );
};

export default CheckSSLCert;