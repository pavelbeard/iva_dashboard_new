const headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
};

let imgPath = "/static/dashboard/images/bootstrap-svg";

let serverPics = {
    "serverMedia": imgPath + "/server.svg",
    "serverMediaUp": imgPath + "/server-n.svg",
    "serverMediaDown": imgPath + "/server-d.svg",
    "serverHead": imgPath + "/server-head.svg",
    "serverHeadUp": imgPath + "/server-head-n.svg",
    "serverHeadDown": imgPath + "/server-head-d.svg"
};

let cpuPics = {
    "cpu": imgPath + "/cpu.svg",
    "cpuNormal": imgPath + "/cpu-n.svg",
    "cpuWarning": imgPath + "/cpu-w.svg",
    "cpuDanger": imgPath + "/cpu-d.svg",
};

let ramPics = {
    "ram": imgPath + "/memory.svg",
    "ramNormal": imgPath + "/memory-n.svg",
    "ramWarning": imgPath + "/memory-w.svg",
    "ramDanger": imgPath + "/memory-d.svg",
};

let ssdPics = {
    "deviceSsd": imgPath + "/device-ssd.svg",
    "deviceSsdNormal": imgPath + "/device-ssd-n.svg",
    "deviceSsdWarning": imgPath + "/device-ssd-w.svg",
    "deviceSsdDanger": imgPath + "/device-ssd-d.svg",
};

let appPics = {
    "appIndicator": imgPath + "/app-indicator.svg",
    "appIndicatorNormal": imgPath + "/app-indicator-n.svg",
};

let ethernetPics = {
    "ethernet": imgPath + "/ethernet.svg",
    "ethernetUp": imgPath + "/ethernet-n.svg",
    "ethernetDown": imgPath + "/ethernet-d.svg",
};

let hardwareAttrs = {
    "server": `[data-indicator-type="server"]`,
    "cpu": `[data-indicator-type="cpu"]`,
    "ram": `[data-indicator-type="ram"]`,
    "disk": `[data-indicator-type="disk"]`,
    "apps": `[data-indicator-type="apps"]`,
    "net": `[data-indicator-type="network"]`,
};

let hardwarePrimePics = {
    "server": serverPics.serverMedia,
    "cpu": cpuPics.cpu,
    "ram": ramPics.ram,
    "disk": ssdPics.deviceSsd,
    "apps": appPics.appIndicator,
    "net": ethernetPics.ethernet,
}

let serverDownPics = {
    "server": serverPics.serverMediaDown,
    "cpu": cpuPics.cpu,
    "ram": ramPics.ram,
    "disk": ssdPics.deviceSsd,
    "apps": appPics.appIndicator,
    "net": ethernetPics.ethernet,
}

let hardwareDropdownLocate = {
    "cpu": '.server-cpu-text.dropend',
    "ram": '.server-ram-text.dropend',
    "disk": '.server-disk-text.dropend',
    "apps": '.server-apps-text.dropend',
    "net": '.server-network-text.dropup',
}

export {headers, serverPics, cpuPics, ramPics, ssdPics, appPics, ethernetPics,
    hardwareAttrs, hardwarePrimePics, hardwareDropdownLocate, serverDownPics}