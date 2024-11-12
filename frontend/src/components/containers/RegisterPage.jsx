import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Navigate } from "react-router-dom";
import CSRFToken from "../auth/CSRFToken";
import { parse } from "../../constants";
import { registerAsync } from "../../slices/authSlice";

const RegisterPage = () => {
  document.title = "Инфопанель | Регистрация";

  const { isRegister, registerErrors, isAuthenticated } = useSelector(
    (state) => state.auth,
  );
  const dispatch = useDispatch();

  const [formData, setFormData] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    password2: "",
  });
  const [messages, setMessages] = useState([]);
  const { username, first_name, last_name, email, password, password2 } =
    formData;

  const onChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = (e) => {
    e.preventDefault();
    dispatch(
      registerAsync({
        username,
        first_name,
        last_name,
        email,
        password,
        password2,
      }),
    );
  };

  const alertBlock = (
    <div className="alert alert-danger mt-4" role="alert">
      {messages.map((message) => {
        return <span key={message}>{message}</span>;
      })}
    </div>
  );

  useEffect(() => {
    localStorage["currentPage"] = JSON.stringify({ page: "/register" });
    setMessages(registerErrors);
  }, [registerErrors, isRegister]);

  if (isRegister) {
    return <Navigate to="/" />;
  } else if (isAuthenticated) {
    let page = parse("currentPage").page;
    if (page === "/register") {
      page = "/dashboard";
    }
    return <Navigate to={page} />;
  }

  return (
    <div className="container mt-3">
      <h1 className="display-6">Регистрация</h1>
      <hr className="my-1" />
      <form onSubmit={(e) => onSubmit(e)}>
        <CSRFToken />
        <div className="d-flex flex-row">
          <div className="form-group w-50">
            <label htmlFor="username" className="form-label">
              Имя пользователя:
            </label>
            <input
              type="text"
              className="form-control"
              placeholder="Имя пользователя"
              id="username"
              name="username"
              onChange={(e) => onChange(e)}
              value={username}
              required
            />
          </div>
          <div className="form-group ms-3 w-50">
            <label htmlFor="email" className="form-label">
              E-mail:
            </label>
            <input
              type="email"
              className="form-control"
              placeholder="E-mail"
              id="email"
              name="email"
              onChange={(e) => onChange(e)}
              value={email}
              required
            />
          </div>
        </div>
        <div className="d-flex flex-row">
          <div className="form-group w-50">
            <label htmlFor="first_name" className="form-label">
              Имя:
            </label>
            <input
              type="text"
              className="form-control"
              placeholder="Имя"
              id="first_name"
              name="first_name"
              onChange={(e) => onChange(e)}
              value={first_name}
              required
            />
          </div>
          <div className="form-group ms-3 w-50">
            <label htmlFor="last_name" className="form-label">
              Фамилия:
            </label>
            <input
              type="text"
              className="form-control"
              placeholder="Фамилия"
              id="last_name"
              name="last_name"
              onChange={(e) => onChange(e)}
              value={last_name}
              required
            />
          </div>
        </div>
        <div className="d-flex flex-row">
          <div className="form-group w-50">
            <label htmlFor="password" className="form-label">
              Пароль:
            </label>
            <input
              type="password"
              className="form-control"
              placeholder="Пароль"
              id="password"
              name="password"
              onChange={(e) => onChange(e)}
              value={password}
              required
            />
          </div>
          <div className="form-group ms-3 w-50">
            <label htmlFor="password2" className="form-label">
              Подтверждение:
            </label>
            <input
              type="password"
              className="form-control"
              placeholder="Подтверждение"
              id="password2"
              name="password2"
              onChange={(e) => onChange(e)}
              value={password2}
              required
            />
          </div>
        </div>
        <button
          className="mt-2 btn btn-primary"
          type="submit"
          onSubmit={onSubmit}
        >
          Зарегистрироваться
        </button>
        {messages.length !== 0 ? alertBlock : ""}
      </form>
    </div>
  );
};

export default RegisterPage;
