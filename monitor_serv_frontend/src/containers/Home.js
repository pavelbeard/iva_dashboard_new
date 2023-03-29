import React from "react";
import {Link} from "react-router-dom";
import {useSelector} from "react-redux";

const Home = () => {
    document.title = "Инфопанель | Добро пожаловать в Инфопанель IVA MCU";

    const successMessage = useSelector(state => state.auth.successMessage);

    const alertBlock = (
        <div className="mt-4 alert alert-success" role="alert">
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
                <div className="d-flex">
                    <a className="btn btn-primary" href="/login">Войти</a>
                    <a className="ms-2 btn btn-secondary" href="/register">Регистрация</a>
                </div>
            </div>
            {successMessage.length !== 0 ? alertBlock : ""}
        </div>
    );
};

export default Home;