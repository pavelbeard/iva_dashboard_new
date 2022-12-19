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
    [processesTooltip, processesCount] = ["".concat(processesArray).replaceAll(',', '\n'),
        processesArray.length];

    //processes
    host.childNodes[3].childNodes[7].childNodes[2].textContent = (connErr !== "") ?
        processesCount : 0;
    host.childNodes[3].childNodes[7].style.backgroundColor = (connErr !== "") ?
        "#69ff4e" : "#777676";

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

function reDrawTableElements(data, callback) {
    let parsedData = JSON.parse(data);
    parsedData.forEach(el => updateServerNode(el.hostname, el.data, el.id, callback));

    // serversElementsArray.forEach(el => servers.appendChild(el))

    // $('[data-toggle="tooltip"]').tooltip();
}

async function getMetrics (url, method, headers) {
    let response = await fetch(url, {
        method: method, headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
        }
    });

    return await response.json();
}

async function inspectServers() {
    let data = await getMetrics("processes/", "GET");
    reDrawTableElements(data, processesData);
}

// main //
document.onload = async () => await inspectServers()
setInterval(inspectServers, 5000);
// main //