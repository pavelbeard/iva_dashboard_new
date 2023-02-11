let headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
}

/**
     * подфункция inspectServers.
     * @param url url метрики в бэкенде.
     * @param method HTTP метод.
     * @param callback функция, обрабатывающая результат опроса серверов
     */
async function getMetricsFromBackend(url, method, callback) {
    const response = await fetch(url, {
        method: method, headers: headers
    }).then(async r => {
        return await r.json();
    }).catch(e => {
        console.log(e);
    });
}