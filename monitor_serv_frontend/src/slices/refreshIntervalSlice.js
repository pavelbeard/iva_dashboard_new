import {createSlice} from "@reduxjs/toolkit";

const initialState = {
    refreshInterval: 5000
};

const refreshIntervalSlice = createSlice({
    name: 'refresh',
    initialState,
    reducers: {
        changeRefreshInterval(state, {payload}) {
            localStorage.setItem('refreshInterval', parseInt(payload));
            state.refreshInterval = localStorage.getItem('refreshInterval');
        },
        checkRefreshInterval(state) {
            const refreshIntervalState = localStorage.getItem('refreshInterval') !== null;
            if (refreshIntervalState) {
                state.refreshInterval = localStorage.getItem('refreshInterval');
            }
        }
    }
});

export const {changeRefreshInterval, checkRefreshInterval} = refreshIntervalSlice.actions;
export default refreshIntervalSlice.reducer;

