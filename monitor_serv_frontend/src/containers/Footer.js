import React from 'react';
import {Container} from "react-bootstrap";
import {APP_VERSION} from "../base";
import StatusBar from "./StatusBar";

export function Footer() {
    return(
        <footer className="footer mt-auto bg-dark">
            <StatusBar/>
            <div className="bg-dark">
                <Container className="text-center text-light">created by pavel borodin</Container>
                <Container className="text-center text-light">{APP_VERSION}</Container>
            </div>
        </footer>
    );
}