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
    targetElem.find('div[class=*"-text"]').find('p').text("N/A");
}

function serverIsUp(targetId, reason= "") {
    let targetElem = $(`#${targetId}`);
    serverStatus(targetElem, "UP", true,
        reason, "#00ff00aa");
}

function serverIsDown (targetId, reason, hardwareAttr, hardwarePic) {
    let targetElem = $(`#${targetId}`);
    let text = reason.replace(/:.*/g, ".");
    serverStatus(targetElem, "DOWN", false,
        text, "#ff0000aa", "none", hardwareAttr, hardwarePic);
}

function noAccessToServer(targetId, reason) {
    let targetElem = $(`#${targetId}`);
    let text = reason.replace(/:.*/g, ".");
    serverStatus(targetElem, "NO ACCESS", false,
        text, "#ff9900aa", "none");
}

function agentIsDown() {

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