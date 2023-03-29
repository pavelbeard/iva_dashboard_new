import React, {Fragment, useEffect} from 'react';
import Header from "../containers/Header";
import {Footer} from "../containers/Footer";
import {checkAuthenticationAsync} from "../slices/authSlice";
import {useDispatch} from "react-redux";

const Layout = ({children}) => {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(checkAuthenticationAsync());
    }, [])

    return (
        <Fragment>
            <Header/>
            {children}
            <Footer/>
        </Fragment>
    );
};

export default Layout;