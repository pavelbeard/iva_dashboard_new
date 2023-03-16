import React, {useEffect, useState} from "react";
import {AppIndicator} from "react-bootstrap-icons";
import {Tooltip} from "react-tooltip";
import {v4} from "uuid";
import axios from "axios";

const AppsState = ({address, port, refreshInterval}) => {
    const [appsCount, setAppsCount] = useState("N/A");
    const [appsDataTooltip, setAppsDataTooltip] = useState("N/A");
    const [color, setColor] = useState("#000000");
    const [iRefreshInterval, setIRefreshInterval] = useState(300);

    useEffect(() => {
        const interval = address && port ? setInterval(() => {
            const query = 'query?query=label_keep(alias(sum by (instance) ' +
                '(namedprocess_namegroup_num_procs), "Process count"), "__name__")';
            const url = `http://${address}:${port}/api/v1/${query}`;

            axios.get(url, {params: {query: encodeURI(query)}})
                .then(response => {
                    if (response.data) {
                        setAppsDataTooltip(response.data);

                        const __appsCount__ = parseInt(response.data.data.result[0].value[1]);

                        if (0 <= __appsCount__ && __appsCount__ < 100 )
                            setColor("#16b616");
                        else if (100 <= __appsCount__ && __appsCount__ < 400)
                            setColor("#ff9900");
                        else
                            setColor("#ff0000");

                        setAppsCount(response.data.data.result[0].value[1]);
                        setIRefreshInterval(refreshInterval);
                    }
                })

        }, iRefreshInterval) : 500;
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
                                <th>Process count</th>
                            </tr>
                        </thead>
                        <tbody>
                            {appsDataTooltip.data === undefined ? "N/A" : appsDataTooltip.data.result.map(i => {
                                return(
                                    <tr key={i.metric.__name__}>
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