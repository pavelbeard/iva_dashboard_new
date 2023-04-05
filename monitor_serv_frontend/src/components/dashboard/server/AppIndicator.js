import {App} from "react-bootstrap-icons";

import './Server.css';
import {useSelector} from "react-redux";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import React, {useEffect, useState} from "react";
import {API_URL} from "../../../base";
import axios from "axios";

const AppIndicator = ({id}) => {
    const hostKey = `host_id${id}`;

    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    const [servicesData, setServicesData] = useState([]);
    const [appsCount, setAppsCount] = useState(0);
    const [color, setColor] = useState("#000000");
    const [isOpen, setIsOpen] = useState(false);
    const [checklistStorage, setChecklistStorage] = useState([]);
    const [_, setChecklistElems] = useState({});

    // 1 принимаем входящие данные
    // 2 создаем список false равный числу входящих данных
    // 3


    const createChecklistStorage = () => {
        const checklist = localStorage.getItem(hostKey);
        const falseArray = new Array(servicesData.length).fill(false);

        if (!checklist) {
            localStorage.setItem(hostKey, falseArray);
        }

        setChecklistStorage(localStorage.getItem(hostKey).split(',').map(
            bool => {return bool === "true"}
        ));
    };

    const updateCheckListStorage = (rows, newArray) => {
        localStorage[hostKey] = newArray;
        setChecklistStorage(localStorage.getItem(hostKey).split(',').map(
            bool => {return bool === "true"}
        ));
    };

    const updateChecklistElems = (key, item) => {
        setChecklistElems(prevState => {
            const dict = {...prevState};
            dict[key] = item;
            localStorage[`checklistElems${id}`] = JSON.stringify(dict);
            return dict;
        });
    }

    const deleteCheckistElemsItem = key => {
        setChecklistElems(prevState => {
            const dict = {...prevState};
            delete dict[key];
            localStorage[`checklistElems${id}`] = JSON.stringify(dict);
            return dict;
        });
    };

    const compare = (oldArray, newArray) => {
        const _newArray_ = newArray.map(service => {return service.metric.___name___})
        const _oldArray_ = oldArray !== null ? typeof oldArray.split === "function" ?
            oldArray.split(',') : [] : [];

        if (_oldArray_.length !== _newArray_.length) {
            return false;
        }

        const filteredArray = _oldArray_.filter(value => newArray.includes(value));

        filteredArray.forEach(value => {
            if (!value) {
                return false;
            }
        });

        return true;
    };

    const colorizeState = state => {
        switch (state) {
            case 'running':
                return "#11ff00";
            case 'stopped':
                return "#ff0000";
            default:
                return "#3b9a4d"
        }
    }

    const handleAppMonitoringList = (e, n) => {
        const parent = e.target.parentElement.parentElement;

        const updatedChecklistStorage = checklistStorage.map((item, index) =>
            index === n ? !item : item
        );
        const rows = parent.parentElement;

        updateCheckListStorage(rows, updatedChecklistStorage);

        const service = parent.querySelector('[data-service="true"]')
            .textContent.replace(/\|\s+/g, '');
        const status = parent.querySelector('[data-status="true"]')
            .textContent.replace(/\|\s+/g, '');
        const elem = {
            color: colorizeState(status),
            service: service
        }

        if (e.target.checked) {
            updateChecklistElems(`item_${n}_${id}`, elem);
        } else {
            deleteCheckistElemsItem(`item_${n}_${id}`, elem);
        }
    };

    const getServicesData = async () => {
        try {
            const urlRequest = `${API_URL}/api/v1/services_status/${id}`;
            const response = (await axios.get(urlRequest)).data;

            if (response.data) {
                setColor("#6e8ff8");

                setServicesData(response.data.result);
                setAppsCount(response.data.result.length);
                createChecklistStorage();
            }
        } catch (err) {
            setColor("#000000");
            setServicesData([]);
            console.log('что-то тут не так');
        }
    }


    const setDataImmediately = () => {
        setTimeout(getServicesData, 0);
    };

    useEffect(() => {
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);
    }, []);


    const checkList = () => {
        if (typeof servicesData.map === "function") {
            return servicesData.map((service, n = 0) => {
                const key = service + "|" + n;
                return(
                    <tr key={key}>
                        <td>
                            <input onClick={e => handleAppMonitoringList(e, n)}
                                   type="checkbox"
                                   defaultChecked={checklistStorage[n]}
                                   disabled={!checklistStorage[n] && checklistStorage.filter(
                                       bool => bool === true
                                   ).length === 6}
                            />
                        </td>
                        <td data-service-num="true">{n}</td>
                        <td data-service="true">| {service.metric.__name__}</td>
                        <td data-status="true" style={{
                            color: `${colorizeState(service.metric.status)}`
                        }}>| {service.metric.status}</td>
                    </tr>
                );
            });
        } else return <></>
    }

    const popover = (
        <div className="bg-dark text-white rounded p-2 tooltip">
            <table className="tooltip-text">
                <thead>
                    <tr>
                        <th></th>
                        <th>#</th>
                        <th>| App name:</th>
                        <th>| Status:</th>
                    </tr>
                </thead>
                <tbody>
                    {checkList()}
                </tbody>
            </table>
        </div>
    );

    return(
        <div className="d-flex flex-row justify-content-start mt-1"
             onMouseLeave={() => setIsOpen(false)}>
            <App height="24" width="24" color={color} data-ivcs-server-img-attr="apps"/>
            <div className="ps-2 mt-1" data-ivcs-server-attr="apps">
                <OverlayTrigger
                    onToggle={() => setIsOpen(true)}
                    show={isOpen}
                    placement="bottom"
                    overlay={popover}>
                    <div className={`${isOpen ? 'indicator' : 'text-decoration-none text-dark'}`}>
                        {appsCount}
                    </div>
                </OverlayTrigger>
            </div>
        </div>
    );
};

export default AppIndicator;