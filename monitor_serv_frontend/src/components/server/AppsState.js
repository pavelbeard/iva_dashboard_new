import React, {useEffect, useState} from "react";
import {AppIndicator} from "react-bootstrap-icons";
import {Tooltip} from "react-tooltip";
import {v4} from "uuid";
import * as query from '../queries'
import {getData, sum, URL} from "../base";

const AppsState = ({host, refreshInterval, targetHealth}) => {
    const [appsCount, setAppsCount] = useState("N/A");
    const [appsDataTooltip, setAppsDataTooltip] = useState([]);
    const [color, setColor] = useState("#000000");

    const getAppsData = async () => {
        const urlRequest = URL + `?query=${encodeURI(query.modules.processes)}`
            + `&host=${host}`
            + `&query_range=false`;
        // const data = await postData(url, body);
        const data = await getData(urlRequest);

        if (data) {
            const __appsDataTooltip__ = data.data.result;

            setAppsDataTooltip(__appsDataTooltip__);

            const __appsCount__ = sum(__appsDataTooltip__.map(i => {
                return parseInt(i.value[1]);
            }));

            if (0 <= __appsCount__ && __appsCount__ < 100)
                setColor("#16b616");
            else if (100 <= __appsCount__ && __appsCount__ < 400)
                setColor("#ff9900");
            else
                setColor("#ff0000");

            setAppsCount(__appsCount__);
        } else {
            setColor("#000000");
            setAppsCount("ERR");
        }
    }

    const setDataImmediately = () => {
        setTimeout(getAppsData, 0);
    };

    useEffect(() => {
        setDataImmediately();
        const interval = setInterval(setDataImmediately, refreshInterval);
        return () => clearInterval(interval);
    }, []);

    const uuid = v4();

    return(
        <div className="d-flex flex-row justify-content-start mt-1">
            <AppIndicator height="24" width="24" color={color} data-ivcs-server-img-attr="apps"/>
            <div className="ps-3 mt-1" data-ivcs-server-attr="apps">
                <a data-tooltip-id={uuid}>{appsCount}</a>
                <Tooltip id={uuid} place="bottom">
                    <table>
                        <thead>
                            <tr>
                                <th>Process name</th>
                                <th>Process count</th>
                            </tr>
                        </thead>
                        <tbody>
                            {appsDataTooltip.map(i => {
                                return(
                                    <tr key={i.metric.__name__}>
                                        <td>{i.metric.__name__}</td>
                                        <td>{i.value[1]}</td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </table>
                </Tooltip>
            </div>
        </div>
    );
};

export default AppsState;