import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {API_URL, CONFIG, IVCS_API_URL} from "../base";
import axios from "axios";

const initialState = {
    isLoading: null,
    conferenceData: [],
    servicesData: [],
    importantServices: []
};

export const getConfData = createAsyncThunk(
    'indicators/getConfData',
    async(arg, thunkAPI) => {
        try {
            const urlRequest = `${IVCS_API_URL}/api/ivcs/conference_data`
        } catch (err) {

        }
    }
);

export const getServicesData = createAsyncThunk(
    'indicators/getServicesData',
    async ({id}, thunkAPI) => {
        try {
            const urlRequest = `${API_URL}/api/v1/services_status/${id}`;
            const response = await axios.get(urlRequest, CONFIG);
            return response.data;
        } catch (err) {
            return {status: "что-то тут не так..."};
        }
    }
);

const indicatorSlice = createSlice({
    name: 'indicatorManager',
    initialState,
    extraReducers: builder => {
        builder
            .addCase(getServicesData.pending, state => {
                state.isLoading = true;
            })
            .addCase(getServicesData.fulfilled, (state, {payload}) => {
                state.servicesData = [];

                if (!payload.status) {
                    console.log(payload)
                }
            })
    }
});

export default indicatorSlice.reducer;