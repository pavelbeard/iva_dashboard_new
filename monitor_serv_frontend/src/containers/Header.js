import React, {useState} from "react";
import {Link, NavLink} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {logoutAsync} from "../slices/authSlice";
import {changeRefreshInterval} from "../slices/refreshIntervalSlice";
import {API_URL} from "../base";
import LoggedAs from "../components/auth/LoggedAs";

import './Containers.css'

const Header = () => {
    const dispatch = useDispatch();
    const isAuthenticated = useSelector(state => state.auth.isAuthenticated);
    const defaultRefreshInterval = useSelector(state => state.refresh.refreshInterval);

    const logout = () => dispatch(logoutAsync());

    const authLinks = (
        <>
            <NavLink to="/" className="nav-item nav-link">Главная</NavLink>
            <NavLink to="/dashboard" className="nav-item nav-link">Инфопанель</NavLink>
            <NavLink to="/charts" className="nav-item nav-link">Графики</NavLink>
            <a href={`${API_URL}/admin`} className="nav-item nav-link">
                Админ
            </a>
        </>
    );

    const guestLinks = (
        <>
            <NavLink to="/login" className="nav-item nav-link">Войти</NavLink>
            <NavLink to="/register" className="nav-item nav-link">Регистрация</NavLink>
        </>
    );

    const setRefreshInterval = e => {
        dispatch(changeRefreshInterval(e.target.value));
    };

    const refreshIntervalControls = (
        <>
            <label htmlFor="selectRefreshInterval" style={{width: "230px"}}
                   className="text-white nav-item nav-link">
                Интервал обновления:
            </label>
            <select id="selectRefreshInterval"
                    defaultValue={defaultRefreshInterval}
                    onChange={e => setRefreshInterval(e)}
                    className="form-select">
                <option value="5000">5 секунд</option>
                <option value="10000">10 секунд</option>
                <option value="15000">15 секунд</option>
                <option value="30000">30 секунд</option>
            </select>
        </>
    );

    const [isNavCollapsed, setIsNavCollapsed] = useState(true);

    const navbarCollapsed = () => setIsNavCollapsed(!isNavCollapsed);

    return(
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container">
                <Link to="/" className="navbar-brand">IVA MCU Инфопанель</Link>
                <button className="navbar-toggler"
                        type="button"
                        data-toggle="collapse"
                        data-target="#dashboardContent"
                        aria-controls="dashboardContent"
                        aria-expanded={isNavCollapsed}
                        aria-label="Toggle navigation" onClick={navbarCollapsed}>
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className={`${isNavCollapsed ? 'collapse' : ''}  navbar-collapse`} id="dashboardContent">
                    <div className="navbar-nav">
                        {isAuthenticated ? authLinks : guestLinks}
                    </div>
                    {isNavCollapsed && isAuthenticated ?
                        <div className="d-flex">
                            <div className="vr bg-white"></div>
                        </div> :
                        "" }
                    <div className="navbar-nav me-lg-2">
                        {isAuthenticated ? refreshIntervalControls : <></>}
                    </div>
                    {isNavCollapsed && isAuthenticated ?
                        <div className="d-flex me-lg-2">
                            <div className="vr bg-white"></div>
                        </div> :
                        "" }
                    <div className="navbar-nav me-lg-2">
                        {isAuthenticated ? <LoggedAs/> : <></>}
                    </div>
                    {isNavCollapsed && isAuthenticated ?
                        <div className="d-flex">
                            <div className="vr bg-white"></div>
                        </div> :
                        "" }
                    <div className="navbar-nav">
                        {isAuthenticated ?
                            <a onClick={logout} href="#!" className="nav-item nav-link">Выйти</a>
                            : ""}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Header;