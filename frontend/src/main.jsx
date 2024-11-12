import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App";
import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true;

const root = document.getElementById("app");
createRoot(root).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
