import thunk from 'redux-thunk';
import {configureStore} from "@reduxjs/toolkit";
import {combineReducers} from "redux";
import authSlice from "./slices/authSlice";
import profile from "./reducers/profile";

const middleware = [thunk];

const rootReducer = combineReducers({
    auth: authSlice,
    profile
});

const store = configureStore({
    reducer: rootReducer,
    devTools: true,
    middleware: defaultMiddleware => defaultMiddleware().concat(middleware)
})
export default store;