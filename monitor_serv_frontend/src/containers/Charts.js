import React, {useEffect, useRef, useState} from "react";
import SystemCharts from "../components/dashboard/charts/SystemCharts";
import {useDispatch, useSelector} from "react-redux";
import {setAutoupdate, setEndDate, setPeriod, setStartDate} from "../slices/datetimeSlice";

const Charts = () => {
    document.title = "Инфопанель | Графики";

    const dispatch = useDispatch();
    const {startDate, endDate, step} = useSelector(state => state.datetimeManager);
    const [value, setValue] = useState("system");
    const [period, _] = useState("1h");
    const [autoupdate, setAutoUpdate] = useState(false);
    const changePeriodSelectRef = useRef();
    const changePeriodManuallyRefStart = useRef();
    const changePeriodManuallyRefEnd = useRef();

    const setChart = event => setValue(event.target.value);

    const changePeriodManually = e => {
        e.preventDefault();
        const element = e.target;
        const date = new Date(element.value + ":00.000Z");
        date.setMinutes(date.getMinutes() - 180);

        const changeElem = changePeriodSelectRef.current;
        changeElem.value = "custom";

        if (element.id === "inputStartDate") {
            dispatch(setStartDate({value: date.toISOString(), op: "+"}));
        }
        if (element.id === "inputEndDate") {
            dispatch(setEndDate({value: date.toISOString(), op: "+"}));
        }
    };

    const changePeriodSelect = e => {
        e.preventDefault();
        dispatch(setPeriod({period: e.target.value}))
    };

    const changeAutoupdate = e => {
        e.preventDefault();
        setAutoUpdate(prevState => !prevState);
        console.log(autoupdate)
        dispatch(setAutoupdate({autoupdate: autoupdate}));
    }

    useEffect(() => {
        localStorage['currentPage'] = JSON.stringify({page: "/charts"});
    }, [startDate, endDate, step]);

    const popover = chartType => {
        switch (chartType) {
            case "modules": return <div>ModulesCharts</div>
            case "network": return <div>NetworkCharts</div>
            default: return <SystemCharts/>
        }
    };

    return(
        <>
            <div className="container-fluid d-flex mt-3">
                <div className="form-group d-flex flex-row ps-5 align-items-center form-font-size">
                    <label htmlFor="inputStartDate" className="pe-1">Начало:</label>
                    <input defaultValue={startDate.slice(0, -8)}
                           onChange={e => changePeriodManually(e)}
                           type="datetime-local" id="inputStartDate" className="form-control"
                           ref={changePeriodManuallyRefStart}
                    />
                    <label htmlFor="inputEndDate" className="ps-2 pe-1">Конец:</label>
                    <input defaultValue={endDate.slice(0, -8)}
                           onChange={e => changePeriodManually(e)}
                           type="datetime-local" id="inputEndDate" className="form-control"
                           ref={changePeriodManuallyRefEnd}
                    />

                    <label className="ps-2 pe-1" htmlFor="filters">Период:</label>
                    <select defaultValue={period} className="form-select"
                            id="filters"
                            aria-label="filters"
                            onChange={e => changePeriodSelect(e)}
                            ref={changePeriodSelectRef}
                    >
                        <option value="1h">За 1 час</option>
                        <option value="3h">За 3 часа</option>
                        <option value="6h">За 6 часов</option>
                        <option value="12h">За 12 часов</option>
                        <option value="1d">За день</option>
                        <option value="1w">За неделю</option>
                        <option value="1m">За месяц</option>
                        <option value="custom">Вручную</option>
                    </select>
                </div>

                <div className="form-font-size d-flex flex-row align-items-center ps-3">
                    <label htmlFor="autoupdate">Автообновление:</label>
                    <input id="autoupdate" className="ms-1" type="checkbox"
                        defaultChecked={autoupdate}
                           onClick={e => changeAutoupdate(e)}
                    />
                </div>

                <div onChange={setChart.bind(this)} className="btn-group ps-3"
                     role="group" aria-label="charts">
                    <input type="radio" className="btn-check" name="system" id="system" autoComplete="off"
                           value="system" checked={"system" === value} readOnly={true}/>
                    <label className="btn btn-outline-primary" htmlFor="system">System</label>
                    <input type="radio" className="btn-check" name="network" id="network" autoComplete="off"
                           value="network" checked={"network" === value} readOnly={true}/>
                    <label className="btn btn-outline-primary" htmlFor="network">Network</label>
                    <input type="radio" className="btn-check" name="modules" id="modules" autoComplete="off"
                           value="modules" checked={"modules" === value} readOnly={true}/>
                    <label className="btn btn-outline-primary" htmlFor="modules">Modules</label>
                </div>
            </div>
            {popover(value)}
        </>
  );
};

export default Charts;