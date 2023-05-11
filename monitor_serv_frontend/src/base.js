import env from 'react-dotenv';

export const API_URL = env?.REACT_APP_BACKEND_URL || "http://127.0.0.1:10111";
export const IVCS_API_URL = env?.REACT_APP_IVCS_API_URL || "http://127.0.0.1:10111";
export const URL = `${API_URL}/api/v1/prom_data`;
export const APP_VERSION = env?.REACT_APP_VERSION || "v0.9.6";

export const CONFIG  = {
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
};

export function fadeOut() {
    return {
        opacity: "0",
        transition: "all 250ms linear 2s"
    }
}

export function sum(arr) {
    if (!(arr instanceof Array))
        return undefined;

    let total = 0;

    for (let i of arr) {
        if (isNaN(i))
            continue;

        total += i;
    }

    return total;
}

export function parse (key) {
    try {
        return JSON.parse(localStorage[key]);
    } catch (err) {
        return undefined;
    }
}

export const setColor = (e, color) => {
    e.target.style.color = color;
}

String.prototype.partition = function (separator) {
    const arr = this.split(separator);
    const index = arr.findIndex(item => item === separator);
    return arr.reduce((acc, item, i) => {
        if (i < index) {
            acc[0].push(item);
        } else if (i > index) {
            acc[1].push(item)
        }
        return acc;
    }, [[], []]);
}