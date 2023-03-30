import React, {useEffect} from "react";
import {useSelector} from "react-redux";
import {fadeOut} from "../base";


const Home = () => {
    document.title = "Инфопанель | Добро пожаловать в Инфопанель IVA MCU";

    const {isAuthenticated, successMessage} = useSelector(state => state.auth);

    const alertBlock = (
        <div className="mt-4 alert alert-success" id="alert" role="alert" onMouseEnter={fadeOut}>
            {successMessage.map(message => {
                return(<span key={message}>{message}</span>)
            })}
        </div>
    );

    return (
        <div className="container">
            <div className="mt-5 p-5 bg-danger bg-opacity-10">
                <h1 className="display-6">Добро пожаловать в Инфопанель IVA MCU</h1>
                <hr className='my-4'/>
                <p className="mt-2">Мониторинг медиа- и головных серверов системы ВКС IVA</p>
                {!isAuthenticated ? <div className="d-flex">
                    <a className="btn btn-primary" href="/login">Войти</a>
                    <a className="ms-2 btn btn-secondary" href="/register">Регистрация</a>
                </div> : ""}
            </div>
            {typeof successMessage.map === "function" ?
                successMessage.length !== 0 ? alertBlock : "" : ""}
        </div>
    );
};

export default Home;