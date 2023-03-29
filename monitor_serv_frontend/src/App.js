import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'

import Layout from './hocs/Layout';
import Home from './containers/Home';
import RegisterPage from "./containers/RegisterPage";
import LoginPage from "./containers/LoginPage";
import Dashboard from "./containers/Dashboard";
import Charts from "./containers/Charts";
import PrivateRoute from "./hocs/PrivateRoute";
import {Provider} from "react-redux";

import store from "./store";
import 'bootstrap/dist/css/bootstrap.css';

const App = () => (
    <Provider store={store}>
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/register" element={<RegisterPage/>}/>
                    <Route path="/login" element={<LoginPage/>}/>
                    <Route path="/dashboard" element={<PrivateRoute component={<Dashboard />} />}/>
                    <Route path="/charts" element={<PrivateRoute component={<Charts />} />}/>
                </Routes>
            </Layout>
        </Router>
    </Provider>
);


export default App;
