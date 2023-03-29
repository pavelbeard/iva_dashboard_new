import {
    LOAD_USER_PROFILE_SUCCESS,
    LOAD_USER_PROFILE_FAIL,
    UPDATE_USER_PROFILE_SUCCESS,
    UPDATE_USER_PROFILE_FAIL
} from "../actions/types";

const initialState = {
    isAuthenticated: null,
    username: '',
    first_name: '',
    last_name: '',
    email: '',
}

export default function (state = initialState, action) {
    const {type, payload} = action;

    switch (type) {
        case UPDATE_USER_PROFILE_SUCCESS:
        case LOAD_USER_PROFILE_SUCCESS:
            return {
                ...state,
                username: payload.username,
                first_name: payload.first_name,
                last_name: payload.last_name,
                email: payload.email
            }
        case LOAD_USER_PROFILE_FAIL:
            return {
                ...state,
                username: '',
                first_name: '',
                last_name: '',
                email: ''
            }
        case UPDATE_USER_PROFILE_FAIL:
            return {
                ...state
            }
        default:
            return state;
    }
};