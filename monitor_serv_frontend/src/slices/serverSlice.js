import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {API_URL, IVCS_API_URL, CONFIG} from "../base";
import axios from "axios";

const initialState = {
    isLoading: null,
    apiStatus: '',
    ivcsApiStatus: '',
    mediaServersId: [],
    auditLogLastEvents: [],
    serversList: [],
};

export const pingApi = createAsyncThunk(
    'servers/pingApi',
    async () => {
        try {
            const pingRequest = `${API_URL}/api/v1/ping`;
            const response1 = await axios.get(pingRequest, CONFIG);
            return response1.data;
        } catch (err) {
            console.log(`${pingApi.name} что-то тут не так...`)
        }
    }
);

export const getServers = createAsyncThunk(
    'servers/getServers',
    async () => {
        try {
            const pingRequest = `${API_URL}/api/targets/all`;
            const response2 = await axios.get(pingRequest, CONFIG);
            return response2.data
        } catch (err) {
            console.log(`${getServers.name} что-то тут не так...`);
        }
    }
);

export const auditLogEvent = createAsyncThunk(
    'servers/auditLogEvent',
    async (args, thunkAPI) => {
        try {
            const getMediaServersRequest = `${IVCS_API_URL}/api/ivcs/audit_log_last_events`;
            const response = await axios.get(getMediaServersRequest, CONFIG);
            return response.data
        } catch (e) {
            console.log(`${auditLogEvent.name} что-то тут не так...`);
        }
    }
)

const serverSlice = createSlice({
    name: 'serverManager',
    initialState,
    reducers: {
        setServersList (state, {payload}) {
            state.servers = payload.servers;
        }
    },
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
            .addCase(getServers.pending, state => {
                state.isLoading = true;
            })
            .addCase(getServers.fulfilled, (state, {payload}) => {
                state.isLoading = false;

                if (payload.length > 0) {
                    state.serversList = payload;
                } else {
                    state.serversList = [];
                }
            })
            .addCase(getServers.rejected, state => {
                state.isLoading = false;
                state.serversList = 'Что-то тут не так...';
            })
            .addCase(auditLogEvent.pending, state => {
                state.isLoading = true;
            })
            .addCase(auditLogEvent.fulfilled, (state, {payload}) => {
                state.isLoading = false;
                state.auditLogLastEvents = payload;
            })
            .addCase(auditLogEvent.rejected, state => {
                state.isLoading = false;
                state.auditLogLastEvents = [];
            })
    }
});

export const {setServersList} = serverSlice.actions;
export default serverSlice.reducer;