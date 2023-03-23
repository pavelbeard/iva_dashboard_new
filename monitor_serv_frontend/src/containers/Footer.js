import React from 'react';
import {Container} from "react-bootstrap";
import {APP_VERSION} from "../base";

export function Footer() {
    const APP_VERSION_LOCAL = window._env_.REACT_APP_VERSION || APP_VERSION

    return(
        <footer className="footer py-2 bg-dark mt-auto">
            <Container className="text-center text-light">created by pavel borodin</Container>
            <Container className="text-center text-light">{APP_VERSION_LOCAL}</Container>
        </footer>
    )
}