import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {API_URL, IVCS_API_URL, CONFIG} from "../base";
import axios from "axios";

const initialState = {
    isLoading: null,
    apiStatus: '',
    ivcsApiStatus: ''
};

export const pingApi = createAsyncThunk(
    'servers/pingApi',
    async () => {
        try {
            const getTargetsRequest = `${API_URL}/api/v1/ping`;
            const response1 = await axios.get(getTargetsRequest, CONFIG);
            return response1.data;
        } catch (err) {
            console.log(`${pingApi.name} что-то тут не так...`)
        }
    }
);

export const pingIvcsApi = createAsyncThunk(
    'servers/pingIvcsApi',
    async () => {
        try {
            const getMediaServersRequest = `${IVCS_API_URL}/api/ivcs/ping`;
            const response2 = await axios.get(getMediaServersRequest, CONFIG);
            return response2.data
        } catch (err) {
            console.log(`${pingIvcsApi.name} что-то тут не так...`);
        }
    }
);

const serverSlice = createSlice({
    name: 'serverManager',
    initialState,
    extraReducers: builder => {
        builder
            .addCase(pingApi.pending, state => {
                state.isLoading = false;
            })
            .addCase(pingApi.fulfilled, (state, {payload}) => {
                state.isLoading = true;

                if (payload?.status === 'ok') {
                    state.servers = payload;
                    state.apiStatus = '👍';
                } else {
                    state.apiStatus = '❌';
                }
            })
            .addCase(pingApi.rejected, state => {
                state.isLoading = false;
                state.apiStatus = 'Что-то тут не так...';
            })
            .addCase(pingIvcsApi.pending, state => {
                state.isLoading = true;
            })
            .addCase(pingIvcsApi.fulfilled, (state, {payload}) => {
                state.isLoading = true;

                if (payload?.status === "ok") {
                    state.ivcsApiStatus = '👍';
                } else {
                    state.ivcsApiStatus = '❌';
                }
            })
            .addCase(pingIvcsApi.rejected, state => {
                state.isLoading = false;
                state.ivcsApiStatus = 'Что-то тут не так...';
            })
    }
});

export default serverSlice.reducer;