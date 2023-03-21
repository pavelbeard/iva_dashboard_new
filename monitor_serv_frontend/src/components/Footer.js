import React from 'react';
import {Container} from "react-bootstrap";

export function Footer() {
    return(
        <footer className="footer py-2 bg-dark mt-auto">
            <Container className="text-center text-light">created by pavel borodin</Container>
            <Container className="text-center text-light">v{process.env.REACT_APP_VERSION}</Container>
        </footer>
    )
}