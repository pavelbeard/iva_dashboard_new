import React, {useState} from "react";
import SystemCharts from "../serverDetail/SystemCharts";

function Charts() {
    const [value, setValue] = useState("system");
    const [filterValue, setFilterValue] = useState("interval.last.hour")
    const [charts, setCharts] = useState({
        system: <SystemCharts filter={filterValue}/>
    })

    const setChart = event => setValue(event.target.value);

    // const setFilter = event => setFilterValue(event.target.value)

    return(
      <div className="container-fluid d-flex mt-3">
          <div className="form-group d-flex flex-row ps-5 align-items-center">
              <label htmlFor="inputDate" className="pe-1">Начало:</label>
              <input style={{width: "230px"}} type="datetime-local" id="inputDateStart" className="form-control"/>
              <label htmlFor="inputDate" className="ps-2 pe-1">Конец:</label>
              <input style={{width: "230px"}} type="datetime-local" id="inputDateEnd" className="form-control"/>
          </div>

          <select defaultValue="3h" className="form-select" style={{width: "150px"}} aria-label="filters">
              <option value="1h">За 1 час</option>
              <option value="3h">За 3 часа</option>
              <option value="6h">За 6 часов</option>
              <option value="12h">За 12 часов</option>
              <option value="1d">За день</option>
              <option value="1w">За неделю</option>
              <option value="1m">За месяц</option>
              <option value="custom">Вручную</option>
          </select>

          <div onChange={setChart.bind(this)} className="btn-group ps-5"
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
  )
}

export default Charts;