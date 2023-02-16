import * as events from "./server-event-handlers.js";
import * as base from "./base.js"
import * as ext from "./tweaks.js";
import {
    appPics, ethernetPics,
    hardwareAttrs,
    hardwareDropdownLocate,
    hardwarePrimePics,
    ramPics,
    serverDownPics,
    serverPics,
    ssdPics
} from "./base.js";
import {convertBytesToMetric as cbtm} from "./converters.js";
import {dropdownTitle} from "./tweaks.js";
import {thresholdUtilEventListener} from "./server-event-handlers.js";

function serverRoleDataHandler(targetId, value) {
    let targetElem = $(`#${targetId}`);

    if (value['server_role'] === "slave" || value['server_role'] === "master") {
        targetElem.find(hardwareAttrs.server).attr('src', serverPics.serverHeadUp)
    } else {
        targetElem.find(hardwareAttrs.server).attr('src', serverPics.serverMediaUp)
    }

    targetElem.find('.server-role').text(value['server_role']);
}

function cpuDataHandler(targetId, values) {
    let targetElem = $(`#${targetId}`);
    let wholeProcessorData = values['whole_processor_data'];
    let processorCoresData = values['processor_cores_data'];
    let cpuIdle = wholeProcessorData['cpu_idle'];
    let cpuUtil = wholeProcessorData['cpu_util'];
    let cpuPic = events.thresholdUtilEventListener(cpuUtil, base.cpuPics);

    targetElem.find(hardwareAttrs.cpu).attr('src', cpuPic);
    targetElem.find(hardwareDropdownLocate.cpu).find('p').text(`${cpuUtil}%`);

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
    ext.dropdownTitle(targetElem, htmlMarkup, hardwareDropdownLocate.cpu);
}

function ramDataHandler(targetId, values) {
    let targetElem = $(`#${targetId}`);
    let ramUtil = values['ram_util'];
    let ramPic = events.thresholdUtilEventListener(ramUtil, ramPics);

    targetElem.find(hardwareAttrs.ram).attr('src', ramPic)
    targetElem.find(hardwareDropdownLocate.ram).find('p').text(`${ramUtil}%`);

    let htmlMarkup = `
        <li><a class="dropdown-item">Ram util: ${ramUtil}%</a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item">Total ram: ${cbtm(values['total_ram'])}</a></li>
        <li><a class="dropdown-item">Ram used: ${cbtm(values['ram_used'])}</a></li>
        <li><a class="dropdown-item">Ram shared: ${cbtm(values['ram_shared'])}</a></li>
        <li><a class="dropdown-item">Ram buff cache: ${cbtm(values['ram_buff_cache'])}</a></li>
        <li><a class="dropdown-item">Ram avail: ${cbtm(values['ram_avail'])}</a></li>
    `;

    dropdownTitle(targetElem, htmlMarkup, hardwareDropdownLocate.ram);
}

function diskDataHandler(targetId, values) {
    let mvPart = values.pop()
    let targetElem = $(`#${targetId}`);
    let mvPartMarkup = "";

    for (let [k, v] of Object.entries(mvPart))
    {
        let isMvPartPercent = k === 'most_valuable_part_use_percent';
        let tmp = !isNaN(parseInt(v)) && !isMvPartPercent ?
            cbtm(v) : v;
        if (isMvPartPercent) tmp += '%';

        mvPartMarkup += `<li><a class="dropdown-item">${k.toCapitalizePythonKey()}: ${tmp}</a></li>`;
    }

    mvPartMarkup += `<li><hr class="dropdown-divider"></li>`;
    let mvPartUsePercent = mvPart['most_valuable_part_use_percent'] + `%`;
    let diskPic = events.thresholdUtilEventListener(mvPartUsePercent.slice(0, -1), ssdPics);

    targetElem.find(hardwareDropdownLocate.disk).find('p').text(mvPartUsePercent);
    targetElem.find(hardwareAttrs.disk).attr('src', diskPic);

    mvPartMarkup += `<li><a class="dropdown-item">
    filesystem | fs size | fs used | fs used % | fs available | mounted on
    </a></li>`

    values.forEach(fs => {
        mvPartMarkup +=
            `<li><a class="dropdown-item">
            ${fs['file_system']} | ${cbtm(fs['fs_size'])} | ${cbtm(fs['fs_used'])} | 
            ${fs['fs_used_prc']} | ${cbtm(fs['fs_avail'])} | ${fs['mounted_on']} 
            </a></li>`
    })

    dropdownTitle(targetElem, mvPartMarkup, hardwareDropdownLocate.disk);
}

function appDataHandler(targetId, values) {
    console.log(targetId, values);
    let targetElem = $(`#${targetId}`);
    let appPic = appPics.appIndicatorNormal;

    targetElem.find(hardwareDropdownLocate.apps).find('p').text(values.length);
    targetElem.find(hardwareAttrs.apps).attr('src', appPic);

    let processMarkup = "<li><a class='dropdown-item'>" +
        "name of process | status" +
        "</a></li>";

    values.forEach(process => {
        processMarkup += `<li><a class="dropdown-item">
        ${process['process_name']} | ${process['process_status']}
        </a></li>`
    });

    dropdownTitle(targetElem, processMarkup, hardwareDropdownLocate.apps);
}

function netDataHandler(targetId, values) {
    console.log(targetId, values);
    let targetElem = $(`#${targetId}`);
    let netPic = ethernetPics.ethernetUp;
    let netMarkup = "";
    // let netMarkup = `<li><a class="dropdown-item">
    // interface | status | ipv4 | rx bytes | rx packets | rx errors + dropped + overruns + frame |
    // tx bytes | tx packets | tx errors + dropped + overruns + carrier + collisions
    // </a></li>`.replace(/[,\n]/, "");

    targetElem.find(hardwareDropdownLocate.net).find('p').text("UP");
    targetElem.find(hardwareAttrs.net).attr('src', netPic);

    values.forEach(iface => {
        netMarkup += `<li><a class="dropdown-item">Interface: ${iface['interface']}<br>Status: ${iface['status']}<br>  
        IPv4: ${iface['ip_address']}<br>RX bytes: ${cbtm(iface['rx_bytes'])}<br> 
        RX packets: ${iface['rx_packets']}<br> RX errors: ${iface['rx_errors_errors']} | dropped: ${iface['rx_errors_dropped']} | 
        overruns: ${iface['rx_errors_overruns']} | frame: ${iface['rx_errors_frame']}<br>
        TX bytes ${cbtm(iface['tx_bytes'])}<br> TX packets ${iface['tx_packets']}<br>
        TX errors ${iface['tx_errors_errors']} | dropped: ${iface['tx_errors_dropped']} | 
        overruns: ${iface['tx_errors_overruns']} | carrier: ${iface['tx_errors_carrier']} | 
        collisions: ${iface['tx_errors_collisions']}</li></a>`
    });

    dropdownTitle(targetElem, netMarkup, hardwareDropdownLocate.net);
}

function serverDataHandler(targetId, values) {
    let targetElem = $(`#${targetId}`);
    targetElem.find('.server-hostname').text(values['hostname']);
}

function uptimeDataHandler(targetId, values) {
    let targetElem = $(`#${targetId}`);
    let html = `<li><a class="dropdown-item">${values['uptime']}</a></li>`

    dropdownTitle(targetElem, html, '.server-img.dropend');
}

function averageLoadDataHandler(targetId, values) {
    console.log(targetId, values);
}


    /**
     *
     * @param responseData
     */
function dataDistributor(responseData) {
    let handlers = [
        serverRoleDataHandler,
        cpuDataHandler,
        ramDataHandler,
        diskDataHandler,
        netDataHandler,
        appDataHandler,
        serverDataHandler,
        uptimeDataHandler,
        averageLoadDataHandler
    ];


    let hard

    for (let key in responseData) {
        let scrapedData = responseData[key];

        // проверяются данные каждого id на соответствие типу данных
        if (!(typeof (scrapedData) === typeof({}) || typeof (scrapedData) === typeof([]))) {
            if (scrapedData.includes('unable to connect'))
                events.serverIsDown(key, scrapedData,
                    Object.values(hardwareAttrs), Object.values(serverDownPics));
            else
                events.agentIsDown()

        } else if (scrapedData.length === handlers.length) {
            for (let i = 0; i < scrapedData.length; i++) {
                events.serverIsUp(key);
                setTimeout(handlers[i], 0, key, scrapedData[i])
            }
        }
    }
}

/**
     * подфункция inspectServers.
     * @param url url метрики в бэкенде.
     * @param method HTTP метод.
     */
async function getMetricsFromBackend(url, method) {
    const response = await fetch(url, {
        method: method, headers: base.headers
    }).then(async r => {
        return JSON.parse(await r.json());
    }).catch(e => {
        console.log(e);
    });

    dataDistributor(response);
}

async function getInterval(url, method) {
    let response = await fetch(url, {
        method: method, headers: base.headers
    });

    let interval = JSON.parse(await response.json());

    if (interval['DoesNotExist'] === undefined)
        return  parseInt(interval.interval) * 1000;
    else
        return 5000;
}

setTimeout(async function() {
    let interval = await getInterval("interval/", "GET");
    setInterval(getMetricsFromBackend, interval, "all-metrics/", "GET")
});