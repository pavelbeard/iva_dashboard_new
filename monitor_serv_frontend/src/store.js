import thunk from 'redux-thunk';
import {configureStore} from "@reduxjs/toolkit";
import {combineReducers} from "redux";
import authSlice from "./slices/authSlice";
import refreshIntervalSlice from "./slices/refreshIntervalSlice";
import serverSlice from "./slices/serverSlice";
import indicatorSlice from "./slices/indicatorSlice";
import datetimeSlice from "./slices/datetimeSlice";

const middleware = [thunk];

const rootReducer = combineReducers({
    auth: authSlice,
    serverManager: serverSlice,
    indicatorManager: indicatorSlice,
    refresh: refreshIntervalSlice,
    datetimeManager: datetimeSlice,
});

const store = configureStore({
    reducer: rootReducer,
    devTools: true,
    middleware: defaultMiddleware => defaultMiddleware().concat(middleware)
})
export default store;