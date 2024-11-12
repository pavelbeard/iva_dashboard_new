import { Provider } from "react-redux";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Dashboard from "./components/containers/Dashboard";
import Home from "./components/containers/Home";
import Journals from "./components/containers/Journals";
import LoginPage from "./components/containers/LoginPage";
import RegisterPage from "./components/containers/RegisterPage";
import Pag from "./components/containers/TablePagination";
import Layout from "./components/hocs/Layout";
import PrivateRoute from "./components/hocs/PrivateRoute";
import store from "./store/store";

import "./i18n";

const App = () => (
  <Provider store={store}>
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/dashboard"
            element={<PrivateRoute component={<Dashboard />} />}
          />
          {/*<Route path="/charts" element={<PrivateRoute component={<Charts />} />}/>*/}
          <Route
            path="/journals"
            element={<PrivateRoute component={<Journals />} />}
          />
          <Route
            path="/test_pag"
            element={<PrivateRoute component={<Pag />} />}
          />
        </Routes>
      </Layout>
    </Router>
  </Provider>
);

export default App;
