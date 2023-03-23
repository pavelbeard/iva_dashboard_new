import {Route, Navigate} from "react-router-dom";
import {connect} from "react-redux";

const PrivateRoute = ({component: Component, isAuth, ...rest}) => (
    <Route
        {...rest}
        render={props => isAuth ? <Component {...props} /> : <Navigate to="/login" />}
    />
);

const mapStateToProps = state => ({
    isAuth: state.auth.isAuth
})

export default connect(mapStateToProps, {})(PrivateRoute);
