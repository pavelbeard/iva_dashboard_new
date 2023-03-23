import {useState} from "react";
import './FormPage.css';
import {API_URL, getData, getResponse, postData} from "../../base";

export function LoginPage() {
    document.title = "Инфопанель | Вход в систему";

    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const [csrf, setCsrf] = useState();

    const csrfCookieSetter = async () => {
        const urlRequest = `${API_URL}/api/v1/csrf_cookie`;
        const response = await getResponse(urlRequest);

        if (response) {
            setCsrf(response.headers['csrf'])
        }
    }

    const login = async () => {
        await csrfCookieSetter();

        const body = {
            username: username,
            password: password,
            csrf: csrf
        };
        const urlRequest = `${API_URL}/api/users/login`;
        const response = await postData(urlRequest, body);
        console.log(response)
    }

    const handleChange = e => {
        const {id, value} = e.target;

        if (id === "username") {
            setUsername(value);
        }
        if (id === "password") {
            setPassword(value);
        }

        setTimeout(login, 0);
    }


    return(
        <div className="d-flex flex-column align-items-center h-100 mt-4" id="formContainer">
            <h3>Вход в систему</h3>
            <form onSubmit={handleChange} className="w-100">
                <div className="form-group">
                    <label htmlFor="username">Имя пользователя:</label>
                    <input type="text" id="username" value={username} className="form-control"/>
                </div>
                <div className="form-group">
                    <label htmlFor="password2">Пароль:</label>
                    <input type="password" id="password2" value={password} onChange={handleChange.bind(this)} className="form-control"/>

                    <button type="submit" className="btn btn-primary mt-2">
                        Войти
                    </button>
                </div>
            </form>
        </div>
    )
}