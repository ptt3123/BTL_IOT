let xValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
let tempValues = [25.8, 25.8, 25.8, 25.8, 25.8, 25.8, 25.8, 25.8, 25.8, 25.8];
let humidityValues = [79, 79, 79, 79, 79, 79, 79, 79, 79, 79];
let lightValues = [495, 495, 495, 495, 495, 495, 495,495, 495, 495];

// chart
const ctx = document.getElementById("myChart").getContext("2d");
const myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [
      {
        label: "Temperature",
        data: tempValues,
        borderColor: "orange",
        fill: false,
        yAxisID: "y-axis-1",
      },
      {
        label: "Humidity",
        data: humidityValues,
        borderColor: "blue",
        fill: false,
        yAxisID: "y-axis-1",
      },
      {
        label: "Light",
        data: lightValues,
        borderColor: "yellow",
        fill: false,
        yAxisID: "y-axis-2",
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
        {
          id: "y-axis-2",
          type: "linear",
          position: "right",
          ticks: {
            min: 0,
            max: 1000,
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

  if(data.type == "hw"){
    const icons = document.querySelectorAll('.hicon');
        console.log(data);
        if(data.fan == "on"){
            icons[0].style.color = "#287bff";
        } else {
            icons[0].style.color = "#999";
        }

        if(data.led == "on"){
            icons[1].style.color = "#287bff";
        } else {
            icons[1].style.color = "#999";
        }

        if(data.con == "on"){
            icons[2].style.color = "#287bff";
        } else {
            icons[2].style.color = "#999";
        }

  } else {

    let tim = data.tim;
    let tem = data.tem;
    let hum = data.hum;
    let lig = data.lig;
  
    // Cập nhậ giá trị
    xValues.push(tim);
    tempValues.push(tem);
    humidityValues.push(hum);
    lightValues.push(lig);
  
    if (xValues.length > 10) {
      xValues.shift();
    }
    if (tempValues.length > 10) {
      tempValues.shift();
    }
    if (humidityValues.length > 10) {
      humidityValues.shift();
    }
    if (lightValues.length > 10) {
      lightValues.shift();
    }
  
    //Cập nhật màu
    let alphat = tem / 100;
    if(alphat < 0.5){
      alphat += 0.2
    }
    document.querySelector(
      ".card.temperature"
    ).style.backgroundColor = `rgba(255, 165, 0, ${alphat})`;
    let alphah = hum / 100;
    if(alphah < 0.5){
      alphah += 0.2
    }
    document.querySelector(
      ".card.humidity"
    ).style.backgroundColor = `rgba(0, 0, 255, ${alphah})`;
    let alphal = lig / 1000;
    if(alphal < 0.5){
      alphal += 0.2
    }
    document.querySelector(
      ".card.light"
    ).style.backgroundColor = `rgba(255, 255, 0, ${alphal})`;
  
    // Cập nhật biểu đồ
    myChart.data.labels = xValues;
    myChart.data.datasets[0].data = tempValues;
    myChart.data.datasets[1].data = humidityValues;
    myChart.data.datasets[2].data = lightValues;
    myChart.update();
  }
};

function sendMessage(hw) {
      let message = { "hw": hw };
      socket.send(JSON.stringify(message));
}