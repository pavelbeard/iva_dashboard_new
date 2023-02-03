import {zip} from "./extensions.js";

function dropdownTitle(hostId, html, cardPart) {
    $(function () {
         $(`div#${hostId}.server`).find(cardPart).hover(function () {
             if ($(`#${hostId}`).attr('data-available') !== "false") {
                 $(this).addClass('show');
                 $(this).find('.dropdown-menu').addClass('show');
                 $(this).find('.dropdown-menu').html(html);
             }
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

    try {
        if (status) {
            host.childNodes[1].childNodes[1].childNodes[7].textContent = data[0]["hostname"]
        } else {
            throw new Error(`Хост ${host.id} недоступен`)
        }
    } catch (e) {
        host.childNodes[1].childNodes[1].childNodes[7].textContent = "Хост недоступен\n";
    }
}

function uptime(data, host) {
    let status = data[0]["uptime"] !== undefined;
    $(`#${host.id}`).attr('data-available', status);

    try {
        if (status) {
            let html = `<li><a class="dropdown-item">${data[0]["uptime"]}</a></li>`;
            dropdownTitle(host.id, html, '.server-img.dropend');
        } else {
            throw new Error(`Хост ${host.id} недоступен`)
        }
    } catch (e) {
        // TODO: logging
    }
}

function netAnalysis(data, host) {
    let status = data[0]["iface"] !== undefined;
    let cmdNotFound = data[0]["command_not_found"] !== undefined;
    $(`#${host.id}`).attr('data-available', status);

    host.childNodes[3].childNodes[9].childNodes[1].src = status ?
        "/static/dashboard/images/dashboard-ethernet-up.svg" :
        cmdNotFound ? "/static/dashboard/images/dashboard-ethernet-down.svg" :
             "/static/dashboard/images/dashboard-ethernet.svg";
    host.childNodes[3].childNodes[9].childNodes[3].childNodes[1].textContent = status ? "UP" : cmdNotFound ? "DOWN" : "N/A" ;

    try {
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
            dropdownTitle(
                host.id,
                  ``.concat(titleInfo).replace(/,/g, ""),
                '.server-network-text.dropend'
            );
        } else {
            throw new Error(`Хост ${host.id} недоступен`)
        }
    } catch (e) {
    }
}


function fileSysAnalysisParts(data, host) {
    let fsIndicatorImage = host.childNodes[3].childNodes[5].childNodes[1];
    let fsIndicatorTextContent = host.childNodes[3].childNodes[5].childNodes[3].childNodes[1];
    let status = data[0]["filesystem"] !== undefined;
    let na = "/static/dashboard/images/dashboard-ssd-card.svg";
    $(`#${host.id}`).attr('data-available', status);

    try {
        if (status) {
            // percentage
            let mostValuablePartUsePercent = data[data.length - 1]["most_valuable_part_use_percent"];

            //style
            let threshold = parseFloat(mostValuablePartUsePercent.slice(0,-1))
            if (threshold > 0.0 && threshold < 50.0) {
                fsIndicatorImage.src =
                    "/static/dashboard/images/dashboard-ssd-card-normal.svg";
            } else if (threshold > 50.0 && threshold < 75.0) {
                fsIndicatorImage.src =
                    "/static/dashboard/images/dashboard-ssd-card-warning.svg";
            } else if (threshold > 75.0 && threshold <= 100.0) {
                fsIndicatorImage.src =
                    "/static/dashboard/images/dashboard-ssd-card-danger.svg";
            }

            let totalDiskSize = data[data.length - 6]["total_disk_size"];
            let mostValuablePartFs = data[data.length - 5]["most_valuable_part_fs"];
            let mostValuablePartSize = data[data.length - 4]["most_valuable_part_size"];
            let mostValuablePartUsed = data[data.length - 3]["most_valuable_part_used"];
            let mostValuablePartAvailable = data[data.length - 2]["most_valuable_part_available"];

            fsIndicatorTextContent.textContent = `${mostValuablePartUsePercent}`;

            //title
            //filesystem size used available use% mounted on

            let slicedData = data.slice(0, -6);
            let htmlCols = "".concat(Object.keys(slicedData[0])).replace(/,/g, " | ")
            let cols = `<li><a class="dropdown-item">${htmlCols}</a></li>`;
            let slicedArray = slicedData.map(el =>
                `<li><a class="dropdown-item">${el["filesystem"]} | ${el["size"]} | ${el["used"]} |` +
                `${el["available"]} | ${el["use_percent"]} | ${el["mounted_on"]}</a></li>`
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
            throw new Error(`Хост ${host.id} недоступен`);
        }
    } catch (e) {
        fsIndicatorImage.src = na;
        fsIndicatorTextContent.textContent = "N/A";
    }
}

function ramAnalysis(data, host) {
    let ramIndicatorImage = host.childNodes[3].childNodes[3].childNodes[1];
    let ramIndicatorTextContent = host.childNodes[3].childNodes[3].childNodes[3].childNodes[1];
    let status = data[0]["ram_util"] !== undefined;
    let na = "/static/dashboard/images/dashboard-ram.svg"
    $(`#${host.id}`).attr('data-available', status);

    try {
        if (status) {
            let threshold = parseFloat(data[0]["ram_util"])
            if (threshold > 0.0 && threshold < 50.0) {
                ramIndicatorImage.src =
                    "/static/dashboard/images/dashboard-ram-normal.svg";
            } else if (threshold > 50.0 && threshold < 75.0) {
                ramIndicatorImage.src =
                    "/static/dashboard/images/dashboard-ram-warning.svg";
            } else if (threshold > 75.0 && threshold <= 100.0) {
                ramIndicatorImage.src =
                    "/static/dashboard/images/dashboard-ram-danger.svg";
            }

            let total = `<li><a class="dropdown-item">Total RAM: ${data[1]["ram_total"]}</a></li>`;
            let free = `<li><a class="dropdown-item">Free RAM: ${data[2]["ram_free"]}</a></li>`;
            let used = `<li><a class="dropdown-item">Used RAM: ${data[3]["ram_used"]}</a></li>`;

            ramIndicatorTextContent.textContent = data[0]["ram_util"].trim() + "%";

            dropdownTitle(host.id, total + free + used, '.server-ram-text.dropend');

        } else {
            throw new Error(`Хост ${host.id} недоступен`);
        }
    } catch (e) {
        ramIndicatorTextContent.textContent = "N/A";
        ramIndicatorImage.src = na;
    }
}

function cpuTopAnalysis(data, host) {
    let cpuIndicator = host.childNodes[3].childNodes[1];
    let cpuIndicatorImage = cpuIndicator.childNodes[1];
    let cpuIndicatorTextContent = host.childNodes[3].childNodes[1].childNodes[3].childNodes[1];
    let status = data[0]["all_cores"] !== undefined;
    let na = "/static/dashboard/images/dashboard-cpu.svg";
    $(`#${host.id}`).attr('data-available', status);


    try {
        if (status) {
            let threshold = parseFloat(data[0]["all_cores"]["cpu_load"]);
            if (threshold > 0.0 && threshold < 50.0) {
                cpuIndicatorImage.src =
                    "/static/dashboard/images/dashboard-cpu-normal.svg";
            } else if (threshold > 50.0 && threshold < 75.0) {
                cpuIndicatorImage.src =
                    "/static/dashboard/images/dashboard-cpu-warning.svg";
            } else if (threshold > 75.0 && threshold <= 100.0) {
                cpuIndicatorImage.src =
                    "/static/dashboard/images/dashboard-cpu-danger.svg";
            }

            cpuIndicatorTextContent.textContent = data[0]["all_cores"]["cpu_load"] + "%";

            let cores = "";

            for (let core = 0; core < data[1]["each_core"].length; core++) {
                cores += `<li><a class="dropdown-item">Core${core}: ${data[1]["each_core"][core][`core${core}`]}%</a></li>`
            }

            dropdownTitle(host.id, cores, '.server-cpu-text.dropend');

        } else {
            throw new Error(`Хост ${host.id} недоступен`);
        }
    } catch (e) {
        cpuIndicatorTextContent.textContent = "N/A";
        cpuIndicatorImage.src = na;
    }
}

function execAnalysis(data, host) {
    let processesIndicator = host.childNodes[3].childNodes[7];
    let processesIndicatorImage = processesIndicator.childNodes[1];
    let processesIndicatorTextContent = processesIndicator.childNodes[3].childNodes[1];
    let status = data[0]["status"] !== undefined;
    $(`#${host.id}`).attr('data-available', status);


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
            processesIndicatorTextContent.textContent = processesCount;
            processesIndicatorImage.src = "/static/dashboard/images/dashboard-apps-normal.svg";

            dropdownTitle(host.id, processesTooltip, '.server-apps-text.dropend');

        } else {
            throw new Error("Хост недоступен.");
        }
    } catch (e) {
        processesIndicatorTextContent.textContent = "N/A";
        processesIndicatorImage.src = "/static/dashboard/images/dashboard-apps.svg";
    }
}

function updateServerNode(data, id, server_role, callback) {
    let host = document.getElementById(id);
    let serverNodeImage = host.childNodes[1].childNodes[1].childNodes[1];
    let serverNodeTextContent = host.childNodes[1].childNodes[1].childNodes[5];
    let err = data[0]["connection_error"] === undefined;

    // server status

    //if server media else server head
    let mediaUp = "/static/dashboard/images/dashboard-server-media-up.svg";
    let mediaDown = "/static/dashboard/images/dashboard-server-media-down.svg";
    let headUp = "/static/dashboard/images/dashboard-server-head-up.svg";
    let headDown = "/static/dashboard/images/dashboard-server-head-down.svg";


    if (server_role === 'media')
        serverNodeImage.src = err ? mediaUp : mediaDown
    else
        serverNodeImage.src = err ? headUp : headDown

    serverNodeTextContent.textContent = err ? "UP\n" : "DOWN\n";

    callback(data, host)

}

function monitorAvailability(servers, reason, available= false) {
    let agentStatus = document.getElementById("agent-status");

    agentStatus.innerHTML = available ? "монитор в норме." : reason
    agentStatus.style.color = available ? "#00ff33AA" : "#ff0033AA";
    let bg = available ? "#ececec" : "#bebdbd";

    let imgArray = [
        "/static/dashboard/images/dashboard-cpu.svg",
        "/static/dashboard/images/dashboard-ram.svg",
        "/static/dashboard/images/dashboard-ssd-card.svg",
        "/static/dashboard/images/dashboard-apps.svg",
        "/static/dashboard/images/dashboard-ethernet.svg",
    ];

    for (let server of servers) {

        if (!available) {

            let serverInfoPane = server.childNodes[1].childNodes[1];
            serverInfoPane.childNodes[3].setAttribute('style', 'white-space: pre;');
            serverInfoPane.childNodes[5].textContent = "no data";
            serverInfoPane.childNodes[7].textContent = "no data";
            serverInfoPane.childNodes[11].textContent = "no data";

            let role = serverInfoPane.childNodes[11].innerHTML === "HEAD";
            let head = "/static/dashboard/images/dashboard-server-head.svg";
            let media = "/static/dashboard/images/dashboard-server-media.svg";
            server.childNodes[1].childNodes[1].childNodes[1].src = role ? head : media;
        }

        // server status
        server.childNodes[1].childNodes[1].style.backgroundColor = bg;

        // server info
        let server_info_pane = server.childNodes[3].childNodes;

        for (let i = 1, img = 0; i < server_info_pane.length; i += 2, img++) {
            // изменяем все индикаторы
            server_info_pane[i].style.backgroundColor = bg;
            if (!available) {
                server_info_pane[i].childNodes[3].childNodes[1].textContent = "N/A";
                server_info_pane[i].childNodes[1].src = imgArray[img];
            }
        }
    }
}

function redrawTableElements(parsedData, callback) {
    // если отсутствует ключ task, то мониторинг пал и
    // ставим дата-атрибут для каждого сервера false - это выключает dropdown
    if (parsedData["task"] === undefined) {
        let servers = $('.server');
        for (let server of servers) {
            $(`#${server.id}`).attr('data-available', false);
        }
    }

    ///если мониторинг пал
    if (parsedData['ClientConnectionError'] !== undefined)
        monitorAvailability(document
            .getElementsByClassName('server'), parsedData['ClientConnectionError']);
    //если конфигурация сервера мониторинга не найдена
    else if (parsedData['DoesNotExist'] !== undefined)
        monitorAvailability(document
            .getElementsByClassName('server'), parsedData['DoesNotExist']);
    //агент не может валидировать данные
    else if (parsedData['ValidationException'] !== undefined)
        monitorAvailability(document
            .getElementsByClassName('server'), parsedData['ValidationException']);
    //таблица с целевыми хостами отсутствует
    else if (parsedData["ProgrammingError"] !== undefined || parsedData['TargetsIsEmpty'] !== undefined)
        monitorAvailability(document
            .getElementsByClassName('server'), parsedData["ProgrammingError"]);
    else {
        monitorAvailability(document
            .getElementsByClassName('server'), "", true);
        parsedData.forEach(el => updateServerNode(el.data, el.id, el.role, callback));
    }

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

    let interval = JSON.parse(await response.json());

    if (interval['DoesNotExist'] === undefined)
        return  parseInt(interval.interval) * 1000;
    else
        return 5000;
}

async function inspectServers() {

    let funcArray = [
        hostnamectl, cpuTopAnalysis, ramAnalysis, fileSysAnalysisParts,
        execAnalysis, netAnalysis, uptime
    ];

    funcArray.forEach(func => setTimeout(
        getMetrics, 0, func.name.toLocaleLowerCase() + "/", "GET", headers, func))

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