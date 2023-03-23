import {Header} from "./containers/Header";
import 'bootstrap/dist/css/bootstrap.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import Dashboard from "./containers/Dashboard";
import Charts from "./components/dashboard/Charts";
import {Footer} from "./containers/Footer";
import {RegisterPage} from "./components/auth/RegisterPage";
import {LoginPage} from "./components/auth/LoginPage";
import {useEffect, useState} from "react";
import Home from "./containers/Home";

function App() {
    const [refreshInterval, setRefreshInterval] = useState(5000);

    const authComponents = (
        <>
            <Route path="/targets" element={<Dashboard appRefreshInterval={refreshInterval}/>}/>
            <Route path="/targets/charts" element={<Charts/>}/>
        </>
    );

    const guestComponents = (
        <>
            <Route path="/" element={<Home/>}></Route>
            <Route path="/register" element={<RegisterPage/>}/>
            <Route path="/login" element={<LoginPage/>}/>
        </>
    );

    const refreshIntervalCallback = e => {
        setRefreshInterval(e.target.value);
    }

    useEffect(() => {

    }, [refreshInterval])

    return (
        <Router>
            <Header refreshIntervalCallback={refreshIntervalCallback}/>
                <Routes>
                    {guestComponents}
                    {authComponents}
                </Routes>
            <Footer/>
        </Router>
    );
}

export default App;
