export const SEVERITY = {
    1: ["Ошибка", "ERROR"],
    2: ["Предупреждение", "WARNING"],
    3: ["Информация", "INFO"],
};

export const RECORD_TYPE = {
    0: ["Компания", "COMPANY"],
    1: ["Конференция", "CONFERENCE"],
    2: ["Сеанс конференции", "CONFERENCE_SESSION"],
    3: ["Домен", "DOMAIN"],
    4: ["Ошибка", "ERROR"],
    5: ["Настройки", "SETTINGS"],
    6: ["Профиль пользователя", "USER_PROFILE"],
    7: ["Сессия пользователя", "USER_SESSION"],
    8: ["Лицензия", "LICENSE"],
    9: ["Ошибка безопасности", "SECURITY"],
    10: ["Чат", "INSTANT_MESSAGING"],
    11: ["Контроль безопасности", "SECURITY_CONTROL"],
};

export function changePageNumStyle() {

}

export function* changedParams (object) {
    for (let outerValue of Object.values(object)) {
        if (typeof outerValue === "object") {
            for (let [innerKey, innerValue] of Object.entries(outerValue)) {
                const oldValue = innerValue.oldValue;
                const newValue = innerValue.newValue;
                yield <div>Параметр <b>
                    {innerKey}</b> изменен с <b>{oldValue}</b> на <b>{newValue}</b></div>;
            }
        }
    }
}

export function parseInfo (object) {
    console.log(object)
    const username = object['userName'] || object['username'] || object['login'];
    const conference = object['conferenceSessionName'] || object['name'] || object['eventName'];
    const eventType = object['changeType']
        || object['accessErrorType']
        || object['reason']
        || object['unauthorizedAccessType'];
    const leaveReason = object['leaveReason'];
    const userAgent = object['userAgent'] || "unknown";
    const sessionEndType = object['sessionEndType'];
    const domainName = object['domainName'];
    const roles = object['roles'] || [];
    const protocol = object['protocol'];

    switch (eventType) {
        case "LOGIN":
            return (<div>
                Пользователь вошел в систему в домене <b>{domainName}</b>.
                <br/>
                Клиентское приложение: <b>{userAgent}</b>
            </div>)
        case "JOIN":
            return <div>Пользователь <b>{username}</b> вошел в конференцию <b>
                "{conference}"</b> в роли {roles.map(role => {return <b>{role}</b>})} <br />
                Протокол: <b>{protocol}</b>
            </div>
        case "UPDATE":
            return <div>Изменены настройки пользователя <b>{username}</b> в мероприятии <b>{conference}</b>
                {Array.from(changedParams(object)).map(item => {
                    return (<div>{item}</div>)
                })}</div>
        case "LOGOUT":
            return (
                <>
                    <div>Пользователь <b>{username}</b> вышел из системы <b>{domainName}</b> по причине <b>
                        {sessionEndType}
                    </b></div>
                    <div>Клиентское приложение:</div>
                    <div><b>{userAgent}</b></div>
                </>
            ) ;
        case "LEAVE":
            return <div>Пользователь <b>{username}</b> вышел из мероприятия <b>
                {conference}
            </b> по причине <b>{leaveReason}</b></div>;
        case "INCORRECT_EVENT_ID":
            return <div>Ошибка при попытке доступа к ресурсу: введен неверный ID мероприятия</div>;
        case "INVALID_CREDENTIALS":
            return <div>Не удалось выполнить вход в домен <b>{domainName}</b><br/>
                с учетными данными <b>{username} из-за неверных учетных данных</b></div>
        case "BLOCKED_ACCESS_FROM_IP":
            return <div>Ошибка при попытке доступа к ресурсу: IP-адрес заблокирован</div>;
        case "BLOCKED_ACCESS_FROM_PROFILE":
            return <div>Доступ из профиля заблокирован</div>;
        case "NOT_IN_CONFERENCE":
            return <div>Попытка неавторизованного выполнения операции в мероприятии <b>{conference}</b>
            <br/>
                пользователь не находится в мероприятии
            </div>;
        case "NO_OPERATOR_ROLE":
            return <div>Попытка неавторизованного выполнения операции в администрировании:
                <br/>отсутствует роль оператора системы
            </div>;
        default:
            return '';
    }
}