$(document).ready(function () {
    function makeServerNode(hostname) {
        let newDiv = document.createElement('div');
        let host = document.createTextNode(hostname);
        newDiv.appendChild(host);
        newDiv.id = hostname;
        newDiv.addEventListener('mousemove', (e) => {
            newDiv.title = 'test'
        })
        newDiv.addEventListener('mouseout', (e) => {
            newDiv.title = ''
        })
        return newDiv;
    }

    function drawTable(data, firstCall) {
        let parsedData = JSON.parse(data);
        let servers = document.getElementById('servers');
        const serversElementsArray = parsedData.map(el => makeServerNode(el.hostname));

        if (firstCall) {
            serversElementsArray.forEach(el => servers.appendChild(el))
        } else {
            serversElementsArray.forEach(el => el.innerHTML)
        }
    }

    const getMetrics = async (url, method, headers) => {
        let response = await fetch(url, {
            method: method, headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            }
        });

        return await response.json();
    };

    async function inspectServers(firstCall) {
        let data = await getMetrics("processes/", "GET")
        drawTable(data, firstCall)
    }

    let start = new Promise(async () => {
        await inspectServers(true)
    })
    
    setInterval(inspectServers, 5000);
})