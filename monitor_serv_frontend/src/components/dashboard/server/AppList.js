import React, {useEffect, useState} from "react";

const AppList = ({id=0}) => {
    const [importantApps, setImportantApps] = useState([]);

    const updateImportantApps = () => {
        const appsDict = JSON.parse(localStorage.getItem(`checklistElems${id}`)) || {};
        const arr = [];
        for (let [key, value] of Object.entries(appsDict)) {
            arr.push(value);
        }

        setImportantApps(arr);
    };

    useEffect(() => {
        const interval = setInterval(updateImportantApps, 200);
        return () => clearInterval(interval);
    }, []);

    const appsStateField = (
        <div className="apps-state-field">
            Наведите курсор
            на число справа от
            индикатора приложений и выберите приложения
        </div>
    );

    return (
        <div className={`text-center mt-1 bg-info bg-info bg-opacity-10
            ${importantApps.length > 0 ? '' : 'd-flex justify-content-center'}`}>
                {typeof importantApps.map === "function" ? importantApps.length > 0
                    ? importantApps.map((app, i=0) => {
                        if (i <= 5)
                            return(
                                <div style={{color: app.color}}
                                    className="ms-1">{app.service}</div>
                            );
                        else
                            return <></>
                    }) : appsStateField : appsStateField
                }
        </div>
    );
};

export default AppList;