import { useEffect } from "react";
import useAppDispatch from "../../lib/hooks/useAppDispatch";
import { checkAuthentication, setAsUser } from "../../slices/authSlice";
import { checkRefreshInterval } from "../../slices/refreshIntervalSlice";
import Header from "../containers/Header";
import Footer from "../containers/Footer";

const Layout = ({ children }) => {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(checkAuthentication());
    dispatch(setAsUser());
    dispatch(checkRefreshInterval());
  }, [dispatch]);

  return (
    <>
      <Header />
      {children}
      <Footer />
    </>
  );
};

export default Layout;
