import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {API_URL, CONFIG} from "../base";
import Cookies from "js-cookie";
import axios from "axios";

CONFIG.headers = {
    ...CONFIG.headers,
    'X-CSRFToken': Cookies.get('csrftoken')
};

const initialState = {
    isAuthenticated: null,
    isLoading: null,
    isRegister: null,
    successMessage: '',
    errorMessage: '',
    registerErrors: []
};

export const registerAsync = createAsyncThunk(
    'auth/registerAsync',
    async ({
        username,
        first_name,
        last_name,
        email,
        password,
        password2
    }, thunkAPI) => {
        CONFIG.headers = {
            ...CONFIG.headers,
            'X-CSRFToken': Cookies.get('csrftoken')
        };


        const body = JSON.stringify({
            username,
            first_name,
            last_name,
            email,
            password,
            password2
        })

        try {
            const urlRequest = `${API_URL}/api/users/register`;
            const response = await axios.post(urlRequest, body, CONFIG);
            return response.data;
        } catch (err) {
            return err.response.data;
        }
    }
);

export const logoutAsync = createAsyncThunk(
    'authSlice/logoutAsync',
    async (arg, thunkAPI) => {
        try {
            const urlRequest = `${API_URL}/api/users/logout`;
            const response = await axios.post(urlRequest, CONFIG);

            return response.data;
        } catch (err) {
            return "something went wrong";
        }
    }
);

export const checkAuthenticationAsync = createAsyncThunk(
    'authSlice/checkAuthenticationAsync',
    async (arg, thunkAPI) => {
        try {
            const urlRequest = `${API_URL}/api/users/authentication`;
            const response = await axios.get(urlRequest, CONFIG);

            return response.data.isAuthenticated;
        } catch (err) {
            // return "something went wrong";
            console.log(err.response.status);
        }
    }
);

export const loginAsync = createAsyncThunk(
    'authSlice/loginAsync',
    async ({username, password}, ThunkAPI) => {
        const body = JSON.stringify({
            username, password
        });

        try {
            const urlRequest = `${API_URL}/api/users/login`;
            const response = await axios.post(urlRequest, body, CONFIG);

            return response.data.status;
        } catch (err) {
            return err.response.data;
        }
    }
);

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {},
    extraReducers: {
        // login
        [loginAsync.pending]: (state) => {
            state.isLoading = true;
            state.isAuthenticated = false;
        },
        [loginAsync.fulfilled]: (state, {payload}) => {
            if (payload?.non_field_errors) {
                state.errorMessage = payload.non_field_errors[0];
            }
            else if (payload === 'success') {
                state.isAuthenticated = true;
                state.successMessage = payload;
            }

            state.isLoading = false;
        },
        [loginAsync.rejected]: (state, {payload}) => {
            state.isLoading = false;
            state.errorMessage = payload;
        },
        // register
        [registerAsync.pending]:(state) => {
            state.isLoading = true;
        },
        [registerAsync.fulfilled]:  (state, {payload}) => {
            if (payload?.non_field_errors instanceof Array) {
                state.registerErrors.push(payload.non_field_errors)
                console.log(state.registerErrors)
            }
            else if (payload?.username instanceof Array) {
                state.registerErrors.push(payload.username);
            }
            else if (payload?.email instanceof Array) {
                state.registerErrors.push(payload.email);
            }
            else if (payload?.first_name instanceof Array) {
                state.registerErrors.push(payload.first_name);
            }
            else if (payload?.last_name instanceof Array) {
                state.registerErrors.push(payload.last_name);
            }
            else if (payload.success){
                state.successMessage = payload;
                state.isRegister = true;
            }

            state.isLoading = false;
        },
        [registerAsync.rejected]: (state, {payload}) => {
            state.isLoading = false;
            state.isRegister =  false;
            state.errorMessage = payload;
        },
        // check auth
        [checkAuthenticationAsync.pending]: (state) => {
            state.isLoading = true;
        },
        [checkAuthenticationAsync.fulfilled]: (state, {payload}) => {
            if (payload === "success") {
                state.successMessage = payload;
                state.isAuthenticated = true;
            } else {
                state.errorMessage = payload;
                state.isAuthenticated = false;
            }
            state.isLoading = false;
        },
        [checkAuthenticationAsync.rejected]: (state, {payload}) => {
            state.isLoading = false;
            state.errorMessage = payload;
        },
        // logout
        [logoutAsync.pending]: (state) => {
                state.isLoading = true;
            },
        [logoutAsync.fulfilled]: (state, {payload}) => {
            if (payload === "success") {
                state.successMessage = payload;
            } else {
                state.errorMessage = payload;
            }
            state.isAuthenticated = false;
            state.isLoading = false;
        },
        [logoutAsync.rejected]: (state, {payload}) => {
            state.isLoading = false;
            state.errorMessage = payload;
        },
    }
});

export default authSlice.reducer;