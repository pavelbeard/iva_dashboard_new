import {Navigate} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {useEffect, useState} from "react";
import {Modal} from "react-bootstrap";
import {checkAuthentication} from "../slices/authSlice";

const PrivateRoute = ({component}) => {
    const dispatch = useDispatch();
    const isAuthenticated = useSelector(state => state.auth.isAuthenticated);
    const [showLogin, setShowLogin] = useState(false);


    useEffect(() => {
        const interval = setInterval(() => {
            dispatch(checkAuthentication());
            if (!isAuthenticated) {
                setShowLogin(true);
            }
        }, 1000);
        return () => clearInterval(interval);
    }, [])

    return(
        <>
            {isAuthenticated ? component : <Navigate to="/login" />}
            <Modal isOpen={showLogin}>
                <h3>Ваша сессия истекла!</h3>
                <button onClick={() => <Navigate to="/login" />}>Вход</button>
            </Modal>
        </>
    );
    // if (isAuthenticated) {
    //     return component;
    // } else {
    //     navigate('/login');
    //     // return <Navigate to="/login" />
    //     // return(
    //     //     <>
    //     //         {component}
    //     //         <Modal isOpen={showModal}>
    //     //             <h3>Ваша сессия истекла</h3>
    //     //             <button onClick={handleLogin}>Вход</button>
    //     //         </Modal>
    //     //     </>
    //     // );
    // }
    // return isAuthenticated ? component : <Navigate to="/login" />;
};

export default PrivateRoute;