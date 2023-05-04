import {useEffect, useState} from "react";
import {API_URL, CONFIG} from "../../../base";
import axios from "axios";
import {useSelector} from "react-redux";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    TimeScale
} from 'chart.js';
import {Line} from "react-chartjs-2";
// import ChartDateFns from "chartjs-adapter-date-fns";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    TimeScale
);

const COLOR_PALETTE =
    ['#AEDCDA', '#97D0A7', '#BCDA78',
    '#E6CD69', '#7AA6D7', '#E2B53E',
    '#FFE001', '#63BA97', '#D38895',
    '#EF9F26', '#DD6BA7', '#857868',
    '#E47A0A', '#DE6277', '#0091A0',
    '#509D28', '#6A6A68', '#DD3F4E',
    '#9C58A1', '#386373', '#1D57A9',
    '#006347', '#425D10', '#AC0123',
    '#56187D', '#411747', '#010101'];

const Chart = ({metricName, host, query, name, metricMeasure}) => {
    const data = {
        labels: [],
        datasets: [{
            label: metricName,
            data: [],
            fill: false,
            borderColor: "#c4b2b2"
        }]
    };

    const options = {
        scales: {
            y: {
                ticks: {
                    callback: function (value, index, ticks) {
                        return this.getLabelForValue(value) + " " + metricMeasure;
                    }
                },
                beginAtZero: true
            },
            x: {
                ticks: {
                    maxRotation: 0,
                    callback: function (value, index, ticks) {
                        return this.getLabelForValue(value).slice(0, -3) ;
                    }
                },

            }
        },
        plugins: {
            title: {
                display: true,
                text: name
            }
        }
    };

    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    let {startDate, endDate, period} = useSelector(state => state.datetimeManager);
    const autoupdate = useSelector(state => state.datetimeManager.autoupdate);
    const [chartData, setChartData] = useState(data);
    const [step, setStep] = useState("1m");

    const fetchData = async () => {
        try {
            let hoursPeriod;
            switch (period) {
                case "3h": hoursPeriod = 3; break;
                case "6h": hoursPeriod = 6; break;
                case "12h": hoursPeriod = 12; break;
                case "1d": hoursPeriod = 24; break;
                case "1w": hoursPeriod = 24 * 7; break;
                case "1m": hoursPeriod = 24 * 30; break;
                case "custom": hoursPeriod = undefined; break;
                default: hoursPeriod = 1; break;
            }

            if (autoupdate) {
                startDate = new Date();
                startDate.setHours((startDate.getHours() + 3) - hoursPeriod);
                startDate = startDate.toISOString();

                endDate = new Date();
                endDate.setHours(endDate.getHours() + 3);
                endDate = endDate.toISOString();
            }

            let hoursDifference;
            if (!(hoursPeriod === undefined || hoursPeriod === 1)) {
                startDate = new Date(startDate);
                startDate.setHours(startDate.getHours() - hoursPeriod);
                startDate = startDate.toISOString();
            }

            hoursDifference = Math.round((new Date(endDate) - new Date(startDate)) / (60 * 60 * 1000));

            if (hoursDifference > 0 && hoursDifference <= 0.5) {
                setStep("15s");
            } else if (hoursDifference > 0.5 && hoursDifference <= 1) {
                setStep("1m");
            } else if (hoursDifference > 1 && hoursDifference <= 3) {
                setStep("2m");
            } else if (hoursDifference > 3 && hoursDifference <= 6) {
                setStep("4m");
            } else if (hoursDifference > 6 && hoursDifference <= 12) {
                setStep("8m");
            } else if (hoursDifference > 12 && hoursDifference <= 24) {
                setStep("15m");
            } else if (hoursDifference > 24 && hoursDifference <= (24 * 7)) {
                setStep("30m");
            } else if (hoursDifference > (24 * 7) && hoursDifference <= (24 * 30)) {
                setStep("1h");
            }

            const urlRequest = `${API_URL}/api/v1/prom_data`
                + `?query=${encodeURI(query)}`
                + `&host=${host}`
                + `&start=${startDate}`
                + `&end=${endDate}`
                + `&step=${step}`
                + `&query_range=true`;
            const response = (await axios(urlRequest, CONFIG)).data;
            const result = response?.data.result;

            if (result?.length > 0) {
                let labels;
                if (hoursDifference >= 24) {
                    labels = result[0].values.map(v => new Date(v[0] * 1000).toLocaleString());
                } else {
                    labels = result[0].values.map(v => new Date(v[0] * 1000).toLocaleTimeString());
                }

                const datasets = result.map((dataset, i = 0) => {
                    const colorPaletteElement = COLOR_PALETTE[i];

                    return {
                        label: dataset.metric.mode || dataset.metric.__name__ + " {" + (dataset.metric.device || "") + "}",
                        data: dataset.values.map(v => parseFloat(v[1]).toFixed(2)),
                        borderColor: colorPaletteElement
                    }
                });

                setChartData({
                    ...data,
                    labels: labels,
                    datasets: datasets
                });
            }
        } catch (err) {
            console.log(`${fetchData.name}: что-то тут не так...`)
        }
    };

    const fetchDataImmediately = () => {
        setTimeout(fetchData, 0);
    };

    useEffect(() => {
        fetchDataImmediately();
        const interval = setInterval(fetchDataImmediately, refreshInterval);
        return () => clearInterval(interval)
    }, [refreshInterval, startDate, endDate, step, period, autoupdate, host]);

    return (
        <div className="ps-5 pt-1 pe-5">
            <Line data={chartData}
                  options={{...options, maintainAspectRatio: false}}
                  width={100}
                  height={350}/>
        </div>
    );
    // return <div>CHART</div>;
};

export default Chart;