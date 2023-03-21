import axios from "axios";

export const URL = `${process.env.REACT_APP_BACKEND_URL}/api/v1/prom_data`;

export const HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    "Content-Type": "application/json"
};

// {method: "GET", headers: HEADERS }

export function getData(url) {
    return axios.get(url)
        .then(async response => {
            if (response.status > 400) {
                throw new Error("Backend responds with error!");
            }
            return await response.data;
        })
        .catch(err => console.log(err));
}

export function postData(url, body) {
    return fetch(url, {method: "POST", headers: HEADERS, body: JSON.stringify(body)})
        .then(async response => {
            if (response.status > 400) {
                throw new Error("Backend responds with error!");
            }
            return await response.json();
        })
        .catch(async err => console.log(err));
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