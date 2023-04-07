import {App} from "react-bootstrap-icons";

import './Server.css';
import {useSelector} from "react-redux";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import React, {useEffect, useState} from "react";
import {API_URL} from "../../../base";
import axios from "axios";
import app from "../../../App";

const AppIndicator = ({id}) => {
    const hostKey = `host_id${id}`;
    const appListKey = `checklistElems${id}`;

    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    const [appData, setAppData] = useState([]);
    const [appsCount, setAppsCount] = useState(0);
    const [color, setColor] = useState("#000000");
    const [isOpen, setIsOpen] = useState(false);
    const [checklistStorage, setChecklistStorage] = useState([]);

    const parse = key => {
        try {
            return JSON.parse(localStorage[key]);
        } catch (err) {
            return undefined;
        }
    }

    // 1 принимаем входящие данные
    const getAppData = async () => {
        try {
            const urlRequest = `${API_URL}/api/v1/services_status/${id}`;
            const response = (await axios.get(urlRequest)).data;

            if (response.data) {
                setColor("#6e8ff8");

                setAppData(response.data.result);
                setAppsCount(response.data.result.length);
                createChecklistStorage(response.data.result.length);
            }
        } catch (err) {
            setColor("#000000");
            setAppData([]);
            console.log('что-то тут не так');
        }
    };

    // 2 создаем список false равный числу входящих данных
    // при этом используем localStorage
    const createChecklistStorage = length => {
        const checklist = parse(hostKey);
        const falseArray = new Array(length).fill(false);

        if (!checklist) {
            localStorage[hostKey] = JSON.stringify(falseArray);
        }

        setChecklistStorage(parse(hostKey));
    };

    const updateCheckListStorage = (rows, newArray) => {
        localStorage[hostKey] = JSON.stringify(newArray);
        setChecklistStorage(parse(hostKey));
    };

    const updateAppList = srcItem => {
        const prevData = parse(appListKey);

        if (prevData?.length > 0) {
            const copy = [...prevData];
            copy.push(srcItem);
            localStorage[`checklistElems${id}`] = JSON.stringify(copy);
        } else {
            localStorage[`checklistElems${id}`] = JSON.stringify([srcItem]);
        }
    };

    const deleteAppListItem = srcElem => {
        const prevData = parse(appListKey);

        if (prevData?.length > 0) {
            const copy = [...prevData];
            const newArray = copy.filter(elem => elem.name !== srcElem.name);
            localStorage[appListKey] = JSON.stringify(newArray);
        }
    };

    const colorizeState = state => {
        switch (state) {
            case 'running':
                return "#00f830";
            case 'stopped':
                return "#ff0000";
            default:
                return "#000"
        }
    }

    const handleAppMonitoringList = (e, n) => {
        const parent = e.target.parentElement.parentElement;

        const updatedChecklistStorage = checklistStorage.map((item, index) =>
            index === n ? !item : item
        );
        const rows = parent.parentElement;

        //3 обновляем хранилище
        updateCheckListStorage(rows, updatedChecklistStorage);

        const appName = parent.querySelector('[data-app-name="true"]')
            .textContent.replace(/\|\s+/g, '');
        const status = parent.querySelector('[data-app-status="true"]')
            .textContent.replace(/\|\s+/g, '');

        const elem = {
            status: colorizeState(status),
            name: appName
        }

        //4 отправляем в AppList.js
        if (e.target.checked) {
            updateAppList(elem);
        } else {
            deleteAppListItem(elem);
        }
    };

    // 5 обновляем состояние
    const autoUpdateAppList = () => {
        //1 проверяем, есть ли вообще новом списке из api приложение
        const currentAppList = parse(appListKey);
        const _appData_ = appData.map(app => app.metric.__name__);
        const copy = [...currentAppList];

        // если приложение перестает быть объектом мониторинга - удаляем из списка мониторинга
        currentAppList.forEach(app => {
            if(!_appData_.includes(app.name)) {
                const index = copy.indexOf(app.name);
                copy.splice(index, 1);
            }
        });

        //если приложение изменило свое состояние - меняем цвет
        const newAppList = currentAppList.map(app => {
            const value = appData.find(value => value.metric.__name__ === app.name);
            if (value) {
                return {
                    status: colorizeState(value.metric.status),
                    name: value.metric.__name__
                };
            } else {
                return app;
            }
        });
        //
        localStorage[appListKey] = JSON.stringify(newAppList);
    };



    const setDataImmediately = () => {
        setTimeout(getAppData, 0);
        if (parse(appListKey)?.length > 0) {
            autoUpdateAppList();
        }
    };

    useEffect(() => {
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);
    }, [refreshInterval, appData]);

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
                    {appData.map((app, n = 0) => {
                        const key = app + "|" + n;
                        return(
                            <tr key={key}>
                                <td>
                                    <input onClick={e => handleAppMonitoringList(e, n)}
                                           type="checkbox"
                                           defaultChecked={checklistStorage[n]}
                                           disabled={!checklistStorage[n] && checklistStorage.filter(
                                               bool => bool === true
                                           ).length === 6}/>
                                </td>
                                <td data-app-num="true">{n}</td>
                                <td data-app-name="true">| {app.metric.__name__}</td>
                                <td data-app-status="true" style={{
                                    color: `${colorizeState(app.metric.status)}`
                                }}>| {app.metric.status}</td>
                            </tr>
                        );
                    })}
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