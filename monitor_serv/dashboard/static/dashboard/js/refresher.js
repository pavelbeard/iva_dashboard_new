function processesData(data) {
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
        return `${el.service}: ${el.status}${st}`
    });
    return "".concat(processesArray).replaceAll(',', '\n')
}

function makeServerNode(hostname, data, id, callback) {
    let oldHost = document.getElementById(id);
    if (oldHost != null)
        oldHost.remove();

    let newDiv = document.createElement('div');
    let host = document.createTextNode(hostname);

    newDiv.appendChild(host);
    newDiv.id = id;
    newDiv.addEventListener('mousemove', (e) => {
        newDiv.title = callback(data)
    });
    newDiv.addEventListener('mouseout', (e) => {
        newDiv.title = ''
    });
    newDiv.setAttribute('data-toggle', 'tooltip');
    newDiv.setAttribute('data-placement', 'right');

    return newDiv;
}

function drawTable(data, callback) {
    let parsedData = JSON.parse(data);
    let servers = document.getElementById('servers');
    const serversElementsArray = parsedData.map(el => makeServerNode(el.hostname, el.data, el.id, callback));

    serversElementsArray.forEach(el => servers.appendChild(el))

    $('[data-toggle="tooltip"]').tooltip();
}

async function getMetrics (url, method, headers) {
    let response = await fetch(url, {
        method: method, headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
        }
    });

    return await response.json();
}

async function inspectServers() {
    let data = await getMetrics("processes/", "GET");
    drawTable(data, processesData);
}

// main //
document.onload = async () => await inspectServers()
setInterval(inspectServers, 5000);
// main //