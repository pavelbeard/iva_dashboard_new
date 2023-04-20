import {JournalText} from "react-bootstrap-icons";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import React, {useEffect, useState} from "react";
import {useSelector} from "react-redux";
import {Link} from "react-router-dom";
import {parseInfo} from "./journalFunctions";
import {CONFIG, IVCS_API_URL} from "../../../base";
import axios from "axios";
const EventsJournal = () => {
    const [color, setColor] = useState("#06567c")

    const popover = data => {
        const infoJson = parseInfo(JSON.parse(data)) || "unknown";
        return(
            <div className="bg-dark text-white rounded p-2 tooltip">
                {infoJson}
            </div>
        );
    };

    const setStyle = (e, className) => {
        e.target.className = className;
    };

    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    const [auditData, setAuditData] = useState([]);

    const getAuditLogData = async () => {
        try {
            const urlRequest = `${IVCS_API_URL}/api/ivcs/audit_log_events?page=1&page_size=9`
            const response = (await axios.get(urlRequest, CONFIG)).data;

            if (response.results) {
                const results = response.results;
                setAuditData(results);
            }
        } catch (err) {
            console.log('что-то тут не так...')
        }
    }

    const setDataImmediately = () => {
        setTimeout(getAuditLogData, 0);
    };

    useEffect(() => {
        setDataImmediately()
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);
    }, [refreshInterval])

    return(
        <div className="dashboard-card iva">
            <div className="iva">
                <div className="d-flex flex-row justify-content-center mt-3">
                    <Link to="/journals">
                        <JournalText height={32} width={32} color={color}
                                     onMouseEnter={() => setColor("#fff")}
                                     onMouseLeave={() => setColor( "#06567c")}/>
                    </Link>
                </div>
                <div className="text-center mt-2">
                    -
                </div>
                <div className="text-center mt-2">Журнал</div>
                <div className="text-center">событий</div>
            </div>
            <div className="iva mt-3">
                <table>
                    <thead>
                        <tr>
                            <th>№</th>
                            <th>| IP-адрес</th>
                        </tr>
                    </thead>
                    <tbody>
                        {auditData.slice(0,9)?.map((i, n=0) => {

                            return(
                                <OverlayTrigger
                                    placement="bottom"
                                    overlay={popover(i['info_json'])}>
                                        <tr key={i['user_ip'] + `${n}`}>
                                            <td>{n + 1}. </td>
                                            <td
                                                 onMouseEnter={e=> {
                                                 setStyle(e, 'indicator')
                                            }}   onMouseLeave={e =>
                                                 setStyle(e, 'text-decoration-none text-dark')}>
                                                 {i['user_ip'] || "none"}
                                            </td>
                                        </tr>
                                </OverlayTrigger>
                            )
                        })}
                    </tbody>
                </table>

            </div>
        </div>
    )
};

export default EventsJournal;