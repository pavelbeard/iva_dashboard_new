import React, {useEffect, useState} from "react";
import './Header.css';
// import Charts from "./dashboard/Charts";

export function Header({refreshIntervalCallback}) {
    const authLinks = (
        <>
            <a href="/logout" className="nav-item nav-link">Выйти</a>
            <a href="/targets" className="nav-item nav-link">Инфопанель</a>
            <a href="/targets/charts" className="nav-item nav-link">Графики</a>
            <a href="/admin" className="nav-item nav-link">Панель админа</a>
        </>
    );

    const guestLinks = (
        <>
            <a href="/login" className="nav-item nav-link">Войти</a>
            <a href="/register" className="nav-item nav-link">Регистрация</a>
        </>
    );

    const [isNavCollapsed, setIsNavCollapsed] = useState(true);

    const navbarCollapsed = () => setIsNavCollapsed(!isNavCollapsed);

    useEffect(() => {
        const interval = setInterval(() => {
            const elems = document.querySelectorAll('a.nav-item.nav-link');
            const path = "/" + (document.URL.split('/')).slice(3).join("/");

            for (let i = 0; i < elems.length; i++) {
                let defaultColor = "#d2d1d1";
                if (elems[i].getAttribute('href') === path) {
                    elems[i].style.color = "#fff";
                }
                else {
                    elems[i].style.color = defaultColor;
                }
            }
        }, 100);
        return () => clearInterval(interval);
    }, []);

    return(
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container ms-0">
                <a href="/" className="navbar-brand">IVA MCU Инфопанель</a>
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
                        {/*{iaAuthenticated ? authLinks : guestLinks}*/}
                        {authLinks}
                    </div>
                    <div className="d-flex flex-row align-items-center">
                        <label htmlFor="selectRefreshInterval" className="text-white">Интервал обновления:</label>
                        <select id="selectRefreshInterval"
                                onChange={refreshIntervalCallback.bind(this)}
                                className="form-select form-select-sm ms-2">
                            <option value="5000">5 секунд</option>
                            <option value="10000">10 секунд</option>
                            <option value="15000">15 секунд</option>
                            <option value="30000">30 секунд</option>
                        </select>
                    </div>
                </div>
            </div>
        </nav>
    )
}