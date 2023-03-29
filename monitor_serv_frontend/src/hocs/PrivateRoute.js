import {Navigate} from "react-router-dom";
import {useSelector} from "react-redux";

const PrivateRoute = ({component}) => {
    const isAuthenticated = useSelector(state => state
        .auth
        .isAuthenticated
    );

    return(
        isAuthenticated ? component : <Navigate to="/login" />
    );
};

export default PrivateRoute;