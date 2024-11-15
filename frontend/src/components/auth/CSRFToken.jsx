import React, { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { API_URL } from "../../constants";

const CSRFToken = () => {
  const [csrfToken, setCsrfToken] = useState("");
  const getCookie = (name) => Cookies.get(name);

  const fetchData = async () => {
    const urlRequest = `${API_URL}/api/v1/csrf_cookie`;

    try {
      await axios.get(urlRequest);
    } catch (err) {}
  };

  useEffect(() => {
    setTimeout(fetchData, 0);
    setCsrfToken(getCookie("csrftoken"));
  }, []);

  return <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />;
};

export default CSRFToken;
