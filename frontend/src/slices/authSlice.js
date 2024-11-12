import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { API_URL, CONFIG } from "../constants";
import Cookies from "js-cookie";
import axios from "axios";

const initialState = {
  isAuthenticated: null,
  asUser: "",
  isLoading: null,
  isRegister: null,
  successMessage: [],
  errorMessage: "",
  registerErrors: [],
  loginErrors: [],
};

CONFIG.headers = {
  ...CONFIG.headers,
  "X-CSRFToken": Cookies.get("csrftoken"),
};

export const registerAsync = createAsyncThunk(
  "auth/registerAsync",
  async (
    { username, first_name, last_name, email, password, password2 },
    thunkAPI,
  ) => {
    const body = JSON.stringify({
      username,
      first_name,
      last_name,
      email,
      password,
      password2,
    });

    try {
      const urlRequest = `${API_URL}/api/users/register`;
      const response = await axios.post(urlRequest, body, CONFIG);
      return response.data;
    } catch (err) {
      return err.response.data;
    }
  },
);

export const logoutAsync = createAsyncThunk(
  "authSlice/logoutAsync",
  async (arg, thunkAPI) => {
    try {
      const urlRequest = `${API_URL}/api/users/logout`;
      const response = await axios.post(urlRequest, CONFIG);

      return response.data;
    } catch (err) {
      return "something went wrong";
    }
  },
);

export const loginAsync = createAsyncThunk(
  "authSlice/loginAsync",
  async ({ username, password }, ThunkAPI) => {
    const body = JSON.stringify({
      username,
      password,
    });

    try {
      const urlRequest = `${API_URL}/api/users/login`;
      const response = await axios.post(urlRequest, body, CONFIG);

      return response.data;
    } catch (err) {
      return err.response.data;
    }
  },
);

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    checkAuthentication(state) {
      const authState = localStorage.getItem("isAuthenticated") !== null;
      if (authState) {
        state.isAuthenticated = localStorage.getItem("isAuthenticated");
      } else {
        state.isAuthenticated = false;
      }
    },
    setAsUser(state) {
      const userState = localStorage.getItem("asUser") !== null;
      if (userState) {
        state.asUser = localStorage.getItem("asUser");
      } else {
        state.asUser = "";
      }
    },
  },
  extraReducers: (builder) => {
    // login
    builder
      .addCase(loginAsync.pending, (state) => {
        state.isLoading = true;
        state.isAuthenticated = false;
        state.successMessage = [];
        state.loginErrors = [];
        state.errorMessage = "";
      })
      .addCase(loginAsync.fulfilled, (state, { payload }) => {
        if (payload?.non_field_errors) {
          payload.non_field_errors.forEach((error) => {
            state.loginErrors.push(error);
          });
          state.isAuthenticated = false;
        } else if (payload.success) {
          localStorage.setItem("isAuthenticated", true);
          localStorage.setItem("asUser", payload.success);
          state.successMessage.push(payload.success);
          state.isAuthenticated = localStorage.getItem("isAuthenticated");
          state.asUser = localStorage.getItem("asUser");
        }

        state.isLoading = false;
      })
      .addCase(loginAsync.rejected, (state, { payload }) => {
        state.isLoading = false;
        state.errorMessage = "Сервер авторизации недоступен";
        localStorage.removeItem("isAuthenticated");
        localStorage.removeItem("asUser");
      })
      // register
      .addCase(registerAsync.pending, (state) => {
        state.isLoading = true;
        state.registerErrors = [];
        state.successMessage = [];
        state.errorMessage = "";
      })
      .addCase(registerAsync.fulfilled, (state, { payload }) => {
        if (payload?.non_field_errors instanceof Array) {
          payload.non_field_errors.forEach((error) => {
            state.registerErrors.push(error);
          });
        } else if (payload?.username instanceof Array) {
          payload.username.forEach((error) => {
            state.registerErrors.push(error);
          });
        } else if (payload?.email instanceof Array) {
          payload.email.forEach((error) => {
            state.registerErrors.push(error);
          });
        } else if (payload?.first_name instanceof Array) {
          payload.first_name.forEach((error) => {
            state.registerErrors.push(error);
          });
        } else if (payload?.last_name instanceof Array) {
          payload.last_name.forEach((error) => {
            state.registerErrors.push(error);
          });
        } else if (payload?.password instanceof Array) {
          payload.password.forEach((error) => {
            state.registerErrors.push(error);
          });
        } else if (payload.success) {
          state.successMessage.push(payload.success);
          state.isRegister = true;
        }

        state.isLoading = false;
      })
      .addCase(registerAsync.rejected, (state, { payload }) => {
        state.isLoading = false;
        state.isRegister = false;
        state.errorMessage = "Сервер авторизации недоступен";
      })
      .addCase(logoutAsync.pending, (state) => {
        state.isLoading = true;
        state.successMessage = [];
        state.errorMessage = "";
      })
      .addCase(logoutAsync.fulfilled, (state, { payload }) => {
        if (payload.success) {
          state.successMessage.push(payload.success);
          localStorage.removeItem("isAuthenticated");
          localStorage.removeItem("asUser");
          localStorage.removeItem("currentPage");
        } else {
          state.errorMessage = "Что-то тут не так...";
        }
        state.isAuthenticated = false;
        state.isLoading = false;
      })
      .addCase(logoutAsync.rejected, (state, { payload }) => {
        state.isLoading = false;
        state.errorMessage = "Сервер авторизации недоступен";
        localStorage.removeItem("isAuthenticated");
        localStorage.removeItem("asUser");
      });
  },
});

export const { checkAuthentication, setAsUser } = authSlice.actions;
export default authSlice.reducer;
