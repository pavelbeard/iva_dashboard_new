import Cookies from 'js-cookie';
import axios from 'axios';
import {
    REGISTER_SUCCESS,
    REGISTER_FAIL
} from "./types";
import {API_URL} from "../base";

export const register = (username, first_name, last_name, email, password, password2) => async dispatch => {
    const config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
    };

    const body = JSON.stringify({
        username, first_name, last_name, email, password, password2
    });
    
    try {
        const urlRequest = `${API_URL}/api/users/register`;
        const response = await axios.post(urlRequest, body, config);

        if (response.data.error) {
            dispatch({
                type: REGISTER_FAIL
            })
        } else {
            dispatch({
                type: REGISTER_SUCCESS
            })
        }

    } catch (err) {
        dispatch({
            type: REGISTER_FAIL
        })
    }
}