import React, {useEffect, useState} from "react";
import {Link, NavLink} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {logoutAsync} from "../slices/authSlice";
const Header = () => {
    const {isAuthenticated} = useSelector(state => state.auth);
    const dispatch = useDispatch();

    const logout = () => dispatch(logoutAsync());

    const authLinks = (
        <>
            <NavLink to="/" className="nav-item nav-link">Главная</NavLink>
            <NavLink to="/dashboard" className="nav-item nav-link">Инфопанель</NavLink>
            <NavLink to="/charts" className="nav-item nav-link">Графики</NavLink>
            <NavLink to="/admin" className="nav-item nav-link">Админ-панель</NavLink>
            <a onClick={logout} href="#!" className="nav-item nav-link">Выйти</a>
        </>
    );

    const guestLinks = (
        <>
            <NavLink to="/login" className="nav-item nav-link">Войти</NavLink>
            <NavLink to="/register" className="nav-item nav-link">Регистрация</NavLink>
        </>
    );

    const refreshIntervalControls = (
        <>
            <label htmlFor="selectRefreshInterval" style={{width: "230px"}} className="text-white">Интервал обновления:</label>
            <select id="selectRefreshInterval"
                    // onChange={refreshIntervalCallback.bind(this)}
                    className="form-select form-select-sm ms-2">
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
            <div className="container ms-0">
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
                    <div className="navbar-nav me-lg-4">
                        {isAuthenticated ? authLinks : guestLinks}
                    </div>
                    <div className="d-flex flex-row align-items-center">
                        {isAuthenticated ? refreshIntervalControls : <></>}
                    </div>
                </div>
            </div>
        </nav>
    )
};

export default Header;