import {useState} from "react";
import {API_URL, getData, getResponse, postData} from "../base";
import axios from "axios";

const LoginPage = () => {
    document.title = "Инфопанель | Вход в систему";

    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const [csrf, setCsrf] = useState();

    const submitForm = async e => {
        e.preventDefault();

        const csrfUrlRequest = `${API_URL}/api/v1/csrf_cookie`;
        const csrfCookie = await axios.get(csrfUrlRequest)
            .then(response => {return response.headers});
        setCsrf(csrfCookie);
    };

    const handleChange = e => {
        const {id, value} = e.target;

        if (id === 'username') {
            setUsername(value);
        }
        if (id === 'password') {
            setPassword(password);
        }
    }


    return(
        <div className="container mt-3">
            <h1 className="display-6">Вход в систему</h1>
            <hr className="my-1" />
            <form onSubmit={submitForm}>
                <div className="form-group">
                    <label htmlFor="username">Имя пользователя:</label>
                    <input type="text" id="username"
                           value={username}
                           onChange={handleChange} className="form-control"/>
                </div>
                <div className="form-group">
                    <label htmlFor="password2">Пароль:</label>
                    <input type="password" id="password2"
                           value={password}
                           onChange={handleChange} className="form-control"/>

                    <button type="submit" className="btn btn-primary mt-2">
                        Войти
                    </button>
                </div>
            </form>
        </div>
    )
};

export default LoginPage;