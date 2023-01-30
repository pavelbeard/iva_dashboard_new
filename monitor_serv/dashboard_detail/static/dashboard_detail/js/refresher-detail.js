// TODO: Переедет в файл уровня детализации
function netAnalysisDetail(data, host) {
    let status = data[0]["interface"] !== undefined;
    let cmdNotFound = data[0]["command_not_found"] !== undefined

    // status

    host.childNodes[3].childNodes[9].style.backgroundColor = status ? "#69ff4e" : cmdNotFound ? "#ff0000" : "#bebdbd";
    host.childNodes[3].childNodes[9].childNodes[2].textContent = status ? "UP" : cmdNotFound ? "DOWN" : "iftop n/a";

    if (status) {
        //int
        let iface = status ? data[0]["interface"] : "";

        //-5 elems
        let lastFiveElems = data.slice(-5,);
        let allRate = "".concat(lastFiveElems
            .map(el => `${Object.keys(el)[0]}: last2s: ${Object.values(el)[0].last2s} | last10s: ${Object.values(el)[0].last10s} | last40s: ${Object.values(el)[0].last40s}`))
            .replace(/,/g, '\n');

        let remainingItems = data.slice(1, -5);

        let remainingResult = "".concat(remainingItems.flatMap(el => {
            if (el.from !== undefined) {
                return `from: ${el.from} | last2s: ${el.last2s} | last10s: ${el.last10s} | last40s: ${el.last40s} | cumulative: ${el.cumulative}\n`;
            } else {
                return `to: ${el.to} | last2s: ${el.last2s} | last10s: ${el.last10s} | last40s: ${el.last40s} | cumulative: ${el.cumulative}\n`;
            }
        })).replace(/,/g, "\n");

        host.childNodes[3].childNodes[9].title = `${iface}\n${remainingResult}\n${allRate}`
    }

}