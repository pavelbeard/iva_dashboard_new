import React from "react";
import {Link} from "react-router-dom";

const Home = () => (
    <div className="container">
        <div className="mt-5 p-5 bg-danger bg-opacity-10">
            <h1 className="display-6">Добро пожаловать в Инфопанель IVA MCU</h1>
            <hr className='my-4' />
            <p className="mt-2">Мониторинг медиа- и головных серверов системы ВКС IVA</p>
            <div className="d-flex">
                <a className="btn btn-primary" href="/login">Войти</a>
                <a className="ms-2 btn btn-secondary" href="/register">Регистрация</a>
            </div>
        </div>

    </div>
);

export default Home;