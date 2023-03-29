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
    successMessage: [],
    errorMessage: '',
    registerErrors: [],
    loginErrors: []
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

            return response.data;
        } catch (err) {
            return err.response.data;
        }
    }
);

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        // login
        builder
        .addCase(loginAsync.pending, (state) => {
            state.isLoading = true;
            state.isAuthenticated = false;
            state.successMessage = [];
            state.loginErrors = [];
            state.errorMessage = ''
        })
        .addCase(loginAsync.fulfilled, (state, {payload}) => {
            if (payload?.non_field_errors) {
                payload.non_field_errors.forEach(error => {
                    state.loginErrors.push(error)
                });
                state.isAuthenticated = false;
            }
            else if (payload.success) {
                state.isAuthenticated = true;
                state.successMessage.push(payload.success);
            }

            state.isLoading = false;
        })
        .addCase(loginAsync.rejected, (state, {payload}) => {
            state.isLoading = false;
            state.errorMessage = "Что-то тут не так...";
        })
        // register
        .addCase(registerAsync.pending,(state) => {
            state.isLoading = true;
            state.registerErrors = [];
            state.successMessage = [];
            state.errorMessage = ''
        })
        .addCase(registerAsync.fulfilled,  (state, {payload}) => {
            if (payload?.non_field_errors instanceof Array) {
                payload.non_field_errors.forEach(error => {
                    state.registerErrors.push(error);
                });
            }
            else if (payload?.username instanceof Array) {
                payload.username.forEach(error => {
                    state.registerErrors.push(error);
                });
            }
            else if (payload?.email instanceof Array) {
                payload.email.forEach(error => {
                    state.registerErrors.push(error);
                });
            }
            else if (payload?.first_name instanceof Array) {
                payload.first_name.forEach(error => {
                    state.registerErrors.push(error);
                });
            }
            else if (payload?.last_name instanceof Array) {
                payload.last_name.forEach(error => {
                    state.registerErrors.push(error);
                });
            }
            else if (payload?.password instanceof Array) {
                payload.password.forEach(error => {
                    state.registerErrors.push(error);
                });
            }
            else if (payload.success){
                state.successMessage.push(payload.success);
                state.isRegister = true;
            }

            state.isLoading = false;
        })
        .addCase(registerAsync.rejected, (state, {payload}) => {
            state.isLoading = false;
            state.isRegister =  false;
            state.errorMessage = "Что-то тут не так...";
        })
        // check auth
        .addCase(checkAuthenticationAsync.pending, (state) => {
            state.isLoading = true;
        })
        .addCase(checkAuthenticationAsync.fulfilled, (state, {payload}) => {
            state.isAuthenticated = payload === "success";
            state.isLoading = false;
        })
        .addCase(checkAuthenticationAsync.rejected, (state, {payload}) => {
            state.isLoading = false;
        })
        // logout
        .addCase(logoutAsync.pending, (state) => {
                state.isLoading = true;
                state.successMessage = [];
                state.errorMessage = '';
            })
        .addCase(logoutAsync.fulfilled, (state, {payload}) => {
            if (payload.success) {
                state.successMessage.push(payload.success);
            } else {
                state.errorMessage = "Что-то тут не так...";
            }
            state.isAuthenticated = false;
            state.isLoading = false;
        })
        .addCase(logoutAsync.rejected, (state, {payload}) => {
            state.isLoading = false;
            state.errorMessage = "Что-то тут не так...";
        })
    }
});

export default authSlice.reducer;