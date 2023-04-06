import {useSelector} from "react-redux";
import {useEffect, useState} from "react";
import {IVCS_API_URL} from "../../../base";
import axios from "axios";

const RoleIndicator = ({host}) => {
    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    const [role, setRole] = useState("NONE")

    const getMediaServers = async () => {
        try {
            const urlRequest = `${IVCS_API_URL}/api/ivcs/media_servers`;
            const response = (await axios.get(urlRequest)).data;

            if (response) {
                const isExist = response.find(i => i.address === host.replace(/:.*/g, ''))
                if (isExist) {
                    setRole('MEDIA');
                } else {
                    setRole('HEAD');
                }
            } else {
                setRole('NONE')
            }
        } catch (e) {
            setRole('NONE')
            console.log('Что-то тут не так...')
        }
    };

    const setDataImmediately = () => {
        setTimeout(getMediaServers, 0);
    };

    useEffect(() => {
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);

    }, [refreshInterval])

    return(
        <div>{role}</div>
    )
};

export default RoleIndicator