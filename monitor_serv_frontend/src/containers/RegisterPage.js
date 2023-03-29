import React, {useEffect, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {Navigate} from "react-router-dom";
import CSRFToken from "../components/auth/CSRFToken";
import {registerAsync} from "../slices/authSlice";

const RegisterPage = () => {
    document.title = "Инфопанель | Регистрация";

    const {isAuthenticated, isRegister, registerErrors} = useSelector(state => state.auth);
    const dispatch = useDispatch();

    const [formData, setFormData] = useState({
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        password2: '',
    });
    const [messages, setMessages] = useState([]);
    const {username, first_name, last_name, email, password, password2} = formData;

    const onChange = e => setFormData({...formData, [e.target.name]: e.target.value});

    const onSubmit = e => {
        e.preventDefault();
        dispatch(registerAsync({username, first_name, last_name, email, password, password2}));
    }

    useEffect(() => {
        setMessages(registerErrors)
    }, [registerErrors, isRegister])

    if (isRegister) {
        return <Navigate to="/" />
    }
    else if (isAuthenticated) {
        return <Navigate to="/dashboard" />
    }

    return (
        <div className="container mt-3">
            <h1 className="display-6">Регистрация</h1>
            <hr className="my-1"/>
            <form onSubmit={e => onSubmit(e)}>
                <CSRFToken />
                <div className="d-flex flex-row">
                    <div className="form-group w-50">
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
                    <div className="form-group ms-3 w-50">
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
                </div>
                <div className="d-flex flex-row">
                    <div className="form-group w-50">
                        <label htmlFor="" className="form-label">Имя:</label>
                        <input type="text"
                               className="form-control"
                               placeholder="Имя"
                               name="first_name"
                               onChange={e => onChange(e)}
                               value={first_name}
                               required
                        />
                    </div>
                    <div className="form-group ms-3 w-50">
                        <label htmlFor="" className="form-label">Фамилия:</label>
                        <input type="text"
                               className="form-control"
                               placeholder="Фамилия"
                               name="last_name"
                               onChange={e => onChange(e)}
                               value={last_name}
                               required
                        />
                    </div>
                </div>
                <div className="d-flex flex-row">
                    <div className="form-group w-50">
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
                    <div className="form-group ms-3 w-50">
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
                </div>
                <button className="mt-2 btn btn-primary"
                        type="submit"
                        onSubmit={onSubmit}>Зарегистрироваться
                </button>
                <div className="form-group mt-4">
                    <ul className="list-group-item-danger rounded">
                        {/*{messages.map(message => {*/}
                        {/*    return (*/}
                        {/*        <li>message</li>*/}
                        {/*    );*/}
                        {/*})}*/}
                        {messages ? messages.map(message => {
                            return(<li>{message}</li>)
                        })

                        : ""}
                    </ul>
                </div>
            </form>
        </div>
    );
};

export default RegisterPage;