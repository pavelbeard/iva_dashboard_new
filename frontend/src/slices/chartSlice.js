import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import thunk from "redux-thunk";

const initialState = {
  filter: "interval.last.hour",
  group: "group.System",
  data: [],
};

const getQueryResultAsync = createAsyncThunk(
  "charts/getQueryResultAsync",
  async ({ query, filter }, thunkAPI) => {},
);

const chartSlice = createSlice({
  name: "chartManager",
  initialState,
  reducers: {
    setFilter(state) {},
  },
  extraReducers: (builder) => {},
});
