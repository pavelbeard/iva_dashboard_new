import axios from "axios";
import env from 'react-dotenv';

export const API_URL = env.REACT_APP_BACKEND_URL || "http://127.0.0.1:10111";
export const URL = `${API_URL}/api/v1/prom_data`;
export const APP_VERSION = env.REACT_APP_VERSION || "v0.8.64";

export const HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    "Content-Type": "application/json"
};

const ONE_HOUR_IN_MS = 1 * 60 * 60 * 1000;
const REFRESH_INTERVAL_MS = 2 * 1000;


export const TIME_RANGE_SHORTCUTS = [
    {
        name: 'interval.last.hour',
        intervalMs: ONE_HOUR_IN_MS, custom: false
    },
    {
        name: 'interval.last.3.hours',
        intervalMs: 3 * ONE_HOUR_IN_MS, custom: false
    },
    {
        name: 'interval.last.6.hours',
        intervalMs: 6 * ONE_HOUR_IN_MS, custom: false
    },
    {
        name: 'interval.last.12.hours',
        intervalMs: 12 * ONE_HOUR_IN_MS, custom: false
    },
    {
        name: 'interval.last.day',
        intervalMs: 24 * ONE_HOUR_IN_MS, custom: false
    },
    {
        name: 'interval.last.week',
        intervalMs: 7 * 24 * ONE_HOUR_IN_MS, custom: false
    },
    {
        name: 'interval.last.month',
        intervalMs: 30 * 24 * ONE_HOUR_IN_MS, custom: false
    },
    {
        name: 'interval.custom',
        intervalMs: 0, custom: true
    },
]

const REFRESH_INTERVALS = [

]

export function getResponse(url) {
    return axios.get(url).then(
        async response => {
            if (response.status > 400) {
                throw new Error("Backend responds with error!")
            }
            return await response;
        });
}

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
    return axios.post(url, body)
        .then(async response => {
            if (response.status > 400) {
                throw new Error("Backend responds with error!");
            }
            return await response.data;
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

export const chartConfig = {
    type: 'line',
    data: {
        datasets: [{
            label: '1',
            data: [0,1],
        },{
            data: [1,3],
        },{
            data: [0,1],
        },{
            data: [0,1],
        },]
    },
    options: {

    },
    plugins: [

    ],
}