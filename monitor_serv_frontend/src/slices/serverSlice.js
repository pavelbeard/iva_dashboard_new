import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {API_URL, IVCS_API_URL, CONFIG} from "../base";
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
            const getMediaServersRequest = `${IVCS_API_URL}/api/ivcs/media_servers`;
            const response2 = await axios.get(getMediaServersRequest, CONFIG);

            let length;
            if (response1.data.length < response2.data.length)
                length = response1.data.length;
            else
                length = response2.data.length;

            //check media
            for (let i = 0; i < length; i++) {
                if (response1.data[i]['address'] === response2.data[i]['address'])
                    response1.data[i].role = "media";
                else
                    response1.data[i].role = "head";
            }
            // console.log(response1)
            // console.log(response2)

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