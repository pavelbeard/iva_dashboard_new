import thunk from "redux-thunk";
import { configureStore } from "@reduxjs/toolkit";
import { combineReducers } from "redux";
import authReducer from "../slices/authSlice";
import refreshIntervalReducer from "../slices/refreshIntervalSlice";
import serverReducer from "../slices/serverSlice";
import indicatorReducer from "../slices/indicatorSlice";

const middleware = [thunk];

const rootReducer = combineReducers({
  auth: authReducer,
  serverManager: serverReducer,
  indicatorManager: indicatorReducer,
  refresh: refreshIntervalReducer,
});

const store = configureStore({
  reducer: rootReducer,
  devTools: true,
  middleware: (defaultMiddleware) => defaultMiddleware().concat(middleware),
});
export default store;
