import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Navigate } from "react-router-dom";
import { parse } from "../../constants";
import CSRFToken from "../auth/CSRFToken";
import { loginAsync } from "../../slices/authSlice";
import "./Containers.css";

const LoginPage = () => {
  document.title = "Инфопанель | Вход в систему";

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [messages, setMessages] = useState([]);
  const { isAuthenticated, successMessage, loginErrors, errorMessage } =
    useSelector((state) => state.auth);
  const dispatch = useDispatch();

  const { username, password } = formData;

  const onChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = (e) => {
    e.preventDefault();

    dispatch(loginAsync({ username, password }));
  };

  const alertBlock = (
    <div
      className={`mt-4 alert-hidden
             alert alert-${successMessage.length !== 0 ? "success" : "danger"}`}
      role="alert"
    >
      {typeof messages.map === "function"
        ? messages.map((message) => {
            return <span key={message}>{message}</span>;
          })
        : ""}
    </div>
  );

  useEffect(() => {
    localStorage["currentPage"] = JSON.stringify({ page: "/login" });

    if (successMessage.length !== 0) {
      setMessages(successMessage);
    } else if (errorMessage === "") {
      setMessages(loginErrors);
    } else {
      setMessages([errorMessage]);
    }
  }, [loginErrors, errorMessage]);

  if (isAuthenticated) {
    let page = parse("currentPage").page;
    if (page === "/login") {
      page = "/dashboard";
    }

    return <Navigate to={page} />;
  }

  return (
    <div className="container mt-3">
      <h1 className="display-6">Вход в систему</h1>
      <hr className="my-1" />
      <form onSubmit={(e) => onSubmit(e)}>
        <CSRFToken />
        <div className="form-group">
          <label htmlFor="username" className="form-label">
            Имя пользователя:
          </label>
          <input
            type="text"
            id="username"
            name="username"
            onChange={(e) => onChange(e)}
            value={username}
            className="form-control"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password" className="form-label">
            Пароль:
          </label>
          <input
            type="password"
            id="password"
            name="password"
            onChange={(e) => onChange(e)}
            value={password}
            className="form-control"
            required
          />
        </div>
        <button type="submit" className="btn btn-primary mt-2">
          Войти
        </button>
        {messages.length !== 0 ? alertBlock : ""}
      </form>
    </div>
  );
};

export default LoginPage;
