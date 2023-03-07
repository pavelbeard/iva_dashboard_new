export const HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
};

export const HTTP_METHODS = {
    get: "GET",
    post: "POST",
    put: "PUT",
    patch: "PATCH",
    delete: "DELETE",
}

export function formatBytes(bytes, decimals = 2) {
    if (!+bytes) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}


const IMG_PATH = "/static/dashboard/images/bootstrap-svg";

export const SERVER_PICS = {
    serverMedia: IMG_PATH + "/server.svg",
    serverMediaUp: IMG_PATH + "/server-n.svg",
    serverMediaDown: IMG_PATH + "/server-d.svg",
    serverHead: IMG_PATH + "/server-head.svg",
    serverHeadUp: IMG_PATH + "/server-head-n.svg",
    serverHeadDown: IMG_PATH + "/server-head-d.svg"
};

export const CPU_PICS = {
    cpu: IMG_PATH + "/cpu.svg",
    cpuNormal: IMG_PATH + "/cpu-n.svg",
    cpuWarning: IMG_PATH + "/cpu-w.svg",
    cpuDanger: IMG_PATH + "/cpu-d.svg",
};

export const RAM_PICS = {
    ram: IMG_PATH + "/memory.svg",
    ramNormal: IMG_PATH + "/memory-n.svg",
    ramWarning: IMG_PATH + "/memory-w.svg",
    ramDanger: IMG_PATH + "/memory-d.svg",
};

export const SSD_PICS = {
    deviceSsd: IMG_PATH + "/device-ssd.svg",
    deviceSsdNormal: IMG_PATH + "/device-ssd-n.svg",
    deviceSsdWarning: IMG_PATH + "/device-ssd-w.svg",
    deviceSsdDanger: IMG_PATH + "/device-ssd-d.svg",
};

export const APP_PICS = {
    appIndicator: IMG_PATH + "/app-indicator.svg",
    appIndicatorNormal: IMG_PATH + "/app-indicator-n.svg",
};

export const ETHERNET_PICS = {
    ethernet: IMG_PATH + "/ethernet.svg",
    ethernetUp: IMG_PATH + "/ethernet-n.svg",
    ethernetDown: IMG_PATH + "/ethernet-d.svg",
};

export const HARDWARE_ATTRS = {
    server: `[data-indicator-type="server"]`,
    cpu: `[data-indicator-type="cpu"]`,
    ram: `[data-indicator-type="ram"]`,
    disk: `[data-indicator-type="disk"]`,
    apps: `[data-indicator-type="apps"]`,
    net: `[data-indicator-type="network"]`,
};

export const HARDWARE_PRIME_PICS = {
    server: SERVER_PICS.serverMedia,
    cpu: CPU_PICS.cpu,
    ram: RAM_PICS.ram,
    disk: SSD_PICS.deviceSsd,
    apps: APP_PICS.appIndicator,
    net: ETHERNET_PICS.ethernet,
}

export const SERVER_DOWN_PICS = {
    server: SERVER_PICS.serverMediaDown,
    cpu: CPU_PICS.cpu,
    ram: RAM_PICS.ram,
    disk: SSD_PICS.deviceSsd,
    apps: APP_PICS.appIndicator,
    net: ETHERNET_PICS.ethernet,
}

export const HARDWARE_DROPDOWN_LOCATE = {
    server: '.server-text.dropend',
    cpu: '.server-cpu-text.dropend',
    ram: '.server-ram-text.dropend',
    disk: '.server-disk-text.dropend',
    apps: '.server-apps-text.dropend',
    net: '.server-network-text.dropup',
}

export function setChartData(xLabels, dataLabels, data) {
    let datasets = [];

    for (let i = 0, x = 0, y = 1; i < data.length; i++, x += 3, y += 3) {
        datasets.push({
            label: dataLabels[i],
            backgroundColor: COLOR_PALLET[x],
            borderColor: COLOR_PALLET[y],
            data: data[i],
        });
    }

    return {
        labels: xLabels,
        datasets: datasets
    }

}

export function setChartConfig(
    title="",data=undefined, callback=undefined,
    type="line", responsive=true,
    position="top", size=14) {
    return  {
        type: type,
        data: data,
        options: {
            animation: {
                duration: 0,
            },
            maintainAspectRatio: false,
            responsive: responsive,
            plugins: {
                legend: {
                    position: position,
                    labels: {
                        color: "black",
                        font: {
                            size: size,
                        }
                    }
                },
                title: {
                    color: "black",
                    display: true,
                    text: title,
                    font: {
                        size: size
                    }
                },
            },
        }
    };
}

export async function chartUpdate(urlId, charts) {
    const url = document.getElementById(urlId).getAttribute('data-url');
    const newData = await fetch(url, {
        method: HTTP_METHODS.get, headers: HEADERS
    }).then(async response => await response.json());
    
    function removeData(chart) {
        chart.data.labels.pop();
        chart.data.datasets.forEach(dataset => {
            dataset.data.pop();
        });
        chart.update();
    }

    function addData(chart, label, data) {
        chart.labels.push(label);
        chart.data.datasets.forEach(dataset => {
            dataset.data.push(data);
        });
        chart.update();
    }

    charts.forEach((chart, i=0) => {
        chart.config.data = newData['chartData'][i];
        chart.update();
    })
}

export function chartGenerator(chartId, config) {
    const containerBody = document.querySelector('#chartBox');

    let canvas = document.createElement('canvas');
    canvas.setAttribute('id', chartId);
    containerBody.append(canvas);

    const context = document.getElementById(chartId).getContext('2d');
    const chart = new Chart(context, config);

    // const totalLabels = chart.data.labels.length;
    // const maxLabelsWidth = 100;
    // const containerChart = document.querySelector('.container-chart');
    //
    //
    // if (totalLabels > maxLabelsWidth) {
    //     containerChart.style.overflowX = "scroll";
    //     const newWidth = (containerBody.style.width + (totalLabels - maxLabelsWidth) * 30);
    //     containerBody.style.width = `${newWidth}px`;
    // }
    // else {
    //     containerChart.style.overflowX = "hidden";
    // }

    return chart;
}

export function convertBytesToMetric(amountStr) {
    let amount = parseInt(amountStr);

    if (amount >= 0 && amount < 1000) {
        return `${amount}B`;
    }
    else if (amount >= 1000 && amount < 1_000_000) {
        return `${(amount / 1000).toFixed(2)}KB`;
    }
    else if (amount >= 1_000_000 && amount < 1_000_000_000) {
        return `${(amount / 1000 ** 2).toFixed(2)}MB`;
    }
    else if (amount >= 1_000_000_000 && amount < 1_000_000_000_000){
        return `${(amount / 1000 ** 3).toFixed(2)}GB`;
    } else {
        return `${(amount / 1000 ** 4).toFixed(2)}TB`;
    }
}
