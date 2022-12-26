function uptime(data, host) {
    let connErr = data[0].uptime === undefined ? "" : 0;
    let result = connErr !== "";

    host.childNodes[1].title = result ? data[0].uptime : "";
}

function netAnalysis(data, host) {
    let connErr = (data[0].interface === undefined) ? "" : 0;
    let result = (connErr !== "");

    // status
    if (data[0].command_not_found === undefined) {
        host.childNodes[3].childNodes[9].style.backgroundColor = result ? "#69ff4e" : "#ff0000";
        host.childNodes[3].childNodes[9].childNodes[2].textContent = result ? "UP" : "DOWN";
    } else {
        host.childNodes[3].childNodes[9].style.backgroundColor = "#bebdbd";
        host.childNodes[3].childNodes[9].childNodes[2].textContent = "iftop n/f";
    }

    if (result) {
        //int
        let iface = result ? data[0].interface : "";

        //-5 elems
        let lastFiveElems = data.slice(-5,);
        let allRate = "".concat(lastFiveElems
            .map(el => `${Object.keys(el)[0]}: last2s: ${Object.values(el)[0].last2s} | last10s: ${Object.values(el)[0].last10s} | last40s: ${Object.values(el)[0].last40s}`))
            .replace(/,/g, '\n');

        let remainingItems = data.slice(1, -5);

        let remainingResult = "".concat(remainingItems.flatMap(el => {
            if (el.from !== undefined) {
                return `from: ${el.from} | last2s: ${el.last2s} | last10s: ${el.last10s} | last40s: ${el.last40s} | cumulative: ${el.cumulative}\n`;
            } else {
                return `to: ${el.to} | last2s: ${el.last2s} | last10s: ${el.last10s} | last40s: ${el.last40s} | cumulative: ${el.cumulative}\n`;
            }
        })).replace(/,/g, "\n");

        host.childNodes[3].childNodes[9].title = `${iface}\n${remainingResult}\n${allRate}`
    }

}


function fileSysAnalysisParts(data, host) {
    let connErr = (data[0].filesystem === undefined) ? "" : 0;
    let result = (connErr !== "");

    //style
    host.childNodes[3].childNodes[5].style.backgroundColor = result ? "#69ff4e" : "#bebdbd";

    let totalDiskSize = result ? data[data.length - 6]["total_disk_size"] : "";
    let mostValuablePartFs = result ? data[data.length - 5]["most_valuable_part_fs"] : "";
    let mostValuablePartSize = result ? data[data.length - 4]["most_valuable_part_size"] : "";
    let mostValuablePartUsed = result ? data[data.length - 3]["most_valuable_part_used"] : "";
    let mostValuablePartAvailable = result ? data[data.length - 2]["most_valuable_part_available"] : "";

    // percentage
    let mostValuablePartUsePercent = result ? data[data.length - 1]["most_valuable_part_use_percent"] : "";

    host.childNodes[3].childNodes[5].childNodes[2].textContent = result ? `${mostValuablePartUsePercent}` : "N/A";

    //title
    //filesystem size used available use% mounted on

    if (result) {
        let slicedData = data.slice(0, -6);
        let cols = "".concat(Object.keys(slicedData[0])).replace(/,/g, " | ") + "\n"
        let slicedArray = slicedData
            .map(el => `${el.filesystem} | ${el.size} | ${el.used} | ${el.available} | ${el.use_percent} | ${el.mounted_on}`);

        let title = "".concat(slicedArray).replace(/,/g, "\n");

        host.childNodes[3].childNodes[5].title =
            `Total disk size: ${totalDiskSize}\n` +
            `MVP fs: ${mostValuablePartFs}\n` +
            `${mostValuablePartFs} size: ${mostValuablePartSize}\n` +
            `${mostValuablePartFs} size used: ${mostValuablePartUsed}\n` +
            `${mostValuablePartFs} size available: ${mostValuablePartAvailable}\n` +
            `${mostValuablePartFs} size use in %: ${mostValuablePartUsePercent}\n\n` +
            cols + title;
    } else {
        host.childNodes[3].childNodes[5].title = "";
    }

}

function ramAnalysis(data, host) {
    let connErr = (data[0].ram_util === undefined) ? "" : 0;
    let result = (connErr !== "");

    host.childNodes[3].childNodes[3].style.backgroundColor = result ? "#69ff4e" : "#bebdbd";
    host.childNodes[3].childNodes[3].childNodes[2].textContent = result ? `${data[0].ram_util}%` : "N/A";

    let total = result ? data[1].ram_total.trim() : "";
    let free = result ? data[2].ram_free.trim() : "";
    let used = result ? data[3].ram_used.trim() : "";

    host.childNodes[3].childNodes[3]
        .title = result ? `Total RAM: ${total}GB\nFree RAM: ${free}GB\nUsed RAM: ${used}GB` : ""
}

function cpuAnalysis(data, host) {
    let connErr = (data[0].cpu_load === undefined) ? "" : 0;
    let result = (connErr !== "");

    host.childNodes[3].childNodes[1].style.backgroundColor = result ? "#69ff4e" : "#bebdbd";
    host.childNodes[3].childNodes[1].childNodes[2].textContent = result ? `${data[0].cpu_load}%` : "N/A";

    //вывод всех ядер и количества ядер
    let core = 0
    let cores  = result ? "".concat(data.slice(2, -1).map(el => `Core ${core++}: ${Object.values(el)[0]}%`))
        .replace( /,/g, '\n') : "";

    host.childNodes[3].childNodes[1]
        .title = result ? `CPU idle: ${data[1].cpu_idle}%\nCPU cores: ${data[data.length - 1].cpu_cores}\n`
        + cores  : "";

}

function execAnalysis(data, host) {
    let connErr = (data[0].status === undefined) ? "" : 0;
    let result = (connErr !== "");

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

    let result = data[0].connection_error === undefined;

    // set hostname
    host.childNodes[1].childNodes[1].childNodes[3].textContent = result  ? hostname : "Хост недоступен\n";

    // server status
    host.childNodes[1].childNodes[1].style.backgroundColor = result ? "#69ff4e" : "#ff0000"
    host.childNodes[1].childNodes[1].childNodes[5].textContent = result ? "UP\n" : "DOWN\n";

    callback(data, host)

}

function monitorUnavailable(servers, reason) {
    let bg_unavailable = "#bebdbd"
    for (let server of servers) {
        // title
        server.childNodes[1].childNodes[1].childNodes[3].setAttribute('style', 'white-space: pre;')
        server.childNodes[1].childNodes[1].childNodes[3].textContent = reason
        server.childNodes[1].childNodes[1].childNodes[5].textContent = "no data"
        // server status
        server.childNodes[1].childNodes[1].style.backgroundColor = bg_unavailable
        //
        // server.childNodes[1].childNodes[3].childNodes[1].src = "/static/dashboard/images/icons8-unlike-64.png"
        // server.childNodes[1].childNodes[3].childNodes[2].textContent = "?  "
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
        monitorUnavailable(document
            .getElementsByClassName('server'), 'Агент мониторинга\r\nнедоступен')
    else if (parsedData['FileNotFoundError'] !== undefined)
        monitorUnavailable(document
            .getElementsByClassName('server'), 'Файл конфигурации\r\nинфопанели не найден')
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
    setTimeout(getMetrics, 0,"disk-info/", "GET", fileSysAnalysisParts);
    setTimeout(getMetrics, 0,"processes/", "GET", execAnalysis);
    setTimeout(getMetrics, 0,"cpu-info/", "GET", cpuAnalysis);
    setTimeout(getMetrics, 0,"ram-info/", "GET", ramAnalysis);
    setTimeout(getMetrics, 0,"net-info/", "GET", netAnalysis);
    setTimeout(getMetrics, 0,"uptime/", "GET", uptime);

    // TODO: создать новый js файл для чисто iva-утилит
}

// main //
document.onload = async () => await inspectServers();
setInterval(inspectServers, 5000);
// main //