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
} from 'chart.js';
import {Line} from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
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

const Chart = ({metricName, host, query, name}) => {
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
                beginAtZero: true
            }
        }
    };

    const refreshInterval = useSelector(state => state.refresh.refreshInterval);
    let {startDate, endDate, period, autoupdate} = useSelector(state => state.datetimeManager);
    const [chartData, setChartData] = useState(data);
    const [step, setStep] = useState("1m");

    const changeDate = date => {
        date = new Date(date);
        date.setMinutes(date.getMinutes() + 1);
        return date.toISOString();
    };

    const fetchData = async () => {
        try {
            if (autoupdate) {
                endDate = changeDate(endDate);
                startDate = changeDate(startDate);
            }

            const hours = Math.round((new Date(endDate) - new Date(startDate)) / (60 * 60 * 1000));
            if (hours > 0 && hours <= 1) {
                setStep("1m");
            } else if (hours > 1 && hours <= 3) {
                setStep("2m");
            } else if (hours > 3 && hours <= 6) {
                setStep("4m");
            } else if (hours > 6 && hours <= 12) {
                setStep("8m");
            } else if (hours > 12 && hours <= 24) {
                setStep("15m");
            } else if (hours > 24 && hours <= (24 * 7)) {
                setStep("30m");
            } else if (hours > (24 * 7) && hours <= (24 * 30)) {
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
                if (hours > 24) {
                    labels = result[0].values.map(v => new Date(v[0] * 1000).toLocaleString());
                } else {
                    labels = result[0].values.map(v => new Date(v[0] * 1000).toLocaleTimeString());
                }

                const datasets = result.map((dataset, i = 0) => {
                    const colorPaletteElement = COLOR_PALETTE[i];

                    return {
                        label: dataset.metric.mode || "",
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
    }, [refreshInterval, startDate, endDate, step, period]);

    return (
        <>
            <div className="container-fluid ps-5 pt-3">{name}  {startDate} </div>
            <div className="ps-5 pt-1 pe-5">
                <Line data={chartData}
                      options={{...options, maintainAspectRatio: false}}
                      width={100}
                      height={350}/>
            </div>
        </>
    );
    // return <div>CHART</div>;
};

export default Chart;