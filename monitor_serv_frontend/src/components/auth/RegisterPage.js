import './FormPage.css';
import {useEffect, useState} from "react";
import {API_URL, postData} from "../../base";

export function RegisterPage() {
    document.title = "Инфопанель | Регистрация";

    const [username, setUsername] = useState();
    const [firstName, setFirstName] = useState();
    const [lastName, setLastName] = useState();
    const [email, setEmail] = useState();
    const [password1, setPassword1] = useState();
    const [password2, setPassword2] = useState();

    const handleData = async () => {
        const urlRequest = `${API_URL}/api/users/register`;
        const body = {
            username: username,
            firstName: firstName,
            lastName: lastName,
            email: email,
            password1: password1,
            password2: password2,
        }

        const response = await postData(urlRequest, body);

    }

    // useEffect(() => {
    //     setTimeout(handleData, 0);
    // }, [username])

    const handleChange = e => {
        const {id, value} = e.target;

        if (id === "username") {
            setUsername(value);
        }
        if (id === "firstName") {
            setFirstName(value);
        }
        
    }

    return(
        <div className="d-flex flex-column align-items-center mt-4" id="formContainer">
            <h3>Регистрация</h3>
            <form onSubmit={handleChange} className="w-100">
                <div className="form-group">
                    <label htmlFor="username">Имя пользователя:</label>
                    <input type="text" id="username" value={username} className="form-control"/>
                    <small id="usernameHelp" onChange={handleChange.bind(this)} className="form-text text-muted">
                        Имя пользователя должно быть написано английскими буквами. Допускаются цифры и символы: [@_]
                    </small>
                </div>
                <div className="form-group">
                    <label htmlFor="firstName">Имя:</label>
                    <input type="text" id="firstName" value={firstName} onChange={handleChange.bind(this)} className="form-control"/>
                </div>
                <div className="form-group">
                    <label htmlFor="lastName">Фамилия:</label>
                    <input type="text" id="lastName" value={lastName} onChange={handleChange.bind(this)} className="form-control"/>
                </div>
                <div className="form-group">
                    <label htmlFor="email">E-mail:</label>
                    <input type="email" id="email" value={email} onChange={handleChange.bind(this)} className="form-control"/>
                </div>
                <div className="form-group">
                    <label htmlFor="password1">Пароль:</label>
                    <input type="password" id="password1" value={password1} onChange={handleChange.bind(this)}  className="form-control"/>
                    <small id="passwordHelp" className="form-text text-muted">
                        Пароль должен состоять из символов, больших букв, цифр.
                    </small>
                </div>
                <div className="form-group">
                    <label htmlFor="password2">Подтверждение:</label>
                    <input type="password" id="password2" value={password2} onChange={handleChange.bind(this)} className="form-control"/>

                    <button type="submit" className="btn btn-primary mt-2">
                        Зарегистрироваться
                    </button>
                </div>
            </form>
        </div>
    )
}