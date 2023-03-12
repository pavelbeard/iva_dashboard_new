import React, {useEffect} from "react";
import {createRoot} from "react-dom/client";
import Dashboard from "./dashboard/Dashboard";


const App = () => {
    useEffect(() => {
        document.title = "Инфопанель";
    })

    return(<Dashboard/>);
};


export default App;

const appContainer = document.getElementById('dashboardRoot');
const root = createRoot(appContainer);
root.render(<App/>);
