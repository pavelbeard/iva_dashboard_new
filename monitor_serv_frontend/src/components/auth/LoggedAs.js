import React from "react";
import {useDispatch, useSelector} from "react-redux";

const LoggedAs = () => {
    const username = useSelector(state => state.auth.asUser);

    return(<div className="text-white">Вы вошли как: {username}</div>)
};

export default LoggedAs;