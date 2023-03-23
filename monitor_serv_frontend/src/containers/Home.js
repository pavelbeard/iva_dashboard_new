import React from "react";
import {Link} from "react-router-dom";

const Home = () => (
    <div className="container">
        <div className="mt-5 p-5 bg-light">
            <h1 className="display-4">Добро пожаловать в Инфопанель IVA VIP</h1>
        </div>
        <p className='lead'>
            This is a wonderful application with session authentication in React and Django.
        </p>
        <hr className='my-4' />
        <p>Нажмите ссылку ниже, чтобы войти в Инфопанель.</p>
        <Link className='btn btn-primary btn-lg' to='/login'>Login</Link>
    </div>
);

export default Home;