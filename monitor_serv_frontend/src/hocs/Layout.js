import React, {Fragment} from 'react';
import Header from "../containers/Header";
import {Footer} from "../containers/Footer";


const Layout = ({children}) => (
    <>
        <Fragment>
            <Header />
            {children}
            <Footer />
        </Fragment>
    </>
);

export default Layout