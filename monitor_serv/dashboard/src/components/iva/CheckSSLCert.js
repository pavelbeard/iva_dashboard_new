import React, {useEffect, useState} from 'react'
import '../card/Card.css';
import axios from "axios";
import {ShieldCheck, ShieldExclamation, ShieldX} from "react-bootstrap-icons";
import {v4} from "uuid";
import {Tooltip} from "react-tooltip";


const CheckSSLCert = ({refreshInterval}) => {
    const [sslCertStatus, setSslCertStatus] = useState();
    const [sslCertRemainingDays, setSslCertRemainingDays] = useState();
    const [sslIssuer, setSslIssuer] = useState();
    const [sslCertValidFrom, setSslCertValidFrom] = useState();
    const [sslCertValidTo, setSslCertValidTo] = useState();
    const [color, setColor] = useState("#000000")

    useEffect(() => {
        const interval = refreshInterval ? setInterval(() => {
            axios.get("/api/v1/ssl_test")
                .then(response => {
                    if (response.data) {
                        const oneDay = 1000 * Math.pow(60, 2) * 24;
                        const validFrom = new Date(response.data.validFrom);
                        const validTo = new Date(response.data.validTo);
                        const sslIssuer = response.data.issuer.organizationName;
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

                        setSslCertValidFrom(validFrom.toDateString());
                        setSslCertValidTo(validTo.toDateString());
                        setSslIssuer(sslIssuer)

                        setSslCertRemainingDays(remainingDays);
                    }
                });
        }, refreshInterval) : 5000;

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
                    <a data-tooltip-id={uuid}>{sslCertStatus === undefined ? "N/A" : sslCertStatus}</a>
                    <Tooltip id={uuid} place="bottom">
                        <div>
                            <div>Осталось дней: {sslCertRemainingDays === undefined ? 0 : sslCertRemainingDays}</div>
                        </div>
                    </Tooltip>
                </div>
                <div className="text-center mt-2">Мониторинг</div>
                <div className="text-center">сертификата</div>
                <div className="text-center"> WEB-RTC</div>
            </div>
            <div className="iva">
                <div className="mt-3">
                    <div>Провайдер:</div>
                    <div className="mt-1 pe-1 iva-left-part">{sslIssuer === undefined ? "N/A" : sslIssuer}</div>
                    <div>Выдан:</div>
                    <div className="mt-1 pe-1 iva-left-part">{sslCertValidFrom === undefined ? "N/A" :
                        sslCertValidFrom}</div>
                    <div>Действует до:</div>
                    <div className="mt-1 pe-1">{sslCertValidTo === undefined ? "N/A" :
                        sslCertValidTo}</div>
                </div>
            </div>

        </div>
    );
};

export default CheckSSLCert;