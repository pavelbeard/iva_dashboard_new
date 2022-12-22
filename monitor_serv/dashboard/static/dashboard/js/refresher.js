function netAnalysis(data, host) {
    let connErr = (data[0].interface === undefined) ? "" : 0;
    let result = (connErr !== "");

    // status
    host.childNodes[3].childNodes[9].style.backgroundColor = result ? "#69ff4e" : "#ff0000";
    host.childNodes[3].childNodes[9].childNodes[2].textContent = result ? "UP" : "DOWN";

    if (result) {
        //int
        let interface = result ? data[0].interface : "";

        //-5 elems
        let lastFiveElems = data.slice(-5,);
        let allRate = "".concat(lastFiveElems
            .map(el => `last2s: ${Object.values(el)[0].last2s} | last10s: ${Object.values(el)[0].last10s} | last40s: ${Object.values(el)[0].last40s}`))
            .replace(/,/g, '\n');

        let remainingItems = data.slice(1, -5);

        let remainingResult = "".concat(remainingItems.flatMap(el => {
            if (el.from !== undefined) {
                return `from: ${el.from} | last2s: ${el.last2s} | last10s: ${el.last10s} | last40s: ${el.last40s} | cumulative: ${el.cumulative}\n`;
            } else {
                return `to: ${el.to} | last2s: ${el.last2s} | last10s: ${el.last10s} | last40s: ${el.last40s} | cumulative: ${el.cumulative}\n`;
            }
        })).replace(/,/g, "\n");



        host.childNodes[3].childNodes[9].title = `${interface}\n${remainingResult}\n${allRate}`
    }

}


function fileSysAnalysisParts(data, host) {
    let connErr = (data[0].filesystem === undefined) ? "" : 0;
    let result = (connErr !== "");

    //style
    host.childNodes[3].childNodes[5].style.backgroundColor = result ? "#69ff4e" : "#bebdbd";

    // percentage
    let used_percent = result ? data[data.length - 1].used_percent : "";
    host.childNodes[3].childNodes[5].childNodes[2].textContent = result ? `${used_percent}%` : "N/A";

    let total_size = result ? data[data.length - 3].total_size : "";
    let total_used = result ? data[data.length - 2].total_used : "";

    //title
    //filesystem size used available use% mounted on

    if (result) {
        let slicedData = data.slice(0, -3);
        let cols = "".concat(Object.keys(slicedData[0])).replace(/,/g, " | ") + "\n"
        let slicedArray = slicedData
            .map(el => `${el.filesystem} | ${el.size} | ${el.used} | ${el.available} | ${el.use_percent} | ${el.mounted_on}`);

        let title = "".concat(slicedArray).replace(/,/g, "\n");

        host.childNodes[3].childNodes[5].title = `Total size: ${total_size}\nTotal used: ${total_used}\n` + cols + title;
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

    let result = data[0].connection_error === undefined;

    // set hostname
    host.childNodes[1].childNodes[1].childNodes[3].textContent = result  ? hostname : "Хост недоступен\n";

    // server status
    host.childNodes[1].childNodes[1].style.backgroundColor = result ? "#69ff4e" : "#ff0000"
    host.childNodes[1].childNodes[1].childNodes[5].textContent = result ? "UP\n" : "DOWN\n";

    callback(data, host)

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
    setTimeout(getMetrics, 0,"disk-info/", "GET", fileSysAnalysisParts);
    setTimeout(getMetrics, 0,"processes/", "GET", execAnalysis);
    setTimeout(getMetrics, 0,"cpu-info/", "GET", cpuAnalysis);
    setTimeout(getMetrics, 0,"ram-info/", "GET", ramAnalysis);
    setTimeout(getMetrics, 0,"net-info/", "GET", netAnalysis);

    // // TODO: создать очередь задач. Самая первая задача должна быть трудной
    // await getMetrics("processes/", "GET", execAnalysis);
    // await getMetrics("cpu-info/", "GET", cpuAnalysis);
    // await getMetrics("ram-info/", "GET", ramAnalysis);
    // await getMetrics("disk-info/", "GET", fileSysAnalysisParts);
}

// main //
document.onload = async () => await inspectServers();
setInterval(inspectServers, 5000);
// main //