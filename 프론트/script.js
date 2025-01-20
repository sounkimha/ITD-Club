const apiKey = "UD7C7A3QU6JVD62L"; // Alpha Vantage 또는 다른 API 키를 입력하세요.
const apiUrl = "https://www.alphavantage.co/query"; // Alpha Vantage API

const stockChart = document.getElementById('stockChart').getContext('2d');
let chart; // 차트를 저장하는 변수

// 차트 초기화 함수
function initializeChart() {
    return new Chart(stockChart, {
        type: 'line',
        data: {
            labels: [], // 날짜를 저장
            datasets: [{
                label: 'Stock Price',
                data: [], // 가격 데이터를 저장
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });
}

// 주식 데이터 가져오기
async function fetchStockData(stockCode) {
    try {
        const response = await fetch(`${apiUrl}?function=TIME_SERIES_DAILY&symbol=${stockCode}&apikey=${apiKey}`);
        const data = await response.json();

        if (data["Error Message"]) {
            alert("Invalid stock code or no data found.");
            return null;
        }

        const timeSeries = data["Time Series (Daily)"];
        const dates = Object.keys(timeSeries).reverse(); // 최신 날짜가 먼저 오므로 반전
        const prices = dates.map(date => parseFloat(timeSeries[date]["4. close"])); // 종가

        return { dates, prices };
    } catch (error) {
        console.error("Error fetching stock data:", error);
        alert("Failed to fetch stock data. Please try again.");
        return null;
    }
}

// 차트 업데이트
function updateChart(chart, dates, prices) {
    chart.data.labels = dates;
    chart.data.datasets[0].data = prices;
    chart.update();
}

// 버튼 클릭 이벤트
document.getElementById('fetchData').addEventListener('click', async () => {
    const stockCode = document.getElementById('stockCode').value.toUpperCase();

    if (!stockCode) {
        alert("Please enter a stock code.");
        return;
    }

    const stockData = await fetchStockData(stockCode);

    if (stockData) {
        updateChart(chart, stockData.dates, stockData.prices);
    }
});

// 초기 차트 생성
chart = initializeChart();

// 이슈 알림 처리
const alerts = [
    "Stock XYZ reached a new high of $160!",
    "Market volatility detected in Tech sector.",
    "Economic report to be released tomorrow."
];

const alertsList = document.getElementById('alerts');
alerts.forEach(alert => {
    const li = document.createElement('li');
    li.textContent = alert;
    alertsList.appendChild(li);
});
