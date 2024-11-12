import { useEffect } from "react";
import { Helmet } from "react-helmet";
import { useTranslation } from "react-i18next";
import { useSelector } from "react-redux";
import { fadeOut } from "../../constants";

const Home = () => {
  const { t } = useTranslation();

  const { isAuthenticated, successMessage } = useSelector(
    (state) => state.auth,
  );

  const alertBlock = (
    <div
      className="mt-4 alert alert-success"
      id="alert"
      role="alert"
      onMouseEnter={fadeOut}
    >
      {successMessage.map((message) => {
        return <span key={message}>{message}</span>;
      })}
    </div>
  );

  useEffect(() => {
    localStorage["currentPage"] = JSON.stringify({ page: "/" });
  }, []);

  return (
    <div className="container">
      <Helmet>
        <title>{t("WELCOME_TITLE")}</title>
        <meta name="description" content={t("WELCOME_DESCRIPTION")} />
      </Helmet>
      <div className="mt-5 p-5 bg-opacity-50">
        <h1 className="display-6">{t("WELCOME_TEXT")}</h1>
        <hr className="my-4" />
        <p className="mt-2">{t("WELCOME_TEXT_DSCR")}</p>
        {!isAuthenticated && (
          <div className="d-flex">
            <a className="btn btn-primary" href="/login">
              {t("UI.LOGIN")}
            </a>
            <a className="ms-2 btn btn-secondary" href="/register">
              {t("UI.REGISTER")}
            </a>
          </div>
        )}
      </div>
      {typeof successMessage.map === "function"
        ? successMessage.length !== 0
          ? alertBlock
          : ""
        : ""}
    </div>
  );
};

export default Home;
