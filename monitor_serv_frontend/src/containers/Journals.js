import React, {useEffect, useState} from "react";
import {CONFIG, IVCS_API_URL} from "../base";
import axios from "axios";
import JournalInfo from "../components/dashboard/iva/JournalInfo";
import {RECORD_TYPE, SEVERITY} from "../components/dashboard/iva/journalFunctions";
import Pagination from "../components/common/Pagination";

const mem = {
    currentPage: undefined
};

const Journals = () => {
    document.title = "Инфопанель | Журнал аудита";

    // const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    const [auditData, setAuditData] = useState([]);
    const [page, setPage] = useState(localStorage['currentPagePaginator']?.page || 1);
    const [pageSize, setPageSize] = useState(10);
    const [lastPage, setLastPage] = useState(0);
    const [prevPage, setPrevPage] = useState();
    const [nextPage, setNextPage] = useState();
    const [pagesRange, setPagesRange] = useState([]);


    const start = () => {
        return new Date().toISOString().slice(0,-8)
    };

    const end = () => {
        const date = new Date();
        date.setDate(date.getDate() + 1);
        return date.toISOString().slice(0, -8);
    };

    const handleChangePage = newPage => {
        localStorage['currentPagePaginator'] = JSON.stringify({page: newPage});
        setPrevPage(newPage - 1);
        setNextPage(newPage + 1);
        setPage(newPage);
    };

    const getAuditLogData = async (page=1, pageSize=25) => {
        try {
            const urlRequest = `${IVCS_API_URL}/api/ivcs/audit_log_events/all?page=${page}&pageSize=${pageSize}`
                // + `&severity=${2}`
                // + `&start=${start}`
                // + `&end=${end}`;
            const response = (await axios.get(urlRequest, CONFIG)).data;

            if (response.results) {
                setAuditData(response.results);
                setLastPage(response.lastPage);
                setPagesRange(response.pagesRange);
            }
        } catch (err) {
            console.log('что-то тут не так...')
        }
    }

    const setDataImmediately = () => {
        setTimeout(getAuditLogData, 0, page, pageSize)
    }

    useEffect(() => {
        localStorage['currentPage'] = JSON.stringify({page: "/journals"});
        setDataImmediately();
    }, [page]);

    const startIndex = page > 1? page * pageSize : 1;

    return(
        <>
            <div className="container-fluid mt-2">
                <div className="row justify-content-between align-items-center">
                    <div className="col-auto">
                        <div className="form-group d-flex flex-row ps-5 align-items-center form-font-size">
                            <label htmlFor="inputDate" className="pe-1">Начало:</label>
                            <input type="datetime-local" id="inputDateStart"
                                   className="form-control"
                                   defaultValue={start()}
                            />
                            <label htmlFor="inputDate" className="ps-2 pe-1">Конец:</label>
                            <input type="datetime-local" id="inputDateEnd"
                                   className="form-control"
                                   defaultValue={end()}
                            />
                            <div className="form-group d-flex flex-row pe-5 form-font-size">
                            <div className="d-flex flex-row align-items-center">
                                <label htmlFor="inputSeverity"
                                       className="access-event-log ms-3 pe-1">Уровень важности:</label>
                                <select name="severity" id="inputSeverity"
                                    className="form-select"
                                    defaultValue="0"
                                >
                                    <option value="0">Любой</option>
                                    <option value="3">{SEVERITY[3][0]}</option>
                                    <option value="2">{SEVERITY[2][0]}</option>
                                    <option value="1">{SEVERITY[1][0]}</option>
                                </select>
                            </div>
                            <div className="d-flex flex-row align-items-center">
                                <label htmlFor="inputRecordType"
                                   className="ps-4 access-event-log">Тип записей:</label>
                                <select name="recordType" id="inputRecordType"
                                    className="form-select"
                                    defaultValue="-1"
                                >
                                    <option value="-1">Любой</option>
                                    <option value="0">{RECORD_TYPE[0][0]}</option>
                                    <option value="1">{RECORD_TYPE[1][0]}</option>
                                    <option value="2">{RECORD_TYPE[2][0]}</option>
                                    <option value="3">{RECORD_TYPE[3][0]}</option>
                                    <option value="4">{RECORD_TYPE[4][0]}</option>
                                    <option value="5">{RECORD_TYPE[5][0]}</option>
                                    <option value="6">{RECORD_TYPE[6][0]}</option>
                                    <option value="7">{RECORD_TYPE[7][0]}</option>
                                    <option value="8">{RECORD_TYPE[8][0]}</option>
                                    <option value="9">{RECORD_TYPE[9][0]}</option>
                                    <option value="10">{RECORD_TYPE[10][0]}</option>
                                    <option value="11">{RECORD_TYPE[11][0]}</option>
                                </select>
                            </div>
                        </div>
                        </div>

                    </div>
                    <div className="ps-5 mt-3">
                        <div className="pe-5">
                            <Pagination currentPage={page} pageCount={pagesRange} lastPage={lastPage}
                                        prevPage={prevPage} nextPage={nextPage}
                                        onPageChange={handleChangePage}/>
                        </div>
                    </div>
                </div>
            </div>
            <div className="container-fluid d-flex mt-3 ps-5 pe-5 audit-log-table">
                <table className="table border-info border-opacity-50" style={{fontSize: "10px"}}>
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th style={{width: "60px"}} scope="col">Дата</th>
                            <th scope="col">Имя пользователя</th>
                            <th scope="col">IP-адрес</th>
                            <th scope="col">Важность</th>
                            <th scope="col">Тип записи</th>
                            <th scope="col">Информация</th>
                        </tr>
                    </thead>
                    <tbody>
                    {auditData.map((item, n) => {
                        // const parsedDate = ;
                        const date = new Date(item['date_created']).toLocaleString('ru-RU');
                        return(<tr key={item['user_ip'] + "|" + n}>
                            <th scope="row">{n + startIndex}</th>
                            <td style={{width: "60px"}}>{date}</td>
                            <td>{item['username']}</td>
                            <td>{item['user_ip']}</td>
                            <td>{SEVERITY[parseInt(item['severity'])][0]} {item['severity']}</td>
                            <td>{RECORD_TYPE[parseInt(item['record_type'])][0]} {item['record_type']}</td>
                            <td><JournalInfo object={JSON.parse(item['info_json'])} /></td>
                        </tr>)
                    })}
                    </tbody>
                </table>
            </div>
        </>
    )
};

export default Journals;