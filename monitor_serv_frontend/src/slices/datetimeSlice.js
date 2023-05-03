import {createSlice} from "@reduxjs/toolkit";

const MOSCOW_TIME = 180

let startDate = new Date();
startDate.setHours(startDate.getHours() - 1);
startDate.setMinutes(startDate.getMinutes() + 180);
startDate = startDate.toISOString();

let endDate = new Date();
endDate.setMinutes(endDate.getMinutes() + 180);
endDate = endDate.toISOString();

export const setDate = (oldDate, op) => {
    const date = new Date(oldDate);
    let res;

    if (op === "+") {
        res = date.getMinutes() + MOSCOW_TIME;
    } else if (op === "-") {
        res = date.getMinutes() - MOSCOW_TIME
    }

    date.setMinutes(res);
    return date.toISOString();
};

const initialState = {
    startDate: startDate,
    endDate: endDate,
    period: "1h",
    autoupdate: false
};

const datetimeSlice = createSlice({
    name: 'datetimeManager',
    initialState,
    reducers: {
        setStartDate(state, {payload}) {
            state.startDate = setDate(payload.value, payload.op);
        },
        setEndDate(state, {payload}) {
            state.endDate = setDate(payload.value, payload.op);
        },
        setPeriod(state, {payload}) {
            state.period = payload.period;
        },
        setAutoupdate(state, {payload}) {
            state.autoupdate = payload.autoupdate
        }
    }
});

export const {
    setStartDate,
    setEndDate,
    setPeriod,
    setAutoupdate
} = datetimeSlice.actions;
export default datetimeSlice.reducer;