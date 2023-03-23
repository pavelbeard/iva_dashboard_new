import {Fragment, useEffect} from "react";
import {Header} from "../containers/Header";
import {Footer} from "../containers/Footer";
import {connect} from "react-redux";

const Layout = ({children, checkAuth, loadUser}) => {
    useEffect(() => {
        checkAuth();
        loadUser();
    });

    return(
        <Fragment>
            <Header />
            {children}
            <Footer />
        </Fragment>
    )
};

export default connect(null, {checkAuth, loadUser})(Layout);