d1=document.getElementById('famousproduct').innerHTML
data1=d1.split(',');
console.log(data1);
const xValues = [data1[1],data1[3],data1[5], data1[7], data1[9],'o'];
const yValues = [parseInt(data1[0]), parseInt(data1[2]), parseInt(data1[4]), parseInt(data1[6]), parseInt(data1[8]),0];
const barColors = ['',"red", "green","blue","orange","brown"];

new Chart("myBarChart", {
  type: "bar",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    legend: {display: false},
    title: {
      display: true,
      text: "Top Products Of Month"
    }
  }
});



//         graph for the toral earnning in months

d=document.getElementById('totalProfit').innerText;
data=d.split(',');
const xxValues = ['0','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const yyValues = [0,parseInt(data[0]),parseInt(data[1]),parseInt(data[2]),parseInt(data[3]),parseInt(data[4]),
parseInt(data[5]),parseInt(data[6]),parseInt(data[7]),parseInt(data[8]),parseInt(data[9]),parseInt(data[10]),parseInt(data[11])];

new Chart("myChart", {
  type: "line",
  data: {
    labels: xxValues,
    datasets: [{
      fill: false,
      lineTension: 0,
      backgroundColor: "rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: yyValues
    }]
  },
  options: {
    legend: {display: false},
    // scales: {
    //    yAxes: [{ticks: {min: 6, max:16}}],
    // },
    title: {
      display: true,
      text: "Total profit"
    }
    
  }
});





d3=document.getElementById('categoryProducts').innerText;
data3=d3.split(',');
const x_Values = ["Fashion", "Daily Use", "Cosmatics", "Toy"];
const y_Values = [parseInt(data3[0]), parseInt(data3[1]), parseInt(data3[2]), parseInt(data3[3])];
const b_arColors = [
  "#b91d47",
  "#00aba9",
  "#2b5797",
  "#e8c3b9"
];

new Chart("userChart", {
  type: "pie",
  data: {
    labels: x_Values,
    datasets: [{
      backgroundColor: b_arColors,
      data: y_Values
    }]
  },
  options: {
    title: {
      display: true,
      text: "World Wide Wine Production 2018"
    }
  }
});



