 //$(document).ready(function(){
 //   $('#getData').hide();
 //    getIndex();
 //});


 function getData(){

     var searchValue = $('#searchText').val();
     if(searchValue  !== ''){
          $.ajax({
             url: "getIndex",
             type: 'POST',
             data: {searchValue : searchValue, index:0}
          })
          .done(function(response){
             $('#getData').html(response);
             getVisualization(searchValue);
          });
        $('#getData').show();
     }else{
         alert("Please enter the keyword to search");
     }


 }

 function getVisualization (searchValue){
          var totalNewData = $('#totalNewData').val();
          var positiveData = $('#positiveCountArr').val();
          var negativeData = $('#negativeCountArr').val();
          totalNewData = JSON.parse(totalNewData);
          positiveData = JSON.parse(positiveData);
          negativeData = JSON.parse(negativeData);
          var totalArray = {totalDataArray :[],positiveData : [], negativeData : []};

          for ( i =0 ; i < totalNewData.length; i++){
            totalArray.totalDataArray.push(totalNewData[i]);
          }

          for ( i =0 ; i < positiveData.length; i++){
            totalArray.positiveData.push(positiveData[i])
          }

          for ( i =0 ; i < negativeData.length; i++){
            totalArray.negativeData.push(negativeData[i])
          }

          if ($('#AreaChart').length) {
               var ctx = document.getElementById('AreaChart').getContext('2d');

               var gradientStroke1 = ctx.createLinearGradient(0, 0, 0, 300);
                gradientStroke1.addColorStop(0, '#4facfe');
                gradientStroke1.addColorStop(1, '#00f2fe');

               var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['','Positive', 'Negative',''],
                        datasets: [{
                            label: 'Tweets',
                            data: ['',totalArray.totalDataArray[0],totalArray.totalDataArray[1],''],
                            backgroundColor: 'rgba(94, 114, 228, 0.3)',
                            borderColor: '1a4089',
                            borderWidth: 3
                        }]
                    }
                });
		    }

          if ($('#lineChart').length) {
                var ctx = document.getElementById('lineChart').getContext('2d');
                var myChart = new Chart(ctx, {
                   type: 'line',
                    data: {
                        labels: ['', '','','','','','',''],
                        datasets: [{
                            label: 'Positive',
                            data: totalArray.positiveData,
                            backgroundColor: "transparent",
                            borderColor: "#2dce89",
                            borderWidth: 3

                        }, {
                            label: 'Negative',
                            data: totalArray.negativeData,
                            backgroundColor: "transparent",
                            borderColor: "#ff2fa0",
                            borderWidth: 3

                        }]
                    }
                });
		    }

          if ($('#barChart').length) {
			var ctx = document.getElementById("barChart").getContext('2d');
			var myChart = new Chart(ctx, {
				type: 'bar',
				data: {
					labels: ['Tweets'],
					datasets: [{
						label: 'Postive',
						data: [totalArray.totalDataArray[0]],
						backgroundColor: "#ff2fa0"
					}, {
						label: 'Negative',
						data: [totalArray.totalDataArray[1]],
						backgroundColor: "1a4089"
					}]
				}, options: {
				  scales: {
				    xAxes: [{
				    	barPercentage: .7
				    	 }]
				  }
				}
			});
          }

          var c3PieChart = c3.generate({
            bindto: '#c3-pie-chart',
            data: {
              // iris data from R
              columns: [
               ["Posiive", totalArray.totalDataArray[0]],
                ["Negative", totalArray.totalDataArray[1]]
              ],
              type: 'pie',
              onclick: function(d, i) {
                console.log("onclick", d, i);
              },
              onmouseover: function(d, i) {
                console.log("onmouseover", d, i);
              },
              onmouseout: function(d, i) {
                console.log("onmouseout", d, i);
              }
            },
            color: {
                pattern: ['1a4089','#2dce89','#11cdef']
            },
            padding: {
                top: 0,
                right:0,
                bottom:30,
                left: 0
            }
          });

          setTimeout(function() {
            c3PieChart.load({
              columns: [
                ["Posiive", totalArray.totalDataArray[0]],
                ["Negative", totalArray.totalDataArray[1]]
                ]
            });
          }, 1500);

          setTimeout(function() {
            c3PieChart.unload({
              ids: 'data1'
            });
            c3PieChart.unload({
              ids: 'data2'
            });
          }, 2500);

          totalArray.positiveData[0] = "Positive";
          totalArray.negativeData[0] = "Negative";
          console.log(totalArray)
          var c3LineChart = c3.generate({
            bindto: '#c3-line-chart',
            data: {
              columns: [
                totalArray.positiveData,
                totalArray.negativeData
              ]
            },
            color: {
                pattern: ['1a4089','#2dce89','#11cdef']
            },
            padding: {
                top: 0,
                right:0,
                bottom:30,
                left: 0
            }
          });


          //setTimeout(function() {
          //  c3LineChart.load({
          //    columns: [
          //      ['data1', 230, 190, 300, 500, 300, 400]
          //    ]
          //  });
          //}, 1000);
          //
          //setTimeout(function() {
          //  c3LineChart.load({
          //    columns: [
          //      ['data3', 130, 150, 200, 300, 200, 100]
          //    ]
          //  });
          //}, 1500);
          //
          //setTimeout(function() {
          //  c3LineChart.unload({
          //    ids: 'data1'
          //  });
          //}, 2000);


     setInterval(function(){
           var indexWithSelector = $(".nav-link").filter(".active").index(".nav-link");
          $.ajax({
             url: "Analysis/getIndex",
             type: 'POST',
             data: {searchValue : searchValue, index:indexWithSelector}
          })
          .done(function(response){
             $('#getData').html(response);
             getVisualization();
          });
     }, 60000);
 }