import axios from "axios";
import {API_URL, CONFIG} from "../base";
import {
    LOAD_USER_PROFILE_SUCCESS,
    LOAD_USER_PROFILE_FAIL,
    UPDATE_USER_PROFILE_SUCCESS,
    UPDATE_USER_PROFILE_FAIL
} from "./types";
import Cookies from "js-cookie";

export const deleteUser = () => async dispatch => {
    // NOT IMPLEMENTED
}

export const updateUser = () => async dispatch => {
    CONFIG.headers = {
        ...CONFIG.headers,
        'X-CSRFToken': Cookies.get('csrftoken'),
    }

    try {
        const response = await axios.put(`${API_URL}/api/users/update`);

        if (response.data.username && response.data.email) {
            dispatch({
                type: UPDATE_USER_PROFILE_SUCCESS,
                payload: response.data
            });
        } else {
            dispatch({
                type: UPDATE_USER_PROFILE_FAIL
            });
        }

    } catch (err) {
        dispatch({
            type: UPDATE_USER_PROFILE_FAIL
        });
    }

}

export const loadUser = () => async dispatch => {
    try {
        const response = await axios.get(`${API_URL}/api/users/me`, CONFIG);

        if (response.data.error) {
            dispatch({
                type: LOAD_USER_PROFILE_FAIL
            });
        } else {
            dispatch({
                type: LOAD_USER_PROFILE_SUCCESS,
                payload: response.data
            });
        }
    }
    catch (err) {
        dispatch({
            type: LOAD_USER_PROFILE_FAIL
        });
    }
}