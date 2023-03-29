import Cookies from 'js-cookie';
import axios from 'axios';
import {
    REGISTER_SUCCESS,
    REGISTER_FAIL,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT_SUCCESS,
    LOGOUT_FAIL,
    AUTHENTICATED_SUCCESS,
    AUTHENTICATED_FAIL,
} from "./types";
import {API_URL, CONFIG} from "../base";
import {loadUser} from "./profiles";

export const checkAuthenticated = () => async dispatch => {
    try {
        const urlRequest = `${API_URL}/api/users/authentication`;
        const response = await axios.get(urlRequest, CONFIG);

        if (response.data.isAuthenticated === "error") {
            dispatch({
                type: AUTHENTICATED_FAIL,
                payload: false,
            })
        }
        else if (response.data.isAuthenticated === "success") {
            dispatch({
                type: AUTHENTICATED_SUCCESS,
                payload: true
            })
        }

    } catch (err) {
        dispatch({
            type: AUTHENTICATED_FAIL,
            payload: false
        })
    }
}

export const logout = () => async dispatch => {
    CONFIG.headers = {
        ...CONFIG.headers,
        'X-CSRFToken': Cookies.get('csrftoken'),
    }

    try {
        const urlRequest = `${API_URL}/api/users/logout`;
        const response = await axios.post(urlRequest, CONFIG);

        if (response.data.success) {
            dispatch({
                type: LOGOUT_SUCCESS,
            });
        } else {
            dispatch({
                type: LOGOUT_FAIL,
            });
        }
    } catch (err) {
        dispatch({
            type: LOGOUT_FAIL
        })
    }
}

export const login = (username, password) => async dispatch => {
    CONFIG.headers = {
        ...CONFIG.headers,
        'X-CSRFToken': Cookies.get('csrftoken'),
    }

    const body = JSON.stringify({
        username, password
    });

    try {
        const urlRequest = `${API_URL}/api/users/login`;
        const response = await axios.post(urlRequest, body, CONFIG);

        if (response.data.error) {
            dispatch({
                type: LOGIN_FAIL,
            });
        } else {
            dispatch({
                type: LOGIN_SUCCESS,
            });

            dispatch(loadUser());
        }
    } catch (err) {
        dispatch({
            type: LOGIN_FAIL
        })
    }
}

export const register = (username, first_name, last_name, email, password, password2) => async dispatch => {
    CONFIG.headers = {
        ...CONFIG.headers,
        'X-CSRFToken': Cookies.get('csrftoken'),
    }

    const body = JSON.stringify({
        username, first_name, last_name, email, password, password2
    });
    
    try {
        const urlRequest = `${API_URL}/api/users/register`;
        const response = await axios.post(urlRequest, body, CONFIG);

        if (response.data.error) {
            dispatch({
                type: REGISTER_FAIL,
            });
        } else {
            dispatch({
                type: REGISTER_SUCCESS,
            });
        }

    } catch (err) {
        dispatch({
            type: REGISTER_FAIL,
        });
    }
}