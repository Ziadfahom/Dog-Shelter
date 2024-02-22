const loadingElement = document.getElementById('loading');


var chart_with_kong;
var chart_without_kong;


$(document).ready(function() {
    function fetchDataAndCreateCharts() {
        Chart.register(ChartDataLabels);
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
                var stance_count_by_day = data.stance_count_by_day;
                var daysOfWeek = Object.keys(stance_count_by_day);
                var stances = Object.keys(stance_count_by_day[daysOfWeek[0]]);
                var ctx_stance_position = document.getElementById('chart_dogStance_dogPosition_with_without').getContext('2d');
                var ctx_health_metrics = document.getElementById('chart_health_metrics').getContext('2d');

                var gradient_with_kong = ctx_with_kong.createLinearGradient(0, 0, 0, 400);
                gradient_with_kong.addColorStop(0, 'rgba(75, 192, 192, 1)');
                gradient_with_kong.addColorStop(1, 'rgba(75, 192, 192, 0.5)');

                var gradient_without_kong = ctx_without_kong.createLinearGradient(0, 0, 0, 400);
                gradient_without_kong.addColorStop(0, 'rgba(255, 99, 132, 1)');
                gradient_without_kong.addColorStop(1, 'rgba(255, 99, 132, 0.5)');


                const colors = [
                    'rgba(255, 99, 132, 1)',  // Red
                    'rgba(75, 192, 192, 1)',  // Green
                    'rgba(255, 206, 86, 1)',  // Yellow
                    'rgba(54, 162, 235, 1)',  // Blue
                    'rgba(153, 102, 255, 1)', // Purple
                    'rgba(128, 0, 0, 1)',     // Maroon
                    'rgba(0, 128, 0, 1)',     // Green
                    'rgba(255, 159, 64, 1)',  // Orange
                    'rgba(128, 0, 128, 1)',   // Purple
                    'rgba(128, 128, 0, 1)',   // Olive
                    'rgba(0, 128, 128, 1)',   // Teal
                    'rgba(0, 0, 128, 1)',     // Navy
                    'rgba(255, 0, 255, 1)',   // Fuchsia
                    'rgba(192, 192, 192, 1)', // Silver
                    'rgba(0, 0, 0, 1)',       // Black
                    'rgba(255, 105, 180, 1)'  // Hot Pink
                ];


                const backgroundColors = colors.map(color => color.replace('1)', '0.6)')); // Corresponding lighter colors for background

                var ctx_by_day = document.getElementById('chart_dogStances_by_day').getContext('2d');
                var gradient_by_day = ctx_by_day.createLinearGradient(0, 0, 0, 400);
                gradient_by_day.addColorStop(0, 'rgba(128, 0, 128, 1)');
                gradient_by_day.addColorStop(1, 'rgba(128, 0, 128, 0.5)');


                chart_with_kong = new Chart(ctx_with_kong, {
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
                        plugins: {
                            datalabels: {
                                color: '#000000',
                                offset: -10,
                                font: {
                                    size: 18,
                                    weight: 'bold'
                                },
                                formatter: function (value, context) {
                                    return value;
                                }
                            },
                            legend: {
                                labels: {
                                    font: {
                                        size: 17,
                                        weight: 'bold'
                                    },
                                    color: '#333333'
                                }
                            }
                        },
                        scales: {
                            x: {
                                pointLabels: {
                                    color: '#333333',
                                    font: {
                                        size: 18
                                    }
                                },
                                grid: {
                                    color: '#666666'
                                },
                                angleLines: {
                                    color: ''
                                },
                                ticks: {
                                    color: '#333333',
                                    font: {
                                        size: 20
                                    }
                                }
                            },
                            y: {
                                pointLabels: {
                                    color: '#333333',
                                    font: {
                                        size: 18
                                    }
                                },
                                grid: {
                                    color: '#666666'
                                },
                                angleLines: {
                                    color: ''
                                },
                                ticks: {
                                    color: '#333333',
                                    font: {
                                        size: 20
                                    }
                                }
                            }
                        }
                    }
                });

                chart_without_kong = new Chart(ctx_without_kong, {
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
                        plugins: {
                            datalabels: {
                                color: '#000000',
                                offset: -10,
                                font: {
                                    size: 18,
                                    weight: 'bold'
                                },
                                formatter: function (value, context) {
                                    return value;
                                }
                            },
                            legend: {
                                labels: {
                                    font: {
                                        size: 17,
                                        weight: 'bold'
                                    },
                                    color: '#333333'
                                }
                            }
                        },
                        scales: {
                            x: {
                                pointLabels: {
                                    color: '#333333',
                                    font: {
                                        size: 18
                                    }
                                },
                                grid: {
                                    color: '#666666'
                                },
                                angleLines: {
                                    color: ''
                                },
                                ticks: {
                                    color: '#333333',
                                    font: {
                                        size: 20
                                    }
                                }
                            },
                            y: {
                                pointLabels: {
                                    color: '#333333',
                                    font: {
                                        size: 18
                                    }
                                },
                                grid: {
                                    color: '#666666'
                                },
                                angleLines: {
                                    color: ''
                                },
                                ticks: {
                                    color: '#333333',
                                    font: {
                                        size: 20
                                    }
                                }
                            }
                        }
                    }
                });


                var chart_breeds = new Chart(ctx_breeds, {
                    type: 'pie',
                    data: {
                        labels: data.dog_breeds.map(item => item.breed),
                        datasets: [{
                            label: '# of Dogs',
                            data: data.dog_breeds.map(item => item.total),
                            backgroundColor: backgroundColors,
                            borderColor: colors,
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: false,
                        title: {
                            display: true,
                            text: 'Distribution of Dog Breeds',
                            fontSize: 24
                        },
                        plugins: {
                            datalabels: {
                                display: true,
                                color: '#333333',
                                font: {
                                    size: 25,
                                    weight: 'bold'
                                },
                                textShadowColor: 'rgba(255, 255, 255, 0.5)',
                                textShadowBlur: 5,
                                formatter: (value, context) => {
                                    return value;
                                }
                            },
                            legend: {
                                labels: {
                                    font: {
                                        size: 17,
                                        weight: 'bold'
                                    },
                                    color: '#333333'
                                }
                            }
                        },
                    }
                });

                var datasets = stances.map((stance, index) => {
                    const colorIndex = index % colors.length;
                    return {
                        label: stance,
                        data: daysOfWeek.map(day => stance_count_by_day[day][stance]),
                        borderColor: colors[colorIndex],
                        borderWidth: 3,
                        backgroundColor: backgroundColors[colorIndex],
                        stack: 'stack1'
                    };
                });


                var chart_stances_by_days = new Chart(ctx_by_day, {
                    type: 'bar',
                    data: {
                        labels: daysOfWeek,
                        datasets: datasets
                    },

                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Dog Stances by Day (Across The Week)',
                            fontSize: 24
                        },
                        plugins: {
                            datalabels: {
                                display: true,
                                color: '#333333',
                                font: {
                                    size: 20,
                                    weight: 'bold',
                                },
                                textShadowColor: 'rgba(255, 255, 255, 0.5)',
                                textShadowBlur: 5,
                                formatter: (value, context) => {
                                    return value !== 0 ? value : null;  // Display label only if value is not zero
                                },
                            },
                            tooltip: {
                                backgroundColor: '#333333',
                                titleColor: '#FFFFFF',
                                bodyColor: '#FFFFFF'
                            },
                            legend: {
                                labels: {
                                    font: {
                                        size: 17,
                                        weight: 'bold'
                                    },
                                    color: '#333333'
                                }
                            }
                        },
                        scales: {
                            y: {
                                stacked: true, // Enables stacking on the Y-axis
                                pointLabels: {
                                    color: '#333333',
                                    font: {
                                        size: 20
                                    }
                                },
                                grid: {
                                    color: '#666666'
                                },
                                ticks: {
                                    color: '#333333',
                                    font: {
                                        size: 20,
                                        weight: 'bold'
                                    }
                                }
                            },
                            x: {
                                stacked: true, // Enables stacking on the X-axis
                                pointLabels: {
                                    color: '#333333',
                                    font: {
                                        size: 20
                                    }
                                },
                                grid: {
                                    color: '#666666'
                                },
                                ticks: {
                                    color: '#333333',
                                    font: {
                                        size: 20,
                                        weight: 'bold'
                                    }
                                }
                            }
                        }
                    }
                });

                // Create the Stance+Position With/Without Kong Radar chart
                var chart_stance_position = new Chart(ctx_stance_position, {
                    type: 'radar',
                    data: {
                        labels: data.top_stance_position_combos.map(item => item[0]), // Stance + Position
                        datasets: [
                            {
                                label: 'With Kong',
                                data: data.top_stance_position_combos.map(item => item[1]), // Count with Kong
                                backgroundColor: 'rgba(0, 128, 0, 0.5)', // Teal-ish green
                                borderColor: 'rgba(0, 128, 0, 1)',
                                borderWidth: 2,
                                pointBackgroundColor: 'rgba(75, 192, 192, 1)' // Sky blue
                            },
                            {
                                label: 'Without Kong',
                                data: data.top_stance_position_combos.map(item => item[2]), // Count without Kong
                                backgroundColor: 'rgba(220, 20, 60, 0.5)', // Crimson-ish red
                                borderColor: 'rgba(220, 20, 60, 1)',
                                borderWidth: 2,
                                pointBackgroundColor: 'rgba(255, 99, 132, 1)' // Red
                            }
                        ]
                    },
                    options: {
                        responsive: false,
                        title: {
                            display: true,
                            text: 'Most Common General Behaviors - Comparison',
                            fontSize: 24,
                            fontColor: '#333333'
                        },
                        plugins: {
                            datalabels: {
                                display: true,
                                color: '#333333',
                                font: {
                                    size: 20,
                                    weight: 'bold'
                                },
                                textShadowColor: 'rgba(255, 255, 255, 0.5)',
                                textShadowBlur: 5,
                                formatter: (value, context) => {
                                    return value;
                                }
                            },
                            tooltip: {
                                backgroundColor: '#333333',
                                titleColor: '#FFFFFF',
                                bodyColor: '#FFFFFF'
                            },
                            legend: {
                                labels: {
                                    font: {
                                        size: 17,
                                        weight: 'bold'
                                    },
                                    color: '#333333'
                                }
                            }
                        },
                        scales: {
                            r: {
                                pointLabels: {
                                    color: '#333333',
                                    font: {
                                        size: 20
                                    }
                                },
                                grid: {
                                    color: '#666666'
                                },
                                angleLines: {
                                    color: ''
                                },
                                ticks: {
                                    color: '#333333',
                                    font: {
                                        size: 20
                                    }
                                }
                            }
                        }
                    }
                });


                // Prepare data for Health Metrics Multi-Series Pie Chart
                // Extract the health metrics
                const health_metrics = data.health_metrics;

                // Generate labels and data arrays for each ring
                const genderData = [health_metrics.gender.M, health_metrics.gender.F];
                const genderLabels = ['Total Male Dogs', 'Total Female Dogs'];

                // Extract vaccination data for each gender
                const vaccinatedMaleData = [health_metrics.vaccinated.M.Y, health_metrics.vaccinated.M.N];
                const vaccinatedFemaleData = [health_metrics.vaccinated.F.Y, health_metrics.vaccinated.F.N];

                // Extract neutered data for each gender
                const neuteredMaleData = [
                    health_metrics.neutered.M.Y.Y,
                    health_metrics.neutered.M.Y.N,
                    health_metrics.neutered.M.Y['-'],
                    health_metrics.neutered.M.N.Y,
                    health_metrics.neutered.M.N.N,
                    health_metrics.neutered.M.N['-']
                ];

                const neuteredFemaleData = [
                    health_metrics.neutered.F.Y.Y,
                    health_metrics.neutered.F.Y.N,
                    health_metrics.neutered.F.Y['-'],
                    health_metrics.neutered.F.N.Y,
                    health_metrics.neutered.F.N.N,
                    health_metrics.neutered.F.N['-']
                ];

                // Takes a base color in RGB format and a factor by which to lighten or darken the color
                function adjustColor(color, factor) {
                    const [r, g, b] = color.match(/\d+/g).map(Number);
                    return `rgba(${Math.min(255, r * factor)}, ${Math.min(255, g * factor)}, ${Math.min(255, b * factor)}, 1)`;
                }

                const health_baseColors = {
                    'M': 'rgba(0, 128, 255, 1)',  // Blue for Male
                    'F': 'rgba(255, 0, 128, 1)'   // Pink for Female
                };

                let health_backgroundColors = [];

                // Blend two colors
                function blendColors(color1, color2, weight) {
                    let w1 = weight;
                    let w2 = 1 - w1;
                    let rgb1 = color1.match(/\d+/g);
                    let rgb2 = color2.match(/\d+/g);

                    let blended = rgb1.map((x, i) => {
                        return Math.floor(x * w1 + rgb2[i] * w2);
                    });

                    return `rgba(${blended[0]}, ${blended[1]}, ${blended[2]}, 1)`;
                }

                const health_outerBaseColors = {
                    'M': 'rgba(128, 0, 128, 1)',  // Purple for Male
                    'F': 'rgba(0, 255, 128, 1)'   // Green for Female
                };

                // Gender
                health_backgroundColors.push(health_baseColors['M'], health_baseColors['F']);

                // Vaccinated
                ['M', 'F'].forEach(gender => {
                    health_backgroundColors.push(blendColors(health_baseColors[gender], health_outerBaseColors[gender], 0.85));
                    health_backgroundColors.push(adjustColor(health_baseColors[gender], 0.65));
                });

                // Neutered
                ['M', 'F'].forEach(gender => {
                    ['Y', 'N'].forEach(vaccination => {
                        health_backgroundColors.push(blendColors(health_baseColors[gender], health_outerBaseColors[gender], 0.75));
                        health_backgroundColors.push(blendColors(health_baseColors[gender], health_outerBaseColors[gender], 0.625));
                        health_backgroundColors.push(blendColors(health_baseColors[gender], health_outerBaseColors[gender], 0.45));
                    });
                });

                // Combine all possible categories and ensure they're in the same order for labels and data
                const vaccinationLabels = ['Male Vaccinated', 'Male Not Vaccinated', 'Female Vaccinated', 'Female Not Vaccinated'];
                const neuteredLabels = [
                    'Male Vaccinated Neutered', 'Male Vaccinated Not Neutered', 'Male Vaccinated Unknown',
                    'Male Not Vaccinated Neutered', 'Male Not Vaccinated Not Neutered', 'Male Not Vaccinated Unknown',
                    'Female Vaccinated Neutered', 'Female Vaccinated Not Neutered', 'Female Vaccinated Unknown',
                    'Female Not Vaccinated Neutered', 'Female Not Vaccinated Not Neutered', 'Female Not Vaccinated Unknown'
                ];

                // Flatten the arrays to include all possible combinations
                const vaccinationData = [].concat.apply([], [vaccinatedMaleData, vaccinatedFemaleData]);
                const neuteredData = [].concat.apply([], [neuteredMaleData, neuteredFemaleData]);

                // Initialize Chart.js Data and Config based on health metrics
                var chart_health_metrics = new Chart(ctx_health_metrics, {
                    type: 'pie',
                    data: {
                        labels: [...genderLabels, ...vaccinationLabels, ...neuteredLabels],
                        datasets: [
                            {
                                label: 'Neutered',
                                backgroundColor: health_backgroundColors.slice(6, 6 + neuteredData.length),
                                borderColor: 'black',
                                data: neuteredData,
                            },
                            {
                                label: 'Vaccinated',
                                backgroundColor: health_backgroundColors.slice(2, 2 + vaccinationData.length),
                                borderColor: 'black',
                                data: vaccinationData
                            },
                            {
                                label: 'Gender',
                                backgroundColor: health_backgroundColors.slice(0, genderData.length),
                                borderColor: 'black',
                                data: genderData
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            datalabels: {
                                color: 'charcoal',
                                font: {
                                    size: 24,
                                    weight: 'bold'
                                },
                                anchor: 'center',
                                align: 'center',
                                formatter: function (value, context) {
                                    if (value === 0) {
                                        return null;
                                    }
                                    if (context.dataIndex === 0) {
                                        return context.dataset.label + '  \n        ' + value;
                                    }
                                    return value;
                                }
                            },
                            tooltip: {
                                bodyFont: {
                                    size: 17,
                                },
                                titleFont: {
                                    size: 18,
                                },
                                callbacks: {
                                    label: function (context) {
                                        let labelIndex;
                                        if (context.datasetIndex === 0) {
                                            labelIndex = genderLabels.length + vaccinationLabels.length + context.dataIndex;
                                        } else if (context.datasetIndex === 1) {
                                            labelIndex = genderLabels.length + context.dataIndex;
                                        } else if (context.datasetIndex === 2) {
                                            labelIndex = context.dataIndex;
                                        }
                                        return context.chart.data.labels[labelIndex] + ': ' + context.formattedValue;
                                    }
                                }
                            },
                            legend: {
                                display: true,
                                position: 'bottom',
                                labels: {
                                    font: {
                                        size: 17,
                                        weight: 'bold'
                                    },
                                    color: '#333333',
                                    generateLabels: function (chart) {
                                        const datasets = chart.data.datasets;
                                        const labels = [];
                                        let cumulativeLength = 0;
                                        for (let i = 0; i < datasets.length; i++) {
                                            const dataset = datasets[i];
                                            for (let j = 0; j < dataset.data.length; j++) {
                                                if (dataset.data[j] !== 0) {
                                                    labels.push({
                                                        datasetIndex: i,
                                                        text: chart.data.labels[cumulativeLength + j],
                                                        fillStyle: health_backgroundColors[cumulativeLength + j], // Corrected here
                                                        hidden: !chart.isDatasetVisible(i),
                                                        index: j
                                                    });
                                                }
                                            }
                                            cumulativeLength += dataset.data.length;
                                        }
                                        return labels;
                                    },
                                    onClick: function (mouseEvent, legendItem, legend) {
                                        legend.chart.getDatasetMeta(legendItem.datasetIndex).hidden = legend.chart.isDatasetVisible(legendItem.datasetIndex);
                                        legend.chart.update();
                                    }
                                }
                            }
                        }
                    }
                });

                // Hide the loading spinner
                loadingElement.style.display = 'none';

            })
            .catch(function () {
                console.error("Error fetching data.");
                loadingElement.innerHTML = "<p>Error fetching data. </p>";
            });
    }

    // Show loading spinner and fetch data
    loadingElement.style.display = 'flex';
    fetchDataAndCreateCharts();

    // Populate the Dog Stances With/Without Kong dropdowns with available year options
    // Fetch data for the dropdowns
    $.getJSON('/chart_data/', function(data) {
        // Populate years for with-kong dropdown
        data.years_with_kong.forEach(function(year) {
            $('#year-select-with-kong').append(new Option(year, year));
        });

        // Event listener for changes in with-kong dropdown
        $('#year-select-with-kong').on('change', function() {
            // Get the selected year
            var selectedYear = $(this).val();

            // Determine the dataset based on the selected year
            var newData;
            if (selectedYear === 'total') {
                newData = data.stances_with_kong;
            } else {
                newData = data.yearly_stances_with_kong[selectedYear] || [];
            }

            // Update chart data
            chart_with_kong.data.labels = newData.map(item => item.dogStance);
            chart_with_kong.data.datasets[0].data = newData.map(item => item.total);

            // Redraw the chart
            chart_with_kong.update();
        });

        // Populate years for without-kong dropdown
        data.years_without_kong.forEach(function(year) {
            $('#year-select-without-kong').append(new Option(year, year));
        });

        // Event listener for changes in without-kong dropdown
        $('#year-select-without-kong').on('change', function() {
            // Get the selected year
            var selectedYear = $(this).val();

            // Determine the dataset based on the selected year
            var newData;
            if (selectedYear === 'total') {
                newData = data.stances_without_kong;
            } else {
                newData = data.yearly_stances_without_kong[selectedYear] || [];
            }

            // Update chart data
            chart_without_kong.data.labels = newData.map(item => item.dogStance);
            chart_without_kong.data.datasets[0].data = newData.map(item => item.total);

            // Redraw the chart
            chart_without_kong.update();
        });
    });

});