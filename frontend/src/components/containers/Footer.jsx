import { useCallback, useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router-dom";
import { APP_VERSION } from "../../constants";
import StatusBar from "./StatusBar";

const Footer = () => {
  const { t } = useTranslation();
  const { pathname } = useLocation();
  const [alertPanel, setAlertPanel] = useState(false);

  const statusBar = useCallback(() => {
    // main
    if (
      pathname === "/" ||
      pathname.includes("login") ||
      pathname.includes("register")
    ) {
      setAlertPanel(false);
    } else {
      setAlertPanel(true);
    }
  }, [pathname]);

  useEffect(() => {
    const interval = setInterval(statusBar, 500);
    return () => clearInterval(interval);
  }, [statusBar]);

  return (
    <footer className="footer mt-auto py-4 bg-dark">
      {alertPanel && <StatusBar />}
      <div className="bg-dark">
        <Container className="text-center text-light">{t("FOOTER")}</Container>
        <Container className="text-center text-light">{APP_VERSION}</Container>
      </div>
    </footer>
  );
}

export default Footer;
