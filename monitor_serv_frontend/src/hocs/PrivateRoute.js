import {Navigate} from "react-router-dom";
import {useSelector} from "react-redux";
import {parse} from "../base";
import {useEffect} from "react";

const PrivateRoute = ({component}) => {
    const isAuthenticated = useSelector(state => state
        .auth
        .isAuthenticated
    );

    useEffect(() => {
        console.log(isAuthenticated)
    })
    // const page = parse('currentPage').page || "/login";

    return isAuthenticated ? component : <Navigate to="/login" />;
};

export default PrivateRoute;