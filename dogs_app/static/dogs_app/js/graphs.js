const loadingElement = document.getElementById('loading');
var detailedData_with_kong = [];
var detailedData_without_kong = [];



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

            detailedData_with_kong = data.stances_with_kong.map(item => ({breed: item.observation__observes__dog__breed, age: item.observation__observes__dog__dateOfBirthEst}));
            detailedData_without_kong = data.stances_without_kong.map(item => ({breed: item.observation__observes__dog__breed, age: item.observation__observes__dog__dateOfBirthEst}));

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


            const backgroundColors = colors.map(color => color.replace('1)', '0.8)')); // Corresponding lighter colors for background

            var ctx_by_day = document.getElementById('chart_dogStances_by_day').getContext('2d');
            var gradient_by_day = ctx_by_day.createLinearGradient(0, 0, 0, 400);
            gradient_by_day.addColorStop(0, 'rgba(128, 0, 128, 1)');
            gradient_by_day.addColorStop(1, 'rgba(128, 0, 128, 0.5)');


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
                    plugins: {
                        datalabels: {
                            color: '#000000',
                            offset: -10,
                            font: {
                                size: 18,
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
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
                    plugins: {
                        datalabels: {
                            color: '#000000',
                            offset: -10,
                            font: {
                                size: 18,
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
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
                const colorIndex = index % colors.length;  // Loop through colors if there are more stances than colors
                return {
                    label: stance,
                    data: daysOfWeek.map(day => {
                        // Only include the count if it's not zero
                        return stance_count_by_day[day][stance] !== 0 ? stance_count_by_day[day][stance] : null;
                    }).filter(v => v !== null),  // Remove nulls (indicating zero counts)
                    borderColor: colors[colorIndex],
                    borderWidth: 2,
                    borderSkipped: true,
                    backgroundColor: backgroundColors[colorIndex],
                    stack: 'stack1'
                };
            });

            // Create a new array of labels (daysOfWeek) that only includes days with non-zero values for each stance.
            var filteredDaysOfWeek = daysOfWeek.filter(day => {
                return stances.some(stance => stance_count_by_day[day][stance] !== 0);
            });

            var chart_stances_by_days = new Chart(ctx_by_day, {
                type: 'bar',
                data: {
                    labels: filteredDaysOfWeek,
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
                                    size: 20
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
                                    size: 20
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
            const genderData = [health_metrics.gender.M, health_metrics.gender.F].filter(value => value !== 0);
            const genderLabels = ['Total Male Dogs', 'Total Female Dogs'].filter((_, index) => genderData[index] !== 0);

            const vaccinationData = [
                health_metrics.vaccinated.M.N,
                health_metrics.vaccinated.M.Y,
                health_metrics.vaccinated.F.Y,
                health_metrics.vaccinated.F.N
            ].filter(value => value !== 0);
            const vaccinationLabels = ['M Not Vaccinated', 'M Vaccinated', 'F Vaccinated', 'F Not Vaccinated'].filter((_, index) => vaccinationData[index] !== 0);

            const neuteredData = [
                health_metrics.neutered.M.N.Y,
                health_metrics.neutered.M.N.N,
                health_metrics.neutered.M.N['-'],
                health_metrics.neutered.M.Y.Y,
                health_metrics.neutered.M.Y.N,
                health_metrics.neutered.M.Y['-'],
                health_metrics.neutered.F.Y.Y,
                health_metrics.neutered.F.Y.N,
                health_metrics.neutered.F.Y['-'],
                health_metrics.neutered.F.N.Y,
                health_metrics.neutered.F.N.N,
                health_metrics.neutered.F.N['-']
            ]
            const neuteredLabels = ['M Not-Vaccinated Neutered', 'M Not-Vaccinated Not-Neutered', 'M Not-Vaccinated Unknown',
                'M Vaccinated Neutered', 'M Vaccinated Not-Neutered', 'M Vaccinated Unknown',
                'F Vaccinated Neutered', 'F Vaccinated Not-Neutered', 'F Vaccinated Unknown',
                'F Not-Vaccinated Neutered', 'F Not-Vaccinated Not-Neutered', 'F Not-Vaccinated Unknown']

            // Takes a base color in RGB format and a factor by which to lighten or darken the color
            function adjustColor(color, factor) {
                const [r, g, b] = color.match(/\d+/g).map(Number);
                return `rgba(${Math.min(255, r * factor)}, ${Math.min(255, g * factor)}, ${Math.min(255, b * factor)}, 1)`;
            }

            const health_baseColors = {
                'M': 'rgba(0, 128, 255, 1)',  // Blue for Male
                'F': 'rgba(255, 0, 128, 1)'  // Pink for Female
            };

            let health_backgroundColors = [];


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

            // // Vaccination
            // ['M', 'F'].forEach(gender => {
            //     health_backgroundColors.push(blendColors(health_baseColors[gender], health_outerBaseColors[gender], 0.6));
            //     health_backgroundColors.push(adjustColor(health_baseColors[gender], 0.9));
            // });

            health_backgroundColors.push(blendColors(health_baseColors['M'], health_outerBaseColors['M'], 0.5));
            health_backgroundColors.push(adjustColor(health_baseColors['M'], 0.9));

            health_backgroundColors.push(blendColors(health_baseColors['F'], health_outerBaseColors['F'], 0.9));
            health_backgroundColors.push(adjustColor(health_baseColors['F'], 0.6));
            // Neutered
            ['M', 'F'].forEach(gender => {
                ['Y', 'N'].forEach(vaccination => {
                    health_backgroundColors.push(blendColors(health_baseColors[gender], health_outerBaseColors[gender], 0.82));
                    health_backgroundColors.push(blendColors(health_baseColors[gender], health_outerBaseColors[gender], 0.7));
                    health_backgroundColors.push(blendColors(health_baseColors[gender], health_outerBaseColors[gender], 0.6));
                });
            });



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
                            formatter: function(value, context) {
                                if (value === 0) {
                                    return null;
                                }
                                // If the current index is the first one in the dataset, display the dataset label
                                if (context.dataIndex === 0) {
                                    return context.dataset.label + '  \n        ' + value;
                                }
                                // Otherwise, display only the value
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
                                label: function(context) {
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
                                generateLabels: function(chart) {
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
                                }
                            },
                            onClick: function(mouseEvent, legendItem, legend) {
                                legend.chart.getDatasetMeta(legendItem.datasetIndex).hidden = legend.chart.isDatasetVisible(legendItem.datasetIndex);
                                legend.chart.update();
                            }
                        }
                    },
                }
            });



            // Hide the loading spinner
            loadingElement.style.display = 'none';
        })
        .catch(function() {
            console.error("Error fetching data.");
            loadingElement.innerHTML = "<p>Error fetching data. </p>";
        });
}
    // Show loading spinner and fetch data
    loadingElement.style.display = 'flex';
    fetchDataAndCreateCharts();