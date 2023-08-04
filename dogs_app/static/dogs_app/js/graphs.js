    const loadingElement = document.getElementById('loading');
        var detailedData_with_kong = [];
        var detailedData_without_kong = [];

        function onBarClick(chart, event, array) {
            if (array[0]) {
                var index = array[0]._index;
                var chartData = array[0]._chart.config.data;
                var label = chartData.labels[index];
                var dataSet = chartData.datasets[0];
                var dataItem = dataSet.data[index];
                var detailedData;
                if (chart.canvas.id === 'chart_dogStances_with_kong') {
                    detailedData = detailedData_with_kong[index];
                } else if (chart.canvas.id === 'chart_dogStances_without_kong') {
                    detailedData = detailedData_without_kong[index];
                }
                alert(`You clicked on stance ${label} with count ${dataItem}.\nDetailed data: ${JSON.stringify(detailedData)}`);
            }
        }

        function createChartOfEngagement(data_with_kong, data_without_kong) {
    var ctx_engagement = document.getElementById('chart_duration_of_engagement').getContext('2d');
    // Convert date strings to Date objects
    var labels_with_kong = data_with_kong.map(item => {
        var parts = item.date.split("-");
        return new Date(parts[0], parts[1] - 1, parts[2]);
    });
    var labels_without_kong = data_without_kong.map(item => {
        var parts = item.date.split("-");
        return new Date(parts[0], parts[1] - 1, parts[2]);
    });

    new Chart(ctx_engagement, {
        type: 'line',
        data: {
            labels: labels_with_kong, // Update here
            datasets: [
                {
                    label: 'With Kong',
                    data: data_with_kong.map(item => item.total),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 2
                },
                {
                    label: 'Without Kong',
                    data: data_without_kong.map(item => item.total),
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Duration of Engagement',
                fontSize: 24
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

        function fetchDataAndCreateCharts() {
            fetch(chartDataUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("HTTP error " + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    var ctx_with_kong = document.getElementById('chart_dogStances_with_kong').getContext('2d');
                    var ctx_without_kong = document.getElementById('chart_dogStances_without_kong').getContext('2d');
                    var ctx_breeds = document.getElementById('chart_dogBreeds').getContext('2d');

                    var gradient_with_kong = ctx_with_kong.createLinearGradient(0, 0, 0, 400);
                    gradient_with_kong.addColorStop(0, 'rgba(75, 192, 192, 1)');
                    gradient_with_kong.addColorStop(1, 'rgba(75, 192, 192, 0.5)');

                    var gradient_without_kong = ctx_without_kong.createLinearGradient(0, 0, 0, 400);
                    gradient_without_kong.addColorStop(0, 'rgba(255, 99, 132, 1)');
                    gradient_without_kong.addColorStop(1, 'rgba(255, 99, 132, 0.5)');

                    var gradient_breeds = ctx_breeds.createLinearGradient(0, 0, 0, 400);
                    gradient_breeds.addColorStop(0, 'rgba(153, 102, 255, 1)');
                    gradient_breeds.addColorStop(1, 'rgba(153, 102, 255, 0.5)');

                    detailedData_with_kong = data.stances_with_kong.map(item => ({breed: item.observation__observes__dog__breed, age: item.observation__observes__dog__dateOfBirthEst}));
                    detailedData_without_kong = data.stances_without_kong.map(item => ({breed: item.observation__observes__dog__breed, age: item.observation__observes__dog__dateOfBirthEst}));

                    var tooltipHandler = function(tooltipModel) {
                // Tooltip Element
                var tooltipEl = document.getElementById('chartjs-tooltip');
                if (!tooltipEl) {
                    tooltipEl = document.createElement('div');
                    tooltipEl.id = 'chartjs-tooltip';
                    tooltipEl.innerHTML = '<table></table>';
                    this._chart.canvas.parentNode.appendChild(tooltipEl);
                }
                if (tooltipModel.opacity === 0) {
                    tooltipEl.style.opacity = 0;
                    return;
                }

                if (tooltipModel.body) {
                    var index = tooltipModel.dataPoints[0].index;
                    var label = tooltipModel.dataPoints[0].label;
                    var value = tooltipModel.dataPoints[0].datasetIndex === 0 ? detailedData_with_kong[index] : detailedData_without_kong[index];
                    tooltipEl.innerHTML = '<table><tbody><tr><td>' + label + ': ' + value + '</td></tr></tbody></table>';
                }
                var positionY = this._chart.canvas.offsetTop;
                var positionX = this._chart.canvas.offsetLeft;

                // Display, position, and set styles for font
                tooltipEl.style.opacity = 1;
                tooltipEl.style.position = 'absolute';
                tooltipEl.style.left = positionX + tooltipModel.caretX + 'px';
                tooltipEl.style.top = positionY + tooltipModel.caretY + 'px';
                tooltipEl.style.fontFamily = tooltipModel._bodyFontFamily;
                tooltipEl.style.fontSize = tooltipModel.bodyFontSize + 'px';
                tooltipEl.style.fontStyle = tooltipModel._bodyFontStyle;
                tooltipEl.style.padding = tooltipModel.yPadding + 'px ' + tooltipModel.xPadding + 'px';
                tooltipEl.style.backgroundColor = 'rgba(0,0,0,0.7)';
                tooltipEl.style.color = 'white';
                tooltipEl.style.borderRadius = '3px';
            };

            var chart_with_kong = new Chart(ctx_with_kong, {
                type: 'bar',
                data: {
                    labels: data.stances_with_kong.map(item => item.dogStance),
                    datasets: [{
                        label: '# of Stances',
                        data: data.stances_with_kong.map(item => item.total),
                        backgroundColor: gradient_with_kong,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Dog Stances with Kong',
                        fontSize: 24
                    },
                    onClick: function(event, array) { onBarClick(chart_with_kong, event, array); },
                    tooltips: {
                        enabled: false,
                        custom: tooltipHandler
                    }
                }
            });

            var chart_without_kong = new Chart(ctx_without_kong, {
                type: 'bar',
                data: {
                    labels: data.stances_without_kong.map(item => item.dogStance),
                    datasets: [{
                        label: '# of Stances',
                        data: data.stances_without_kong.map(item => item.total),
                        backgroundColor: gradient_without_kong,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Dog Stances without Kong',
                        fontSize: 24
                    },
                    onClick: function(event, array) { onBarClick(chart_without_kong, event, array); },
                    tooltips: {
                        enabled: false,
                        custom: tooltipHandler
                    }
                }
            });

                    var chart_breeds = new Chart(ctx_breeds, {
                    type: 'bar',
                    data: {
                        labels: data.dog_breeds.map(item => item.breed),
                        datasets: [{
                            label: '# of Dogs',
                            data: data.dog_breeds.map(item => item.total),
                            backgroundColor: gradient_breeds,
                            borderColor: 'rgba(153, 102, 255, 1)',
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Distribution of Dog Breeds',
                            fontSize: 24
                        }
                    }
                });
                    // Call the function to create the duration of engagement chart
                    createChartOfEngagement(data.durations_with_kong, data.durations_without_kong);

                    // Hide loading spinner after successful fetch
                    loadingElement.style.display = 'none';
                })

                .catch(function() {
                    console.error("Error fetching data.");
                    loadingElement.innerHTML = "<p>Error fetching data. </p>";
                });
        }

        // Show loading spinner and fetch data
        loadingElement.style.display = 'block';
        fetchDataAndCreateCharts();