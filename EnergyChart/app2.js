var chartColors = {
    yellow: 'rgb(255, 205, 86)', 
    orange: 'rgb(255, 159, 64)',
    smoothOrange :'rgb(255, 159, 64,0.7)',
    smoothYellow: 'rgb(255, 220, 86)',
    grey: 'rgb(150,150,150,0.8)'
   
  };
  
  var roundNumber = function (num, scale) {
    var number = Math.round(num * Math.pow(10, scale)) / Math.pow(10, scale);
    if(num - number > 0) {
      return (number + Math.floor(2 * Math.round((num - number) * Math.pow(10, (scale + 1))) / 10) / Math.pow(10, scale));
    } else {
      return number;
    }
  };

  var origLineElement = Chart.elements.Line;
  

  Chart.elements.Line = Chart.Element.extend({
    draw: function() {
      var vm = this._view;
      var backgroundColors = this._chart.controller.data.datasets[this._datasetIndex].backgroundColor;
      var points = this._children;
      var ctx = this._chart.ctx;
      var minX = points[0]._model.x;
      var maxX = points[points.length - 1]._model.x;
      var linearGradient = ctx.createLinearGradient(minX, 0, maxX, 0);
  
      // iterate over each point to build the gradient
      points.forEach(function(point, i) {
        // `addColorStop` expects a number between 0 and 1, so we
        // have to normalize the x position of each point between 0 and 1
        // and round to make sure the positioning isn't too percise 
        // (otherwise it won't line up with the point position)
        var colorStopPosition = roundNumber((point._model.x - minX) / (maxX - minX), 2);
  
        // special case for the first color stop
        if (i === 0) {
          linearGradient.addColorStop(0, backgroundColors[i]);
        } else {
          // only add a color stop if the color is different
          if (backgroundColors[i] !== backgroundColors[i-1]) {
            // add a color stop for the prev color and for the new color at the same location
            // this gives a solid color gradient instead of a gradient that fades to the next color
            linearGradient.addColorStop(colorStopPosition, backgroundColors[i - 1]);
            linearGradient.addColorStop(colorStopPosition, backgroundColors[i]);
          }
        }
      });
  
    
      vm.backgroundColor = linearGradient;
  

      origLineElement.prototype.draw.apply(this);
    }               
  });
  
  Chart.controllers.line = Chart.controllers.line.extend({
    datasetElementType: Chart.elements.Line,
  });
  

  var labels = ["Octobre","Novembre", "Décembre", "Janvier", "Février", "Mars", "Avril","Mai"];
  var fillColors = [chartColors.smoothYellow,  chartColors.smoothYellow, chartColors.smoothYellow,chartColors.smoothYellow,chartColors.smoothYellow,chartColors.orange, chartColors.orange];
  
  var ctx = document.getElementById("myChart").getContext("2d");

    Promise.all([
        fetch('https://raw.githubusercontent.com/IsmailBarkani/COD/master/JSON/EnergyElectOct19.json?token=AKNCG7DLMI23QBRQJODJRZK7PIYD6').then(resp => resp.json()),
        fetch('https://raw.githubusercontent.com/IsmailBarkani/COD/master/JSON/EnergyElectNov19.json?token=AKNCG7FX5IEAF2DHX3T4CZC7PI34K').then(resp => resp.json()),
        fetch('https://raw.githubusercontent.com/IsmailBarkani/COD/master/JSON/EnergyElectDec19.json?token=AKNCG7C6XUXJTBLWBA4TY6K7PI362').then(resp => resp.json()),
        fetch('https://raw.githubusercontent.com/IsmailBarkani/COD/master/JSON/EnergyElectFev20.json?token=AKNCG7HUBCLKKIGUOI5TD3S7PI4AI').then(resp => resp.json()),
        fetch('https://raw.githubusercontent.com/IsmailBarkani/COD/master/JSON/EnergyElectMars20.json?token=AKNCG7HNQIGOTK6DLQ34BTK7PI4BC').then(resp => resp.json()),
        fetch('https://raw.githubusercontent.com/IsmailBarkani/COD/master/JSON/EnergyElectAvril20.json?token=AKNCG7GMUPWTVG7TMW6QGRK7PI4CI').then(resp => resp.json())
      ]).then(data => {
        console.log
        var DATA_OCT = 0
        var DATA_NOV = 0
        var DATA_DEC = 0
        var DATA_JAN = 0
        var DATA_FEV = 0
        var DATA_MAR = 0
        var DATA_AVR = 0

         

    for(var j=0; j<data[0].consolidated_energy_consumption[0].values.length;j++){
        DATA_OCT += data[0].consolidated_energy_consumption[0].values[j].value/data[0].consolidated_energy_consumption[0].values.length
    } 
    for(var j=0; j<data[1].consolidated_energy_consumption[0].values.length;j++){
        DATA_NOV += data[1].consolidated_energy_consumption[0].values[j].value/data[1].consolidated_energy_consumption[0].values.length
    } 
    for(var j=0; j<data[2].consolidated_energy_consumption[0].values.length;j++){
        DATA_DEC += data[2].consolidated_energy_consumption[0].values[j].value/data[2].consolidated_energy_consumption[0].values.length

        DATA_JAN = DATA_DEC
    } 
    for(var j=0; j<data[3].consolidated_energy_consumption[0].values.length;j++){
        DATA_FEV += data[3].consolidated_energy_consumption[0].values[j].value/data[3].consolidated_energy_consumption[0].values.length
    } 
    for(var j=0; j<data[4].consolidated_energy_consumption[0].values.length;j++){
        DATA_MAR += data[4].consolidated_energy_consumption[0].values[j].value/data[4].consolidated_energy_consumption[0].values.length
    } 
    for(var j=0; j<data[5].consolidated_energy_consumption[0].values.length;j++){
        DATA_AVR += data[5].consolidated_energy_consumption[0].values[j].value/data[5].consolidated_energy_consumption[0].values.length
    } 
    var lineData = [DATA_OCT.toFixed(2),DATA_NOV.toFixed(2),DATA_DEC.toFixed(2),DATA_JAN.toFixed(2),DATA_FEV.toFixed(2),DATA_MAR.toFixed(2),DATA_AVR.toFixed(2)]
        
    
    // Creation the chart
    var myLine = new Chart(ctx, {
            type: 'line',
            data: {
              labels: labels,
              datasets: [{
                label: "Consommation en MW",
                backgroundColor: fillColors, // now we can pass in an array of colors (before it was only 1 color)
                borderColor: chartColors.grey,
                pointBackgroundColor: fillColors,
                pointBorderWidth : 4,
                fill: true,
                data: lineData,
              }]
            },
            options: {
              responsive: true,
              title: {
                display: true,
                fontSize : 18,
                text:'Consommation d\'Energie Electrique en France 2019 - 2020 (en MWh)'
              },
              legend: {
                display: false,
              },
              scales: {
                xAxes: [{
                  gridLines: {
                    offsetGridLines: true
                  },
                 
                }],
              }
            }
          })
        
      })

    
  

 
  