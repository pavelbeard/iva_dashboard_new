import React, { useEffect, useState } from "react";

const AppList = ({ id = 0 }) => {
  const [importantApps, setImportantApps] = useState([]);

  const updateImportantApps = () => {
    const apps = JSON.parse(localStorage.getItem(`checklistElems${id}`)) || [];
    setImportantApps(apps);
  };

  useEffect(() => {
    const interval = setInterval(updateImportantApps, 200);
    return () => clearInterval(interval);
  }, []);

  const appsStateField = (
    <div className="apps-state-field">
      Наведите курсор на число справа от индикатора приложений и выберите
      приложения
    </div>
  );

  return (
    <div
      className={`text-center mt-1 bg-info bg-dark bg-opacity-25
            ${importantApps.length > 0 ? "" : "d-flex justify-content-center"}`}
    >
      {typeof importantApps.map === "function"
        ? importantApps.length > 0
          ? importantApps.map((app, i = 0) => {
              if (i <= 5)
                return (
                  <div style={{ color: app.status }} className="ms-1">
                    {app.name}
                  </div>
                );
              else return <></>;
            })
          : appsStateField
        : appsStateField}
    </div>
  );
};

export default AppList;
