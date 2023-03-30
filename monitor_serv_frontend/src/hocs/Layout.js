import React, {Fragment, useEffect} from 'react';
import Header from "../containers/Header";
import {Footer} from "../containers/Footer";
import {checkAuthentication, setAsUser} from "../slices/authSlice";
import {useDispatch} from "react-redux";
import {checkRefreshInterval} from "../slices/refreshIntervalSlice";

const Layout = ({children}) => {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(checkAuthentication());
        dispatch(setAsUser());
        dispatch(checkRefreshInterval());
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