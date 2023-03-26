import React, {useState} from "react";
import {connect} from "react-redux";
import {Navigate} from "react-router-dom";

import {register} from "../actions/auth";
import CSRFToken from "../components/auth/CSRFToken";

const RegisterPage = ({register}) => {
    const [formData, setFormData] = useState({
        username: '',
        firstname: '',
        lastname: '',
        email: '',
        password: '',
        password2: '',
    });
    const [userCreated, setUserCreated] = useState();

    const {username, firstname, lastname, email, password, password2} = formData;

    const onChange = e => setFormData({...formData, [e.target.name]: e.target.value});

    const onSubmit = e => {
        e.preventDefault();

        register(username, firstname, lastname, email, password, password2);
        setUserCreated(true);

    }

    if (userCreated) {
        return <Navigate to="/"/>
    }

    return (
        <div className="container mt-3">
            <h1 className="display-6">Регистрация</h1>
            <hr className="my-1"/>
            <form onSubmit={e => onSubmit(e)}>
                <CSRFToken />
                <div className="form-group">
                    <label htmlFor="" className="form-label">Имя пользователя:</label>
                    <input type="text"
                           className="form-control"
                           placeholder="Имя пользователя"
                           name="username"
                           onChange={e => onChange(e)}
                           value={username}
                           required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="" className="form-label">Имя:</label>
                    <input type="text"
                           className="form-control"
                           placeholder="Имя"
                           name="firstname"
                           onChange={e => onChange(e)}
                           value={firstname}
                           required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="" className="form-label">Фамилия:</label>
                    <input type="text"
                           className="form-control"
                           placeholder="Фамилия"
                           name="lastname"
                           onChange={e => onChange(e)}
                           value={lastname}
                           required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="" className="form-label">E-mail:</label>
                    <input type="email"
                           className="form-control"
                           placeholder="E-mail"
                           name="email"
                           onChange={e => onChange(e)}
                           value={email}
                           required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="" className="form-label">Пароль:</label>
                    <input type="password"
                           className="form-control"
                           placeholder="Пароль"
                           name="password"
                           onChange={e => onChange(e)}
                           value={password}
                           required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="" className="form-label">Подтверждение:</label>
                    <input type="password"
                           className="form-control"
                           placeholder="Подтверждение"
                           name="password2"
                           onChange={e => onChange(e)}
                           value={password2}
                           required
                    />
                </div>

                <button className="mt-2 btn btn-primary"
                        type="submit"
                        onSubmit={onSubmit}>Зарегистрироваться
                </button>
            </form>
        </div>
    );
};

export default connect(null, {register})(RegisterPage);