import {zip} from "./extensions.js";

let imagesPath = "/static/dashboard/images";


function dropdownTitle(hostElem, html, cardPart) {
    $(function () {
         hostElem.find(cardPart).hover(function () {
             if (hostElem.attr('data-available') !== "false") {
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

function hostnamectl(data, hostElem) {
    let status = data[0]["hostname"] !== undefined;
    // set hostname

    try {
        if (status) {
            hostElem.find('.server-hostname').text(data[0]["hostname"]);
        } else {
            throw new Error(`Хост ${hostElem.id} недоступен`)
        }
    } catch (e) {
        hostElem.find('.server-hostname').text("Хост недоступен");
    }
}

function uptime(data, hostElem) {
    let status = data[0]["uptime"] !== undefined;
    hostElem.attr('data-available', status);

    try {
        if (status) {
            let html = `
                <li><a class="dropdown-item">${data[0]["uptime"]}</a></li>
            `;
            dropdownTitle(hostElem, html, '.server-img.dropend');
        } else {
            throw new Error(`Хост ${hostElem.id} недоступен`)
        }
    } catch (e) {
        // TODO: logging
    }
}

function netAnalysis(data, hostElem) {
    let status = data[0]["iface"] !== undefined;
    let cmdNotFound = data[0]["command_not_found"] !== undefined;

    // для dropdown-menu
    hostElem.attr('data-available', status);

    let src = imagesPath + (status ? "/bootstrap-svg/ethernet-n.svg" :
        cmdNotFound ? "/bootstrap-svg/ethernet-d.svg" : "/bootstrap-svg/ethernet.svg");

    // status
    hostElem.find('[data-indicator-type="network"]').attr('src', src);
    hostElem.find('.server-network-text').find('p').text(status ? "UP" : cmdNotFound ? "DOWN" : "N/A");

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
            let divider = `<li><hr class="dropdown-divider"></li>`;
            let txErrors = data.map(i =>
                `<li><a class="dropdown-item">TX errors: ${Object.entries(i["tx_errors"])}</a></li>${divider}`
            ).map(i => i.replace(/,(?!\d+)/g, ' | ').replace(/,(?=\d+)/g, '='));

            let titleInfo = [...zip(ifaces, ipAddresses, rxBytes, rxPackets, rxErrors, txBytes, txPackets, txErrors)];
            dropdownTitle(
                hostElem,
                ``.concat(titleInfo).replace(/,/g, ""),
                '.server-network-text.dropend'
            );
        } else if(cmdNotFound) {
            dropdownTitle(
                hostElem, '<li>' +
                '<a class="dropdown-item">Команда ifconfig не найдена. Установите net-tools!</a></li>',
                '.server-network-text.dropend'
            )
        } else {
            throw new Error(`Хост ${hostElem.id} недоступен`)
        }
    } catch (e) {
    }
}


function fileSysAnalysisParts(data, hostElem) {
    let fsIndicatorImage = hostElem.find('[data-indicator-type="disk"]');
    let fsIndicatorTextContent = hostElem.find('.server-disk-text').find('p');
    let status = data[0]["filesystem"] !== undefined;
    let na = imagesPath + "/bootstrap-svg/device-ssd.svg";

    // dropdown menu
    hostElem.attr('data-available', status);

    try {
        if (status) {
            // percentage
            let mostValuablePartUsePercent = data[data.length - 1]["most_valuable_part_use_percent"];

            //style
            let threshold = parseFloat(mostValuablePartUsePercent.slice(0,-1))
            if (threshold > 0.0 && threshold < 50.0) {
                fsIndicatorImage.attr('src', imagesPath + "/bootstrap-svg/device-ssd-n.svg");
            } else if (threshold > 50.0 && threshold < 75.0) {
                fsIndicatorImage.attr('src', imagesPath + "/bootstrap-svg/device-ssd-w.svg");
            } else if (threshold > 75.0 && threshold <= 100.0) {
                fsIndicatorImage.attr('src', imagesPath + "/bootstrap-svg/device-ssd-d.svg");
            }

            let totalDiskSize = data[data.length - 6]["total_disk_size"];
            let mostValuablePartFs = data[data.length - 5]["most_valuable_part_fs"];
            let mostValuablePartSize = data[data.length - 4]["most_valuable_part_size"];
            let mostValuablePartUsed = data[data.length - 3]["most_valuable_part_used"];
            let mostValuablePartAvailable = data[data.length - 2]["most_valuable_part_available"];

            fsIndicatorTextContent.text(mostValuablePartUsePercent);

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

            dropdownTitle(hostElem, html, '.server-disk-text.dropend');

        } else {
            throw new Error(`Хост ${hostElem.id} недоступен`);
        }
    } catch (e) {
        fsIndicatorImage.attr('src', na);
        fsIndicatorTextContent.text("N/A");
    }
}

function ramAnalysis(data, hostElem) {
    let ramIndicatorImage = hostElem.find('[data-indicator-type="ram"]');
    let ramIndicatorTextContent = hostElem.find('.server-ram-text').find('p');
    let status = data[0]["ram_util"] !== undefined;
    let na = imagesPath + "/bootstrap-svg/memory.svg"

    // dropdown menu
    hostElem.attr('data-available', status);

    try {
        if (status) {
            let threshold = parseFloat(data[0]["ram_util"])
            if (threshold > 0.0 && threshold < 50.0) {
                ramIndicatorImage.attr('src', imagesPath + "/bootstrap-svg/memory-n.svg");
            } else if (threshold > 50.0 && threshold < 75.0) {
                ramIndicatorImage.attr('src', imagesPath + "/bootstrap-svg/memory-w.svg");
            } else if (threshold > 75.0 && threshold <= 100.0) {
                ramIndicatorImage.attr('src', imagesPath + "/bootstrap-svg/memory-d.svg");
            }

            let total = `<li><a class="dropdown-item">Total RAM: ${data[1]["ram_total"]}</a></li>`;
            let free = `<li><a class="dropdown-item">Free RAM: ${data[2]["ram_free"]}</a></li>`;
            let used = `<li><a class="dropdown-item">Used RAM: ${data[3]["ram_used"]}</a></li>`;

            ramIndicatorTextContent.text(data[0]["ram_util"].trim() + "%");

            dropdownTitle(hostElem, total + free + used, '.server-ram-text.dropend');

        } else {
            throw new Error(`Хост ${hostElem.id} недоступен`);
        }
    } catch (e) {
        ramIndicatorTextContent.text("N/A");
        ramIndicatorImage.attr('src', na);
    }
}

function cpuTopAnalysis(data, hostElem) {
    let cpuIndicatorImage = hostElem.find('[data-indicator-type="cpu"]');
    let cpuIndicatorTextContent = hostElem.find('.server-cpu-text').find('p');
    let status = data[0]["all_cores"] !== undefined;
    let na = imagesPath + "/bootstrap-svg/cpu.svg";

    // dropdown menu
    hostElem.attr('data-available', status);


    try {
        if (status) {
            let threshold = parseFloat(data[0]["all_cores"]["cpu_load"]);
            if (threshold > 0.0 && threshold < 50.0) {
                cpuIndicatorImage.attr('src', imagesPath + "/bootstrap-svg/cpu-n.svg");
            } else if (threshold > 50.0 && threshold < 75.0) {
                cpuIndicatorImage.attr('src', imagesPath + "/bootstrap-svg/cpu-w.svg");
            } else if (threshold > 75.0 && threshold <= 100.0) {
                cpuIndicatorImage.attr('src', imagesPath + "/bootstrap-svg/cpu-d.svg");
            }

            cpuIndicatorTextContent.text(data[0]["all_cores"]["cpu_load"] + "%");

            let cores = "";

            for (let core = 0; core < data[1]["each_core"].length; core++) {
                cores += `<li><a class="dropdown-item">Core${core}: ${data[1]["each_core"][core][`core${core}`]}%</a></li>`
            }

            dropdownTitle(hostElem, cores, '.server-cpu-text.dropend');

        } else {
            throw new Error(`Хост ${hostElem.id} недоступен`);
        }
    } catch (e) {
        cpuIndicatorTextContent.text("N/A");
        cpuIndicatorImage.attr('src', na);
    }
}

function execAnalysis(data, hostElem) {
    let processesIndicatorImage = hostElem.find('[data-indicator-type="apps"]');
    let processesIndicatorTextContent = hostElem.find('.server-apps-text').find('p');
    let status = data[0]["status"] !== undefined;
    let na = imagesPath + "/bootstrap-svg/app-indicator.svg"
    hostElem.attr('data-available', status);


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

            let processesTooltip = "".concat(processesArray).replace(/,/g, '\n');
            let processesCount = processesArray.length;

            //processes
            processesIndicatorTextContent.text(processesCount);
            processesIndicatorImage.attr('src', imagesPath + "/bootstrap-svg/app-indicator-n.svg");

            dropdownTitle(hostElem, processesTooltip, '.server-apps-text.dropend');

        } else {
            throw new Error("Хост недоступен.");
        }
    } catch (e) {
        processesIndicatorTextContent.text("N/A");
        processesIndicatorImage.attr('src', na);
    }
}

function updateServerNode(data, id, server_role, callback) {
    let hostElem = $(`#${id}`);
    let serverNodeImage = hostElem.find('[data-indicator-type="server"]');
    let serverNodeTextContent = hostElem.find('.server-status');
    let err = data[0]["connection_error"] === undefined;

    // server status

    //if server media else server head
    let mediaUp = imagesPath + "/bootstrap-svg/server-n.svg";
    let mediaDown = imagesPath + "/bootstrap-svg/server-d.svg";
    let headUp = imagesPath + "/bootstrap-svg/server-head-n.svg";
    let headDown = imagesPath + "/bootstrap-svg/server-head-d.svg";


    if (server_role === 'media')
        serverNodeImage.attr('src', err ? mediaUp : mediaDown);
    else
        serverNodeImage.attr('src', err ? headUp : headDown);

    // status
    serverNodeTextContent.text(err ? "UP\n" : "DOWN\n");

    callback(data, hostElem)

}

    /**
     * функция, перерисовывающая сервера, в зависимости от доступности монитора.
     * @param servers сервера.
     * @param reason причина, по умолчанию - undefined.
     * @param available доступность, по умолчанию - true.
     */
function monitorAvailability(servers, reason=undefined, available= true) {
    let agentStatus = $('#agent-status');

    agentStatus.text(available ? "монитор в норме." : reason);
    agentStatus.css({"color": available ? "#00ff33AA" : "#ff0033AA"});
    let bg = available ? "#ececec" : "#bebdbd";

    let serverInfoPaneLeft = servers.find('.server-left-part');

    serverInfoPaneLeft.css({"background": bg});

    if(!available) {
        let text = "N/A";
        serverInfoPaneLeft.find('.server-status').text(text);
        serverInfoPaneLeft.find('.server-hostname').text(text);
    }

    let imgArray = [
        imagesPath + "/bootstrap-svg/cpu.svg",
        imagesPath + "/bootstrap-svg/memory.svg",
        imagesPath + "/bootstrap-svg/device-ssd.svg",
        imagesPath + "/bootstrap-svg/app-indicator.svg",
        imagesPath + "/bootstrap-svg/ethernet.svg",
    ];

    for (let server of servers) {
        let serverElem = $(`#${server.id}`);

        if (!available) {
            let role = serverElem.find('.server-role').text() === "HEAD";
            let head = imagesPath + "/bootstrap-svg/server-head.svg";
            let media = imagesPath + "/bootstrap-svg/server.svg";
            serverElem.find('img').attr('src', role ? head : media);
        }

        // server info
        let serverInfoPaneRight = server.childNodes[3].childNodes;

        for (let i = 1, img = 0; i < serverInfoPaneRight.length; i += 2, img++) {
            // изменяем все индикаторы
            serverInfoPaneRight[i].style.backgroundColor = bg;

            if (!available) {
                serverInfoPaneRight[i].childNodes[3].childNodes[1].textContent = "N/A";
                serverInfoPaneRight[i].childNodes[1].src = imgArray[img];
            }

        }

    }

}

    /**
     * функция, перерисывающая инфопанель в завимости от определенных условий
     * @param parsedData данные с серверов.
     * @param callback функция обработки данных с серверов.
     */
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
        monitorAvailability($('.server'), parsedData['ClientConnectionError'], false);
    //если конфигурация сервера мониторинга не найдена
    else if (parsedData['DoesNotExist'] !== undefined)
        monitorAvailability($('.server'), parsedData['DoesNotExist'], false);
    //агент не может валидировать данные
    else if (parsedData['ValidationException'] !== undefined)
        monitorAvailability($('.server'), parsedData['ValidationException'], false);
    //таблица с целевыми хостами отсутствует
    else if (parsedData["ProgrammingError"] !== undefined || parsedData['TargetsIsEmpty'] !== undefined)
        monitorAvailability($('.server'), parsedData["ProgrammingError"], false);
    else {
        monitorAvailability($('.server'));
        parsedData.forEach(el => updateServerNode(el.data, el.id, el.role, callback));
    }

}

let headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
}

    /**
     * подфункция inspectServers.
     * @param url url метрики в бэкенде.
     * @param method HTTP метод.
     * @param headers AJAX заголовки.
     * @param callback функция, обрабатывающая результат снятия метрики
     */
async function getMetrics (url, method, headers, callback) {
    let response = await fetch(url, {
        method: method, headers: headers
    });

    let data = await response.json()
    let parsedData = JSON.parse(data);

    if (callback !== undefined)
        redrawTableElements(parsedData, callback);
}


    /**
     * функция берет интервал с бэкенда.
     * в случае, если бэкенд пал - интервал равен 5с
     */
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

    /**
     * функция берет данные с серверов через бэкенд,
     * раз в 15 секунд по умолчанию.
     * интервал снятия метрик можно настроить в админке
     */
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

    /**
     * main
     * инициализация скрипта
     */
setTimeout(async function () {
    await inspectServers();
    let interval = await getInterval("interval/", "GET", headers);
    setInterval(inspectServers, interval);
}, 0);
// main //