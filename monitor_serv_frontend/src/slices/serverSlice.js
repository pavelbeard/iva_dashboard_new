import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {API_URL, CONFIG} from "../base";
import axios from "axios";

const initialState = {
    isLoading: null,
    servers: []
};

export const getServers = createAsyncThunk(
    'servers/getServers',
    async (arg, thunkAPI) => {
        try {
            const getTargetsRequest = `${API_URL}/api/targets/all`;
            const response1 = await axios.get(getTargetsRequest, CONFIG);

            return response1.data;
        } catch (err) {
            return [{status: "Что-то тут не так..."}];
        }
    }
);

const serverSlice = createSlice({
    name: 'serverManager',
    initialState,
    extraReducers: builder => {
        builder
            .addCase(getServers.pending, state => {
                state.isLoading = false;
            })
            .addCase(getServers.fulfilled, (state, {payload}) => {
                state.isLoading = true;
                state.servers = payload;
            })
            .addCase(getServers.rejected, state => {
                state.isLoading = false;
                state.servers = [{status: "Что-то тут не так..."}];
            })
    }
});

export default serverSlice.reducer;