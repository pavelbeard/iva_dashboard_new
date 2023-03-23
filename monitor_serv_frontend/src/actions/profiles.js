import axios from "axios";
import {API_URL} from "../base";

export const loadUser = async dispatch => {
    const config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await axios.get(`${API_URL}/api/users/me`, config)
    }
    catch (e) {

    }
}