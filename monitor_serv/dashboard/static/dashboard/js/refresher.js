import {zip} from "./extensions.js";

function uptime(data, host) {
    let status = data[0]["uptime"] !== undefined;

    host.childNodes[1].title = status ? data[0]["uptime"] : "";
}

// TODO: Переедет в файл уровня детализации
function netAnalysisDetail(data, host) {
    let status = data[0]["interface"] !== undefined;
    let cmdNotFound = data[0]["command_not_found"] !== undefined

    // status

    host.childNodes[3].childNodes[9].style.backgroundColor = status ? "#69ff4e" : cmdNotFound ? "#ff0000" : "#bebdbd";
    host.childNodes[3].childNodes[9].childNodes[2].textContent = status ? "UP" : cmdNotFound ? "DOWN" : "iftop n/a";

    if (status) {
        //int
        let iface = status ? data[0]["interface"] : "";

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

function netAnalysis(data, host) {
    let status = data[0]["iface"] !== undefined
    let cmdNotFound = data[0]["command_not_found"] !== undefined


    host.childNodes[3].childNodes[9].childNodes[1].src = status ?
        "/static/dashboard/images/dashboard-ethernet-up.svg" :
        cmdNotFound ? "/static/dashboard/images/dashboard-ethernet-down.svg" :
             "/static/dashboard/images/dashboard-ethernet.svg";
    host.childNodes[3].childNodes[9].childNodes[2].textContent = status ? "UP" : cmdNotFound ? "DOWN" : "N/A" ;

    if (status) {
        let ifaces = data.map(i => `interface: ${i["iface"]} - status: ${i["status"]}\n`);
        let ipAddresses = data.map(i => `ip address: ${i["ipaddress"]}\n`);
        let rxBytes = data.map(i => `RX bytes: ${i["rx_bytes"]}\n`);
        let rxPackets = data.map(i => `RX packets: ${i["rx_packets"]}\n`);
        let rxErrors = data.map(i => `RX errors: ${Object.entries(i["rx_errors"])}\n`)
            .map(i => i.replace(/,(?!\d+)/g, ' | ').replace(/,(?=\d+)/g, '='))
        let txBytes = data.map(i => `TX bytes: ${i["tx_bytes"]}\n`);
        let txPackets = data.map(i => `TX packets: ${i["tx_packets"]}\n`);
        let txErrors = data.map(i => `TX errors: ${Object.entries(i["tx_errors"])}\n\n`)
            .map(i => i.replace(/,(?!\d+)/g, ' | ').replace(/,(?=\d+)/g, '='))

        let titleInfo = [...zip(ifaces, ipAddresses, rxBytes, rxPackets, rxErrors, txBytes, txPackets, txErrors)];

        host.childNodes[3].childNodes[9].title = "".concat(titleInfo).replace(/,/g, "");
    } else {
        host.childNodes[3].childNodes[9].title = ""
    }

}


function fileSysAnalysisParts(data, host) {
    let err = data[0].filesystem !== undefined

    // percentage
    let mostValuablePartUsePercent = err ? data[data.length - 1]["most_valuable_part_use_percent"] : "";

    //style
    let na = "/static/dashboard/images/dashboard-ssd-card.svg"
    try {
        let threshold = parseFloat(mostValuablePartUsePercent.slice(0,-1))
        if (threshold > 0.0 && threshold < 50.0) {
            host.childNodes[3].childNodes[5].childNodes[1].src =
                "/static/dashboard/images/dashboard-ssd-card-normal.svg";
        } else if (threshold > 50.0 && threshold < 75.0) {
            host.childNodes[3].childNodes[5].childNodes[1].src =
                "/static/dashboard/images/dashboard-ssd-card-warning.svg";
        } else if (threshold > 75.0 && threshold <= 100.0) {
            host.childNodes[3].childNodes[5].childNodes[1].src =
                "/static/dashboard/images/dashboard-ssd-card-danger.svg";
        } else if (!err) {
            throw new Error("N/A");
        }
    } catch (e) {
        host.childNodes[3].childNodes[5].childNodes[1].src = na;
        console.log(e);
    }

    let totalDiskSize = err ? data[data.length - 6]["total_disk_size"] : "";
    let mostValuablePartFs = err ? data[data.length - 5]["most_valuable_part_fs"] : "";
    let mostValuablePartSize = err ? data[data.length - 4]["most_valuable_part_size"] : "";
    let mostValuablePartUsed = err ? data[data.length - 3]["most_valuable_part_used"] : "";
    let mostValuablePartAvailable = err ? data[data.length - 2]["most_valuable_part_available"] : "";


    host.childNodes[3].childNodes[5].childNodes[2].textContent = err ? `${mostValuablePartUsePercent}` : "N/A";

    //title
    //filesystem size used available use% mounted on

    if (err) {
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
    let err = data[0]["ram_util"] !== undefined;

    let na = "/static/dashboard/images/dashboard-ram.svg"
    try {
        let threshold = parseFloat(data[0]["ram_util"])
        if (threshold > 0.0 && threshold < 50.0) {
            host.childNodes[3].childNodes[3].childNodes[1].src =
                "/static/dashboard/images/dashboard-ram-normal.svg";
        } else if (threshold > 50.0 && threshold < 75.0) {
            host.childNodes[3].childNodes[3].childNodes[1].src =
                "/static/dashboard/images/dashboard-ram-warning.svg";
        } else if (threshold > 75.0 && threshold <= 100.0) {
            host.childNodes[3].childNodes[3].childNodes[1].src =
                "/static/dashboard/images/dashboard-ram-danger.svg";
        } else if (!err) {
            throw new Error("N/A");
        }
    } catch (e) {
        host.childNodes[3].childNodes[3].childNodes[1].src = na;
        console.log(e)
    }


    host.childNodes[3].childNodes[3].childNodes[2].textContent = err ? `${data[0]["ram_util"]}%` : "N/A";

    let total = err ? data[1]["ram_total"].trim() : "";
    let free = err ? data[2]["ram_free"].trim() : "";
    let used = err ? data[3]["ram_used"].trim() : "";

    host.childNodes[3].childNodes[3]
        .title = err ? `Total RAM: ${total}GB\nFree RAM: ${free}GB\nUsed RAM: ${used}GB` : ""
}

function cpuAnalysis(data, host) {
    let err = data[0]["cpu_load"] !== undefined;

    let na = "/static/dashboard/images/dashboard-cpu.svg"
    try {
        let threshold = parseFloat(data[0]["cpu_load"]);
        if (threshold > 0.0 && threshold < 50.0) {
            host.childNodes[3].childNodes[1].childNodes[1].src =
                "/static/dashboard/images/dashboard-cpu-normal.svg";
        } else if (threshold > 50.0 && threshold < 75.0) {
            host.childNodes[3].childNodes[1].childNodes[1].src =
                "/static/dashboard/images/dashboard-cpu-warning.svg";
        } else if (threshold > 75.0 && threshold <= 100.0) {
            host.childNodes[3].childNodes[1].childNodes[1].src =
                "/static/dashboard/images/dashboard-cpu-danger.svg";
        } else if (!err) {
            throw new Error("N/A");
        }
    } catch (e) {
        host.childNodes[3].childNodes[1].childNodes[1].src = na;
        console.log(e)
    }

    host.childNodes[3].childNodes[1].childNodes[2].textContent = err ? `${data[0]["cpu_load"]}%` : "N/A";

    //вывод всех ядер и количества ядер
    let core = 0
    let cores  = err ? "".concat(data.slice(2, -1).map(el => `Core ${core++}: ${Object.values(el)[0]}%`))
        .replace( /,/g, '\n') : "";

    host.childNodes[3].childNodes[1]
        .title = err ? `CPU idle: ${data[1]["cpu_idle"]}%\nCPU cores: ${data[data.length - 1]["cpu_cores"]}\n`
        + cores  : "";

}

function execAnalysis(data, host) {
    let err = data[0]["status"] !== undefined;

    let processesArray = data.map(el => {
        let st = ''
        switch (el["status"]) {
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
        return `${el["service"]}: ${el["status"]}${st}`;
    });
    let processesTooltip, processesCount;

    [processesTooltip, processesCount] = ["".concat(processesArray).replace(/,/g, '\n'),
        processesArray.length];

    //processes
    host.childNodes[3].childNodes[7].title = err ? processesTooltip : "";
    host.childNodes[3].childNodes[7].childNodes[1].src =
        err ? "/static/dashboard/images/dashboard-apps-normal.svg" :
            "/static/dashboard/images/dashboard-apps.svg";
    host.childNodes[3].childNodes[7].childNodes[2].textContent = err ? processesCount : 0;


}

function updateServerNode(hostname, data, id, server_role, callback) {
    let host = document.getElementById(id);

    let err = data[0]["connection_error"] === undefined;

    // set hostname
    host.childNodes[1].childNodes[1].childNodes[3].textContent = err  ? hostname : "Хост недоступен\n";

    // server status

    //if server media else server head

    if (server_role === 'media') {
        host.childNodes[1].childNodes[1].childNodes[1].src = err ?
            "/static/dashboard/images/dashboard-server-media-up.svg" :
            "/static/dashboard/images/dashboard-server-media-down.svg"
    } else {
        host.childNodes[1].childNodes[1].childNodes[1].src = err ?
            "/static/dashboard/images/dashboard-server-head-up.svg" :
            "/static/dashboard/images/dashboard-server-head-down.svg"
    }
    host.childNodes[1].childNodes[1].childNodes[5].textContent = err ? "UP\n" : "DOWN\n";

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

function redrawTableElements(parsedData, callback) {
    ///если мониторинг пал
    if (parsedData['ClientConnectionError'] !== undefined)
        monitorUnavailable(document
            .getElementsByClassName('server'), 'Агент мониторинга\r\nнедоступен!')
    //если конфигурация сервера мониторинга не найдена
    else if (parsedData['FileNotFoundError'] !== undefined)
        monitorUnavailable(document
            .getElementsByClassName('server'), 'Файл конфигурации\r\nинфопанели не найден!')
    //агент не может валидировать данные
    else if (parsedData['ValidationException'] !== undefined)
        monitorUnavailable(document
            .getElementsByClassName('server'), 'Агент не распознал\r\nданные!')
    //таблица с целевыми хостами отсутствует
    else if (parsedData["ProgrammingError"] !== undefined || parsedData['TargetsIsEmpty'] !== undefined)
        monitorUnavailable(document
            .getElementsByClassName('server'), 'Целевые хосты\r\nне найдены!')
    else
        parsedData.forEach(el => updateServerNode(el.hostname, el.data, el.id, el.role, callback));

}

let headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
}

async function getMetrics (url, method, headers, callback) {
    let response = await fetch(url, {
        method: method, headers: headers
    });

    let data = await response.json()
    let parsedData = JSON.parse(data);

    if (callback !== undefined)
        redrawTableElements(parsedData, callback);
}

async function getInterval(url, method, headers) {
    let response = await fetch(url, {
        method: method, headers: headers
    });

    let int = JSON.parse(await response.json());

    if (int['file_not_found'] === undefined)
        return  parseInt(int.interval) * 1000;
    else
        return 5000;
}

async function inspectServers() {
    setTimeout(getMetrics, 0,"cpu-info/", "GET", headers, cpuAnalysis);
    setTimeout(getMetrics, 0,"ram-info/", "GET", headers, ramAnalysis);
    setTimeout(getMetrics, 0,"disk-info/", "GET", headers, fileSysAnalysisParts);
    setTimeout(getMetrics, 0,"processes/", "GET", headers, execAnalysis);
    setTimeout(getMetrics, 0,"net-info/", "GET", headers, netAnalysis);
    setTimeout(getMetrics, 0,"uptime/", "GET", headers, uptime);

    // TODO: создать новый js файл для чисто iva-утилит
    // TODO: переписать в функциях часть кода, отвечающий за обработку ошибок в промисы
}

// main //
setTimeout(async function () {
    await inspectServers();
    setTimeout(getMetrics, 0, 'dal/hostnamectl/', "GET")
    let interval = await getInterval("interval/", "GET", headers);
    setInterval(inspectServers, interval);
}, 0);
// main //