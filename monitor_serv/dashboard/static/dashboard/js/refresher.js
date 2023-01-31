import {zip} from "./extensions.js";

function dropdownTitle(hostId, html, cardPart) {
    $(document).ready(function () {
        $(`div#${hostId}.server`).find(cardPart).hover(function () {
            $(this).addClass('show');
            $(this).find('.dropdown-menu').addClass('show');
            $(this).find('.dropdown-menu').html(html);
        }, function () {
            $(this).removeClass('show');
            $(this).find('.dropdown-menu').removeClass('show');
            $(this).find('.dropdown-menu').empty()
        });
    });
}

function hostnamectl(data, host) {
    let status = data[0]["hostname"] !== undefined;
    // set hostname
    host.childNodes[1].childNodes[1].childNodes[7].textContent = status  ? data[0]["hostname"] : "Хост недоступен\n";
}

function uptime(data, host) {
    let status = data[0]["uptime"] !== undefined;

    if (status) {
        let html = `<li><a class="dropdown-item">${data[0]["uptime"]}</a></li>`;
        dropdownTitle(host.id, html, '.server-img.dropend');
    }
}

function netAnalysis(data, host) {
    let status = data[0]["iface"] !== undefined
    let cmdNotFound = data[0]["command_not_found"] !== undefined

    host.childNodes[3].childNodes[9].childNodes[1].src = status ?
        "/static/dashboard/images/dashboard-ethernet-up.svg" :
        cmdNotFound ? "/static/dashboard/images/dashboard-ethernet-down.svg" :
             "/static/dashboard/images/dashboard-ethernet.svg";
    host.childNodes[3].childNodes[9].childNodes[3].childNodes[1].textContent = status ? "UP" : cmdNotFound ? "DOWN" : "N/A" ;

    if (status) {
        let ifaces =
            data.map(i => `<li><a class="dropdown-item">interface: ${i["iface"]} - status: ${i["status"]}</a></li>`);
        let ipAddresses =
            data.map(i => `<li><a class="dropdown-item">ip address: ${i["ipaddress"]}</a></li>`);
        let rxBytes =
            data.map(i => `<li><a class="dropdown-item">RX bytes: ${i["rx_bytes"]}</a></li>`);
        let rxPackets =
            data.map(i => `<li><a class="dropdown-item">RX packets: ${i["rx_packets"]}</a></li>`);
        let rxErrors = data.map(i =>
            `<li><a class="dropdown-item">RX errors: ${Object.entries(i["rx_errors"])}</a></li>`
        ).map(
            i => i.replace(/,(?!\d+)/g, ' | ').replace(/,(?=\d+)/g, '=')
        );
        let txBytes = data.map(i =>
            `<li><a class="dropdown-item">TX bytes: ${i["tx_bytes"]}</a> </li>`
        );
        let txPackets = data.map(i =>
            `<li><a class="dropdown-item">TX packets: ${i["tx_packets"]}</a></li>`
        );
        let divider =  `<li><hr class="dropdown-divider"></li>`;
        let txErrors = data.map(i =>
            `<li><a class="dropdown-item">TX errors: ${Object.entries(i["tx_errors"])}</a></li>${divider}`
        ).map(i => i.replace(/,(?!\d+)/g, ' | ').replace(/,(?=\d+)/g, '='));

        let titleInfo = [...zip(ifaces, ipAddresses, rxBytes, rxPackets, rxErrors, txBytes, txPackets, txErrors)];

        // host.childNodes[3].childNodes[9].title = "".concat(titleInfo).replace(/,/g, "");
        dropdownTitle(
            host.id, ``.concat(titleInfo).replace(/,/g, ""),
            '.server-network-text.dropend')
    }
}


function fileSysAnalysisParts(data, host) {
    let status = data[0]["filesystem"] !== undefined;
    let na = "/static/dashboard/images/dashboard-ssd-card.svg"

    try {
        if (status) {
            // percentage
            let mostValuablePartUsePercent = data[data.length - 1]["most_valuable_part_use_percent"];

            //style
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
            }

            let totalDiskSize = data[data.length - 6]["total_disk_size"];
            let mostValuablePartFs = data[data.length - 5]["most_valuable_part_fs"];
            let mostValuablePartSize = data[data.length - 4]["most_valuable_part_size"];
            let mostValuablePartUsed = data[data.length - 3]["most_valuable_part_used"];
            let mostValuablePartAvailable = data[data.length - 2]["most_valuable_part_available"];

            host.childNodes[3].childNodes[5].childNodes[3].childNodes[1].textContent = `${mostValuablePartUsePercent}`;

            //title
            //filesystem size used available use% mounted on

            let slicedData = data.slice(0, -6);
            let htmlCols = "".concat(Object.keys(slicedData[0])).replace(/,/g, " | ")
            let cols = `<li><a class="dropdown-item">${htmlCols}</a></li>`;
            let slicedArray = slicedData.map(el =>
                `<li><a class="dropdown-item">${el.filesystem} | ${el.size} | ${el.used} | ${el.available} | ${el.use_percent} | ${el.mounted_on}</a></li>`
            )
            let htmlTitle = "".concat(slicedArray).replace(/,/g, "");
            let title = `<li><a class="dropdown-item">${htmlTitle}</a></li>`

            let html = `
                <li><a class="dropdown-item">Total disk size: ${totalDiskSize}</a></li>
                <li><a class="dropdown-item">MVP Fs: ${mostValuablePartFs}</a></li>
                <li><a class="dropdown-item">${mostValuablePartFs} size: ${mostValuablePartSize}</a></li>
                <li><a class="dropdown-item">${mostValuablePartFs} size used: ${mostValuablePartUsed}</a></li>
                <li><a class="dropdown-item">${mostValuablePartFs} size available: ${mostValuablePartAvailable}</a></li>
                <li><a class="dropdown-item">${mostValuablePartFs} size use in %: ${mostValuablePartUsePercent}</a></li>
            ` + cols + title;

            dropdownTitle(host.id, html, '.server-disk-text.dropend');

        } else {
            throw new Error("N/A");
        }
    } catch (e) {
        host.childNodes[3].childNodes[5].childNodes[1].src = na;
        host.childNodes[3].childNodes[5].childNodes[3].childNodes[1].textContent = "N/A";
        console.log(e);
    }
}

function ramAnalysis(data, host) {
    let status = data[0]["ram_util"] !== undefined;
    let na = "/static/dashboard/images/dashboard-ram.svg"

    try {
        if (status) {
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
            }

            let total = `<li><a class="dropdown-item">Total RAM: ${data[1]["ram_total"].trim()}GB</a></li>`;
            let free = `<li><a class="dropdown-item">Free RAM: ${data[2]["ram_free"].trim()}GB</a></li>`;
            let used = `<li><a class="dropdown-item">Used RAM: ${data[3]["ram_used"].trim()}GB</a></li>`;

            host.childNodes[3].childNodes[3].childNodes[3].childNodes[1].textContent = data[0]["ram_util"].trim() + "%";

            dropdownTitle(host.id, total + free + used, '.server-ram-text.dropend');

        } else {
            throw new Error("N/A");
        }
    } catch (e) {
        host.childNodes[3].childNodes[3].childNodes[1].src = na;
        console.log(e);
    }
}

function cpuTopAnalysis(data, host) {
    let status = data[0]["all_cores"] !== undefined;
    let na = "/static/dashboard/images/dashboard-cpu.svg";

    try {
        if (status) {
            let threshold = parseFloat(data[0]["all_cores"]["cpu_load"]);
            if (threshold > 0.0 && threshold < 50.0) {
                host.childNodes[3].childNodes[1].childNodes[1].src =
                    "/static/dashboard/images/dashboard-cpu-normal.svg";
            } else if (threshold > 50.0 && threshold < 75.0) {
                host.childNodes[3].childNodes[1].childNodes[1].src =
                    "/static/dashboard/images/dashboard-cpu-warning.svg";
            } else if (threshold > 75.0 && threshold <= 100.0) {
                host.childNodes[3].childNodes[1].childNodes[1].src =
                    "/static/dashboard/images/dashboard-cpu-danger.svg";
            }

            host.childNodes[3].childNodes[1].childNodes[3].childNodes[1].textContent = data[0]["all_cores"]["cpu_load"] + "%";

            let cores = "";

            for (let core = 0; core < data[1]["each_core"].length; core++) {
                cores += `<li><a class="dropdown-item">Core${core}: ${data[1]["each_core"][core][`core${core}`]}%</a></li>`
            }

            dropdownTitle(host.id, cores, '.server-cpu-text.dropend')

        } else {
            throw new Error("N/A");
        }
    } catch (e) {
        host.childNodes[3].childNodes[1].childNodes[2].textContent = "N/A";
        host.childNodes[3].childNodes[1].childNodes[1].src = na;
        console.log(e)
    }


}

function execAnalysis(data, host) {
    let status = data[0]["status"] !== undefined;

    try {
        if (status) {
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
                return `<li><a class="dropdown-item">${el["service"]}: ${el["status"]}${st}</a></li>`;
            });

            let processesTooltip, processesCount;

            [processesTooltip, processesCount] = ["".concat(processesArray).replace(/,/g, '\n'),
                processesArray.length];

            //processes
            host.childNodes[3].childNodes[7].childNodes[3].childNodes[1].textContent = processesCount;
            host.childNodes[3].childNodes[7].childNodes[1].src = "/static/dashboard/images/dashboard-apps-normal.svg";

            dropdownTitle(host.id, processesTooltip, '.server-apps-text.dropend')

        } else {
            throw new Error("N/A");
        }
    } catch (e) {
        host.childNodes[3].childNodes[7].childNodes[3].childNodes[1].textContent = 0;
        host.childNodes[3].childNodes[7].childNodes[1].src = "/static/dashboard/images/dashboard-apps.svg";
    }
}

function updateServerNode(data, id, server_role, callback) {
    let host = document.getElementById(id);
    let err = data[0]["connection_error"] === undefined;

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
        server.childNodes[1].childNodes[1].childNodes[7].textContent = "no data"
        // server status
        server.childNodes[1].childNodes[1].style.backgroundColor = bg_unavailable

        // server info
        let server_info_pane = server.childNodes[3].childNodes
        for (let i = 1; i < server_info_pane.length; i += 2) {
            // изменяем все индикаторы
            server_info_pane[i].style.backgroundColor = bg_unavailable
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
        parsedData.forEach(el => updateServerNode(el.data, el.id, el.role, callback));

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
    setTimeout(getMetrics, 0,"hostnamectl/", "GET", headers, hostnamectl)
    setTimeout(getMetrics, 0,"cpu-top-info/", "GET", headers, cpuTopAnalysis);
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
    let interval = await getInterval("interval/", "GET", headers);
    setInterval(inspectServers, interval);
}, 0);
// main //