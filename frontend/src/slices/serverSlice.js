import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { API_URL, IVCS_API_URL, CONFIG } from "../constants";
import axios from "axios";

const initialState = {
  isLoading: null,
  apiStatus: "",
  ivcsApiStatus: "",
  mediaServersId: [],
  auditLogLastEvents: [],
};

export const pingApi = createAsyncThunk("servers/pingApi", async () => {
  try {
    const pingRequest = `${API_URL}/api/v1/ping`;
    const response1 = await axios.get(pingRequest, CONFIG);
    return response1.data;
  } catch (err) {
    console.log(`${pingApi.name} что-то тут не так...`);
  }
});

export const pingIvcsApi = createAsyncThunk("servers/pingIvcsApi", async () => {
  try {
    const pingRequest = `${IVCS_API_URL}/api/ivcs/ping`;
    const response2 = await axios.get(pingRequest, CONFIG);
    return response2.data;
  } catch (err) {
    console.log(`${pingIvcsApi.name} что-то тут не так...`);
  }
});

export const auditLogEvent = createAsyncThunk(
  "servers/auditLogEvent",
  async (args, thunkAPI) => {
    try {
      // const {secureAudit, severity, start, end} = args;

      const getMediaServersRequest = `${IVCS_API_URL}/api/ivcs/audit_log_last_events`;
      // + `?secureAudit=${secureAudit}`
      // + `&severity=${severity}`
      // + `&start=${start}`
      // + `&end=${end}`;
      const response = await axios.get(getMediaServersRequest, CONFIG);
      return response.data;
    } catch (e) {
      console.log(`${auditLogEvent.name} что-то тут не так...`);
    }
  },
);

const serverSlice = createSlice({
  name: "serverManager",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(pingApi.pending, (state) => {
        state.isLoading = false;
      })
      .addCase(pingApi.fulfilled, (state, { payload }) => {
        state.isLoading = true;

        if (payload?.status === "ok") {
          state.servers = payload;
          state.apiStatus = "👍";
        } else {
          state.apiStatus = "❌";
        }
      })
      .addCase(pingApi.rejected, (state) => {
        state.isLoading = false;
        state.apiStatus = "Что-то тут не так...";
      })
      .addCase(pingIvcsApi.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(pingIvcsApi.fulfilled, (state, { payload }) => {
        state.isLoading = false;

        if (payload?.status === "ok") {
          state.ivcsApiStatus = "👍";
        } else {
          state.ivcsApiStatus = "❌";
        }
      })
      .addCase(pingIvcsApi.rejected, (state) => {
        state.isLoading = false;
        state.ivcsApiStatus = "Что-то тут не так...";
      })
      .addCase(auditLogEvent.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(auditLogEvent.fulfilled, (state, { payload }) => {
        state.isLoading = false;
        state.auditLogLastEvents = payload;
      })
      .addCase(auditLogEvent.rejected, (state) => {
        state.isLoading = false;
        state.auditLogLastEvents = [];
      });
  },
});

export default serverSlice.reducer;
