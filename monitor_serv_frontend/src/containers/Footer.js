import React, {useEffect, useState} from 'react';
import {Container} from "react-bootstrap";
import {API_URL, APP_VERSION} from "../base";
import StatusBar from "./StatusBar";

export function Footer() {
    const [alertPanel, setAlertPanel] = useState("");

    const statusBar = () => {
        // main
        if (document.location.href === document.location.origin + "/") {
            setAlertPanel("");
        } else if (document.location.href.includes('login')) {
            setAlertPanel("");
        } else if (document.location.href.includes('register')) {
            setAlertPanel("")
        } else {
            setAlertPanel(<StatusBar />);
        }
    };

    useEffect(() => {
        const interval = setInterval(statusBar, 500);
        return () => clearInterval(interval);
    }, [])


    return(
        <footer className="footer mt-auto bg-dark">
            {alertPanel}
            <div className="bg-dark">
                <Container className="text-center text-light">created by pavel borodin</Container>
                <Container className="text-center text-light">{APP_VERSION}</Container>
            </div>
        </footer>
    );
}