function fileSysAnalysis(data, host) {
    let connErr = (data[0].filesystem === undefined) ? "" : 0;
    let result = (connErr !== "");

    host.childNodes[3].childNodes[5].style = result ? "#69ff4e" : "#bebdbd";

}

function ramAnalysis(data, host) {
    let connErr = (data[0].ram_util === undefined) ? "" : 0
    let result = (connErr !== "")

    host.childNodes[3].childNodes[3].style.backgroundColor = result ? "#69ff4e" : "#bebdbd"
    host.childNodes[3].childNodes[3].childNodes[2].textContent = result ? `${data[0].ram_util}%` : "Неизвестно%"

    let total = data[1].ram_total.trim()
    let free = data[2].ram_free.trim()
    let used = data[3].ram_used.trim()

    host.childNodes[3].childNodes[3]
        .title = `Total RAM: ${total}GB\nFree RAM: ${free}GB\nUsed RAM: ${used}GB`
}

function cpuAnalysis(data, host) {
    let connErr = (data[0].cpu_load === undefined) ? "" : 0
    let result = (connErr !== "")

    host.childNodes[3].childNodes[1].style.backgroundColor = result ? "#69ff4e" : "#bebdbd"
    host.childNodes[3].childNodes[1].childNodes[2].textContent = result ? `${data[0].cpu_load}%` : "Неизвестно%"

    //вывод всех ядер и количества ядер
    let core = 0
    let cores  = "".concat(data.slice(2, -1).map(el => `Core ${core++}: ${Object.values(el)[0]}%`))
        .replace( /,/g, '\n')

    host.childNodes[3].childNodes[1]
        .title = result ? `CPU idle: ${data[1].cpu_idle}%\nCPU cores: ${data[data.length - 1].cpu_cores}\n`
        + cores  : ""

}

function execAnalysis(data, host) {
    let connErr = (data[0].status === undefined) ? "" : 0
    let result = (connErr !== "")

    // TODO: Здесь будут выводиться результаты из crm status

    let processesArray = data.map(el => {
        let st = ''
        switch (el.status) {
            case 'running':
                st += ' [+]'
                break
            case 'stopped':
                st += ' [-]'
                break
            default:
                st += ' [?]'
                break
        }
        return `${el.service}: ${el.status}${st}`;
    });
    let processesTooltip, processesCount;

    [processesTooltip, processesCount] = ["".concat(processesArray).replace(/,/g, '\n'),
        processesArray.length];

    //processes
    host.childNodes[3].childNodes[7].title = result ? processesTooltip : "";
    host.childNodes[3].childNodes[7].childNodes[2].textContent = result ? processesCount : 0;
    host.childNodes[3].childNodes[7].style.backgroundColor = result ? "#69ff4e" : "#bebdbd";


}

function updateServerNode(hostname, data, id, callback) {
    let host = document.getElementById(id);

    let connError = "no connection with server."
    let result = (data[0] !== connError)

    // set hostname
    host.childNodes[1].childNodes[1].childNodes[3].textContent = result  ? hostname : "Хост недоступен\n";

    // server status
    host.childNodes[1].childNodes[1].style.backgroundColor = result ? "#69ff4e" : "#ff0000"
    host.childNodes[1].childNodes[1].childNodes[5].textContent = result ? "UP\n" : "DOWN\n";

    callback(data, host, connError)

}

function monitorUnavailable(servers) {
    let bg_unavailable = "#bebdbd"
    for (let server of servers) {
        // title
        server.childNodes[1].childNodes[1].childNodes[3].setAttribute('style', 'white-space: pre;')
        server.childNodes[1].childNodes[1].childNodes[3].textContent = "Агент мониторинга\r\nнедоступен"
        server.childNodes[1].childNodes[1].childNodes[5].textContent = "no data"
        // server status
        server.childNodes[1].childNodes[1].style.backgroundColor = bg_unavailable
        //
        server.childNodes[1].childNodes[3].childNodes[1].src = "/static/dashboard/images/icons8-unlike-64.png"
        server.childNodes[1].childNodes[3].childNodes[2].textContent = "?  "
        // server info
        let server_info_pane = server.childNodes[3].childNodes
        for (let i = 1; i < server_info_pane.length; i += 2) {
            // изменяем все индикаторы
            server_info_pane[i].style.backgroundColor = bg_unavailable
            server_info_pane[i].title = ""
            server_info_pane[i].childNodes[2].textContent = "?  "
        }
    }
}

function redrawTableElements(data, callback) {
    let parsedData = JSON.parse(data);

    ///если мониторинг пал
    if (parsedData['ClientConnectionError'] !== undefined)
        monitorUnavailable(document.getElementsByClassName('server'))
    else
        parsedData.forEach(el => updateServerNode(el.hostname, el.data, el.id, callback));

}

async function getMetrics (url, method, callback) {
    let response = await fetch(url, {
        method: method, headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
        }
    });

    let data = await response.json()
    redrawTableElements(data, callback);
}

async function inspectServers() {
    await getMetrics("processes/", "GET", execAnalysis);
    await getMetrics("cpu-info/", "GET", cpuAnalysis);
    await getMetrics("ram-info/", "GET", ramAnalysis);
    await getMetrics("disk-info/", "GET", fileSysAnalysis);

}

// main //
document.onload = async () => await inspectServers()
setInterval(inspectServers, 5000);
// main //