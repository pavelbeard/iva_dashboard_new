import { useSelector } from "react-redux";
import { useEffect, useState } from "react";
import { IVCS_API_URL } from "../../../constants";
import axios from "axios";

const RoleIndicator = ({ host }) => {
  const refreshInterval = useSelector((state) => state.refresh.refreshInterval);
  const [role, setRole] = useState("NONE");

  const getMediaServers = async () => {
    let _role_;
    try {
      const urlRequest = `${IVCS_API_URL}/api/ivcs/media_servers`;
      const response = (await axios.get(urlRequest)).data;

      if (response) {
        const isExist = response.find(
          (i) => i.address === host.replace(/:.*/g, ""),
        );
        if (isExist) {
          setRole("MEDIA");
          _role_ = "MEDIA";
        } else {
          setRole("HEAD");
          _role_ = "HEAD";
        }
      } else {
        setRole("NONE");
        _role_ = "NONE";
      }
    } catch (e) {
      setRole("NONE");
      _role_ = "NONE";
      console.log("Что-то тут не так...");
    }

    localStorage[host] = JSON.stringify(_role_);
  };

  const setDataImmediately = () => {
    setTimeout(getMediaServers, 0);
  };

  useEffect(() => {
    setDataImmediately();
    const interval = setInterval(setDataImmediately, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  return <div>{role}</div>;
};

export default RoleIndicator;
