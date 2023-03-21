import React, {useEffect, useState} from "react";
import './Header.css';
// import Charts from "./dashboard/Charts";

export function Header() {
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
                    <div className="navbar-nav">
                        <a href="/targets" className="nav-item nav-link">Инфопанель</a>
                        <a href="/targets/detail" className="nav-item nav-link">Детализация</a>
                    </div>
                </div>

            </div>
        </nav>
    )
}