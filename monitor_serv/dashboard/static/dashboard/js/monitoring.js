import {
    APP_PICS, CPU_PICS, ETHERNET_PICS,
    HARDWARE_ATTRS,
    HARDWARE_DROPDOWN_LOCATE,
    HEADERS,
    RAM_PICS,
    SERVER_DOWN_PICS,
    SERVER_PICS,
    SSD_PICS, convertBytesToMetric
} from "../../../../static/js/base.js";
import {dropdownTitle} from "./tweaks.js";
import {
    agentIsDown,
    noAccessToServer,
    serverIsDown,
    serverIsUp,
    thresholdUtilEventListener
} from "./server-event-handlers.js";

function serverRoleDataHandler(targetId, value) {
    let targetElem = $(`#${targetId}`);

    if (value['server_role'] === "slave" || value['server_role'] === "master") {
        targetElem.find(HARDWARE_ATTRS.server).attr('src', SERVER_PICS.serverHeadUp)
    } else {
        targetElem.find(HARDWARE_ATTRS.server).attr('src', SERVER_PICS.serverMediaUp)
    }

    targetElem.find('.server-role').text(value['server_role']);
}

function cpuDataHandler(targetId, values) {
    let targetElem = $(`#${targetId}`);
    let wholeProcessorData = values['whole_processor_data'];
    let processorCoresData = values['processor_cores_data'];
    let cpuUtil = wholeProcessorData['cpu_util'];
    let cpuPic = thresholdUtilEventListener(cpuUtil, CPU_PICS);

    targetElem.find(HARDWARE_ATTRS.cpu).attr('src', cpuPic);
    targetElem.find(HARDWARE_DROPDOWN_LOCATE.cpu).find('p').text(`${cpuUtil}%`);

    let wholeProcessorDataMarkup = [
        `<li><a class="dropdown-item">CPU Util: ${cpuUtil}%</a></li>`,
        `<li><hr class="dropdown-divider"></li>`,
    ];

    let processorCoresDataMarkup = [];

    processorCoresData.forEach((core, i=0) => {
        let cpuCoreUtil = core[`core${i++}`] + '%';
         processorCoresDataMarkup
             .push(`<li><a class="dropdown-item">Core ${i++} util: ${cpuCoreUtil}</a></li>`);
    });

    let htmlMarkup = "".concat(wholeProcessorDataMarkup + processorCoresDataMarkup)
        .replace(/,/g, "");
    dropdownTitle(targetElem, htmlMarkup, HARDWARE_DROPDOWN_LOCATE.cpu);
}

function ramDataHandler(targetId, values) {
    let targetElem = $(`#${targetId}`);
    let ramUtil = values['ram_util'];
    let ramPic = thresholdUtilEventListener(ramUtil, RAM_PICS);

    targetElem.find(HARDWARE_ATTRS.ram).attr('src', ramPic)
    targetElem.find(HARDWARE_DROPDOWN_LOCATE.ram).find('p').text(`${ramUtil}%`);

    let htmlMarkup = `
        <li><a class="dropdown-item">Ram util: ${ramUtil}%</a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item">Total ram: ${convertBytesToMetric(values['total_ram'])}</a></li>
        <li><a class="dropdown-item">Ram used: ${convertBytesToMetric(values['ram_used'])}</a></li>
        <li><a class="dropdown-item">Ram shared: ${convertBytesToMetric(values['ram_shared'])}</a></li>
        <li><a class="dropdown-item">Ram buff cache: ${convertBytesToMetric(values['ram_buff_cache'])}</a></li>
        <li><a class="dropdown-item">Ram avail: ${convertBytesToMetric(values['ram_avail'])}</a></li>
    `;

    dropdownTitle(targetElem, htmlMarkup, HARDWARE_DROPDOWN_LOCATE.ram);
}

function diskDataHandler(targetId, values) {
    let mvPart = values.pop()
    let targetElem = $(`#${targetId}`);
    let mvPartMarkup = "";

    for (let [k, v] of Object.entries(mvPart))
    {
        let isMvPartPercent = k === 'most_valuable_part_use_percent';
        let tmp = !isNaN(parseInt(v)) && !isMvPartPercent ?
            convertBytesToMetric(v) : v;
        if (isMvPartPercent) tmp += '%';

        mvPartMarkup += `<li><a class="dropdown-item">${k.toCapitalizePythonKey()}: ${tmp}</a></li>`;
    }

    mvPartMarkup += `<li><hr class="dropdown-divider"></li>`;
    let mvPartUsePercent = mvPart['most_valuable_part_use_percent'] + `%`;
    let diskPic = thresholdUtilEventListener(mvPartUsePercent.slice(0, -1), SSD_PICS);

    targetElem.find(HARDWARE_DROPDOWN_LOCATE.disk).find('p').text(mvPartUsePercent);
    targetElem.find(HARDWARE_ATTRS.disk).attr('src', diskPic);

    mvPartMarkup += `<li><a class="dropdown-item">
    filesystem | fs size | fs used | fs used % | fs available | mounted on
    </a></li>`

    values.forEach(fs => {
        mvPartMarkup +=
            `<li><a class="dropdown-item">
            ${fs['file_system']} | ${convertBytesToMetric(fs['fs_size'])} | ${convertBytesToMetric(fs['fs_used'])} | 
            ${fs['fs_used_prc']} | ${convertBytesToMetric(fs['fs_avail'])} | ${fs['mounted_on']} 
            </a></li>`
    })

    dropdownTitle(targetElem, mvPartMarkup, HARDWARE_DROPDOWN_LOCATE.disk);
}

function appDataHandler(targetId, values) {
    let targetElem = $(`#${targetId}`);
    let appPic = APP_PICS.appIndicatorNormal;

    targetElem.find(HARDWARE_DROPDOWN_LOCATE.apps).find('p').text(values.length);
    targetElem.find(HARDWARE_ATTRS.apps).attr('src', appPic);

    let processMarkup = "<li><a class='dropdown-item'>" +
        "name of process | status" +
        "</a></li>";

    values.forEach(process => {
        processMarkup += `<li><a class="dropdown-item">
        ${process['process_name']} | ${process['process_status']}
        </a></li>`
    });

    dropdownTitle(targetElem, processMarkup, HARDWARE_DROPDOWN_LOCATE.apps);
}

function netDataHandler(targetId, values) {
    let targetElem = $(`#${targetId}`);
    let netPic = ETHERNET_PICS.ethernetUp;
    let netMarkup = "";

    targetElem.find(HARDWARE_DROPDOWN_LOCATE.net).find('p').text("UP");
    targetElem.find(HARDWARE_ATTRS.net).attr('src', netPic);

    values.forEach(iface => {
        netMarkup += `<li><a class="dropdown-item">Interface: ${iface['interface']}<br>Status: ${iface['status']}<br>  
        IPv4: ${iface['ip_address']}<br>RX bytes: ${convertBytesToMetric(iface['rx_bytes'])}<br> 
        RX packets: ${iface['rx_packets']}<br> RX errors: ${iface['rx_errors_errors']} | dropped: ${iface['rx_errors_dropped']} | 
        overruns: ${iface['rx_errors_overruns']} | frame: ${iface['rx_errors_frame']}<br>
        TX bytes ${convertBytesToMetric(iface['tx_bytes'])}<br> TX packets ${iface['tx_packets']}<br>
        TX errors ${iface['tx_errors_errors']} | dropped: ${iface['tx_errors_dropped']} | 
        overruns: ${iface['tx_errors_overruns']} | carrier: ${iface['tx_errors_carrier']} | 
        collisions: ${iface['tx_errors_collisions']}</li></a>`
    });

    dropdownTitle(targetElem, netMarkup, HARDWARE_DROPDOWN_LOCATE.net);
}

function serverDataHandler(targetId, values) {
    let targetElem = $(`#${targetId}`);
    targetElem.find('.server-hostname').text(values['hostname']);
}

function uptimeDataHandler(targetId, values) {
    let targetElem = $(`#${targetId}`);
    let html = `<li><a class="dropdown-item">${values['uptime']}</a></li>`

    dropdownTitle(targetElem, html, HARDWARE_DROPDOWN_LOCATE.server);
}

function averageLoadDataHandler(targetId, values) {
    console.log(targetId, values);
}


    /**
     *
     * @param responseData
     */
function dataDistributor(responseData) {
    const HANDLERS = [
        serverRoleDataHandler,
        cpuDataHandler,
        ramDataHandler,
        diskDataHandler,
        appDataHandler,
        netDataHandler,
        serverDataHandler,
        uptimeDataHandler,
        averageLoadDataHandler
    ];

    for (let key in responseData) {
        let scrapedData = responseData[key];

        // проверяются данные каждого id на соответствие типу данных
        if (!(typeof (scrapedData) === typeof({}) || typeof (scrapedData) === typeof([]))) {
            if (scrapedData.includes('unable to connect')
                || scrapedData.includes('unexpected exception')
                || scrapedData.includes('Connect call failed'))
                serverIsDown(key, scrapedData,
                    Object.values(HARDWARE_ATTRS), Object.values(SERVER_DOWN_PICS));
            else if (scrapedData.includes('bad credentials'))
                noAccessToServer(key, scrapedData,
                    Object.values(HARDWARE_ATTRS), Object.values(SERVER_DOWN_PICS));
            else
               return;

        } else if (scrapedData.length === HANDLERS.length) {
            for (let i = 0; i < scrapedData.length; i++) {
                serverIsUp(key);
                setTimeout(HANDLERS[i], 0, key, scrapedData[i])
            }
        }
    }
}

async function checkAgentHealth (url, method) {
    const response = await fetch(url, {
        method: method, headers: HEADERS
    }).then(async r => {
        return JSON.parse(await r.json());
    });

    agentIsDown(response);
}

/**
     * подфункция inspectServers.
     * @param url url метрики в бэкенде.
     * @param method HTTP метод.
     */
async function getMetricsFromBackend(url, method) {
    const response = await fetch(url, {
        method: method, headers: HEADERS
    }).then(async r => {
        return JSON.parse(await r.json());
    }).catch(err_response => {
        return err_response;
    });

    dataDistributor(response);
}

async function getInterval(url, method) {
    let response = await fetch(url, {
        method: method, headers: HEADERS
    });

    let interval = JSON.parse(await response.json());

    if (interval['DashboardSettingsNotFound'] === undefined)
        return  parseInt(interval.interval) * 1000;
    else
        return 5000;
}

setTimeout(async function() {
    let interval = await getInterval("interval/", "GET");
    setTimeout(getMetricsFromBackend,0, "all-metrics/", "GET")
    setInterval(getMetricsFromBackend, interval, "all-metrics/", "GET")
    setTimeout(checkAgentHealth,0, "check-agent-health/", "GET")
    setInterval(checkAgentHealth, interval, "check-agent-health/", "GET")
});