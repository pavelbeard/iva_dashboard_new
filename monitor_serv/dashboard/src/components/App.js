import React, {useEffect} from "react";
import {createRoot} from "react-dom/client";
import Dashboard from "./dashboard/Dashboard";
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Charts from "./dashboard/Charts";


const App = () => {
    useEffect(() => {
        document.title = "Инфопанель";
    })

    return(
        <Router>
            <Routes>
                <Route path='/targets' element={<Dashboard/>}/>
                <Route path='/targets/detail' element={<Charts/>}/>
            </Routes>
        </Router>
    );
};


export default App;

const appContainer = document.getElementById('dashboardRoot');
const root = createRoot(appContainer);
root.render(<App/>);
