function cpuData(data, host) {
    let connErr = (data[0].cpu_load === undefined) ? "" : 0

    host.childNodes[3].childNodes[1].style.backgroundColor = (connErr !== "") ?
        "#69ff4e" : "#bebdbd"

    host.childNodes[3].childNodes[1].childNodes[2].textContent = (connErr !== "") ?
        `${data[0].cpu_load}%` : "0%"

    host.childNodes[3].childNodes[1].title = (connErr !== "") ?
        `CPU cores: ${data[1].cores}` : ""

}

function processesData(data, host) {
    let connErr = (data[0].status === undefined) ? "" : 0

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

    // TODO: написать полифил для replaceAll

    [processesTooltip, processesCount] = ["".concat(processesArray).replaceAll(',', '\n'),
        processesArray.length];

    //processes
    host.childNodes[3].childNodes[7].title = (connErr !== "") ?
        processesTooltip : "";
    host.childNodes[3].childNodes[7].childNodes[2].textContent = (connErr !== "") ?
        processesCount : 0;
    host.childNodes[3].childNodes[7].style.backgroundColor = (connErr !== "") ?
        "#69ff4e" : "#bebdbd";


}

function updateServerNode(hostname, data, id, callback) {
    let host = document.getElementById(id);

    // set hostname
    let connError = "no connection with server."
    host.childNodes[1].childNodes[1].childNodes[3].textContent = (data[0] !== connError) ?
        hostname : "Хост недоступен\n";

    // set status
    host.childNodes[1].childNodes[3].childNodes[1].src = (data[0] !== connError) ?
        "/static/dashboard/images/icons8-like-64.png" : "/static/dashboard/images/icons8-unlike-64.png";
    host.childNodes[1].childNodes[3].childNodes[2].textContent = (data[0] !== connError) ?
        "UP\n" : "DOWN\n";
    host.childNodes[1].childNodes[3].style.backgroundColor = (data[0] !== connError) ?
        "#69ff4e" : "#ff0000"

    callback(data, host, connError)

}

function monitorUnavailable(servers) {
    let bg_unavailable = "#bebdbd"
    for (let server of servers) {
        // title
        server.childNodes[1].childNodes[1].childNodes[3].textContent = "Агент мониторинга недоступен"
        // status
        server.childNodes[1].childNodes[3].style.backgroundColor = bg_unavailable
        server.childNodes[1].childNodes[3].childNodes[1].src = "/static/dashboard/images/icons8-unlike-64.png"
        server.childNodes[1].childNodes[3].childNodes[2].textContent = "?  "
        // server info
        let server_info_pane = server.childNodes[3].childNodes
        for (let i = 1; i < server_info_pane.length; i += 2) {
            // server_info_pane[i].style.backgroundColor = bg_unavailable
            server_info_pane[i].title = ""
            server_info_pane[i].childNodes[2].textContent = "?  "
        }
    }
}

function reDrawTableElements(data, callback) {
    let parsedData = JSON.parse(data);

    ///если мониторинг пал
    if (parsedData['ClientConnectionError'] !== undefined)
        monitorUnavailable(document.getElementsByClassName('server'))

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
    reDrawTableElements(data, callback);
}

async function inspectServers() {
    await getMetrics("processes/", "GET", processesData);
    await getMetrics("cpu-info/", "GET", cpuData);

}

// main //
document.onload = async () => await inspectServers()
setInterval(inspectServers, 5000);
// main //