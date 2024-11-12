import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { useEffect } from "react";

const PrivateRoute = ({ component }) => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

  return isAuthenticated ? component : <Navigate to="/login" />;
};

export default PrivateRoute;
