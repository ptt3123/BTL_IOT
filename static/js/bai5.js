let xValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
let wsValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

// chart
const ctx = document.getElementById("myChart").getContext("2d");
const myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [
      {
        label: "WindSpeed",
        data: wsValues,
        borderColor: "black",
        fill: false,
        yAxisID: "y-axis-1",
      },
    ],
  },
  options: {
    legend: { display: true },
    scales: {
      yAxes: [
        {
          id: "y-axis-1",
          type: "linear",
          position: "left",
          ticks: {
            min: 0,
            max: 100,
          },
        },
      ],
    },
  },
});

// websocket
const socket = new WebSocket("ws://localhost:8000/ws");

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
    let tim = data.tim;
    let ws = data.ws;
    console.log(ws)

    // Thay đổi nội dung trong div có class "temperature"
    let valueElement = document.getElementById('value');
    valueElement.innerText = ws + ' M/s';

    let warningIcon = document.getElementById('warning-icon');
    if (ws >= 60) {
    // Thay đổi màu nền (background-color)
    warningIcon.style.backgroundColor = 'red';  // Bạn có thể thay đổi 'red' thành bất kỳ màu nào bạn muốn
    } else {
    warningIcon.style.backgroundColor = 'green';
    }

    // Cập nhậ giá trị
    xValues.push(tim);
    wsValues.push(ws);

    if (xValues.length > 10) {
      xValues.shift();
    }
    if (wsValues.length > 10) {
      wsValues.shift();
    }

    //Cập nhật màu
    let alphat = ws / 100;
    if(alphat < 0.5){
      alphat += 0.2
    }
//    document.querySelector(
//      ".card.temperature"
//    ).style.backgroundColor = `rgba(255, 165, 0, ${alphat})`;


    // Cập nhật biểu đồ
    myChart.data.labels = xValues;
    myChart.data.datasets[0].data = wsValues;
    myChart.update();
};