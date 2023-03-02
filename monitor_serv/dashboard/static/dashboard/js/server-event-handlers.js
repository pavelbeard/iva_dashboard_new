import {
    APP_PICS, CPU_PICS, ETHERNET_PICS,
    HARDWARE_ATTRS,
    HARDWARE_DROPDOWN_LOCATE,
    RAM_PICS,
    SERVER_PICS,
    SSD_PICS
} from "../../../../static/js/base.js";

function serverStatus(
    targetElem, status, availability,
    reason, availabilityColor,
    role="", hardwareAttrs=[],
    hardwarePics=[]
) {
    targetElem.attr('data-available', availability);
    targetElem.find('.server-status').text(status);
    targetElem.find(`[data-add-info="server-add-info-indicator"]`).text(reason);

    if (role !== "") {
        targetElem.find('.server-role').text(role);
    }

    // картинки по умолчанию
    hardwareAttrs.forEach((attr, i=0) => {
        targetElem.find(attr).attr('src', hardwarePics[i]); i++;
    })

    // цвет фона, определяющий доступность
    targetElem.find(`[data-add-info="server-add-info-indicator"]`).css(
        {"background": availabilityColor}
    );

    // обнуляем все индикаторы
    // targetElem.find('div[class=*"-text"]').find('p').text("N/A");
}

function serverIsUp(targetId, reason= "") {
    let targetElem = $(`#${targetId}`);
    serverStatus(targetElem, "UP", true,
        reason, "#00ff00aa");
}

function serverIsDown (targetId, reason, hardwareAttr, hardwarePic) {
    let targetElem = $(`#${targetId}`);
    let text = reason.replace(/:.*/g, ".");

    targetElem.find('div[class*="-text"]').find('p').text("N/A");

    serverStatus(targetElem, "DOWN", false,
        text, "#ff0000aa", "none", hardwareAttr, hardwarePic);
}

function noAccessToServer(targetId, reason) {
    let targetElem = $(`#${targetId}`);
    let text = reason.replace(/:.*/g, ".");
    serverStatus(targetElem, "NO ACCESS", false,
        text, "#ff9900aa", "none");
}

function agentIsDown(response) {
    let isAvailable = !(response.ping === "false") && !(response["DashboardSettingsNotFound"] === "no data.");
    let status = isAvailable ? "агент доступен." : "агент недоступен.";

    let agentStatus = $("#agent-status");
    agentStatus.css({color: isAvailable ?  '#00ff00aa' : '#ff0000AA', wordBreak: "break-all"});
    agentStatus.text(status);

    let monitoringStatusBar = $("#monitoring-status-bar");
    monitoringStatusBar.text(isAvailable ? "" : response.reason !== undefined ? response.reason : "");

    if (!isAvailable) {
        let servers = $('.server');
        monitoringStatusBar.css({color: "#ff0000AA", fontWeight: 700});

        servers.find('.server-status').text("N/A");
        servers.find('.server-hostname').text("N/A");
        servers.find('.server-role').text("N/A");

        servers.find(HARDWARE_ATTRS.server).attr('src', SERVER_PICS.serverMedia);

        servers.find(HARDWARE_DROPDOWN_LOCATE.cpu).find('p').text('N/A');
        servers.find(HARDWARE_ATTRS.cpu).attr('src', CPU_PICS.cpu);

        servers.find(HARDWARE_DROPDOWN_LOCATE.ram).find('p').text('N/A');
        servers.find(HARDWARE_ATTRS.ram).attr('src', RAM_PICS.ram);

        servers.find(HARDWARE_DROPDOWN_LOCATE.disk).find('p').text('N/A');
        servers.find(HARDWARE_ATTRS.disk).attr('src', SSD_PICS.deviceSsd);

        servers.find(HARDWARE_DROPDOWN_LOCATE.apps).find('p').text('N/A');
        servers.find(HARDWARE_ATTRS.apps).attr('src', APP_PICS.appIndicator);

        servers.find(HARDWARE_DROPDOWN_LOCATE.net).find('p').text('N/A');
        servers.find(HARDWARE_ATTRS.net).attr('src', ETHERNET_PICS.ethernet);
    }
}

function thresholdUtilEventListener(utilization, picsObj) {
    let util = parseFloat(utilization);
    let picsKeys = Object.keys(picsObj);

    if (util => 0.0 && util < 50.0) {
        return picsObj[picsKeys[1]];
    } else if (util => 50.0 && util < 75.0) {
        return picsObj[picsKeys[2]];
    } else {
        return picsObj[picsKeys[3]];
    }
}

export {serverIsUp, serverIsDown, noAccessToServer, agentIsDown, thresholdUtilEventListener}