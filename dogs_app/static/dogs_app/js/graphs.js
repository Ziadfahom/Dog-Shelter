const loadingElement = document.getElementById('loading');

// Global variable to hold the fetched data
let globalData;

// Global variable to store the chart data for the Dog Stances With/Without Kong Charts
var chart_with_kong;
var chart_without_kong;

// Global variables to hold chart and data for Dog Stances by Day Chart
let globalMaxDogStancesCount;
let globalTopStancesPerYearLimits;
let globalStanceData;
let globalDaysOfWeek;
let globalTopDogStances;
let chart_stances_by_days;

// Set Up the colors for the charts
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

$(document).ready(function() {

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

    // Add event listener for year dropdown change in the "Top Stances by Day" chart
    $('#year-select-stances').change(function() {
        var selectedYear = $(this).val();
        updateSliderForYear(selectedYear);
    });

    // Add event listener for "Show All" checkbox in the "Top Stances by Day" chart
    $('#showAllStances').change(function() {
        var selectedYear = $('#year-select-stances').val();
        updateSliderForYear(selectedYear);
    });

    // Add event listener for slider change in the "Top Stances by Day" chart
    $('#stanceSlider').on('input', function() {
        var slider = document.getElementById('stanceSlider');
        var showAllCheckBox = document.getElementById('showAllStances')
        if (slider.value !== slider.max) {
            showAllCheckBox.checked = false;
        }
        updateStanceLimit(this.value);
    });
});

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
                // Set the global data variable
                globalData = data;

                // Set Up the Charts

                // Dog Stances With/Without Kong Bar Charts
                var ctx_with_kong = document.getElementById('chart_dogStances_with_kong').getContext('2d');
                var ctx_without_kong = document.getElementById('chart_dogStances_without_kong').getContext('2d');

                // Dog Breeds Pie Chart
                var ctx_breeds = document.getElementById('chart_dogBreeds').getContext('2d');

                // Dog Stances by Day Chart
                // Initialize global variables
                initializeGlobalStancesVariables(data);
                // Populate Year Dropdown
                populateYearDropdown(data.top_stances_per_year_limits);

                // Initialize the chart with the fetched data
                updateStanceLimit(document.getElementById('stanceSlider').value);

                // Stance+Position With/Without Kong Radar Chart
                var ctx_stance_position = document.getElementById('chart_dogStance_dogPosition_with_without').getContext('2d');

                // Health Metrics Multi-Series Pie Chart
                var ctx_health_metrics = document.getElementById('chart_health_metrics').getContext('2d');


                // Define Colors
                var gradient_with_kong = ctx_with_kong.createLinearGradient(0, 0, 0, 400);
                gradient_with_kong.addColorStop(0, 'rgba(75, 192, 192, 1)');
                gradient_with_kong.addColorStop(1, 'rgba(75, 192, 192, 0.5)');

                var gradient_without_kong = ctx_without_kong.createLinearGradient(0, 0, 0, 400);
                gradient_without_kong.addColorStop(0, 'rgba(255, 99, 132, 1)');
                gradient_without_kong.addColorStop(1, 'rgba(255, 99, 132, 0.5)');


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
                            fontSize: 24,
                            position: 'top'
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
                                        size: 18,
                                        weight: 'bold'
                                    },
                                    color: '#333333'
                                },
                                position: 'bottom'
                            }
                        },
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
                const vaccinatedData = [].concat(health_metrics.vaccinated.M.Y, health_metrics.vaccinated.M.N, health_metrics.vaccinated.F.Y, health_metrics.vaccinated.F.N);

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

                const neuteredData = [].concat.apply([], [neuteredMaleData, neuteredFemaleData]);

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
                // Combined labels
                const combinedLabels = [...genderLabels, ...vaccinationLabels, ...neuteredLabels];

                // Initialize Chart.js Data and Config based on health metrics
                var chart_health_metrics = new Chart(ctx_health_metrics, {
                    type: 'pie',
                    data: {
                        labels: combinedLabels,
                        datasets: [
                            {
                                label: 'Neutered',
                                backgroundColor: health_backgroundColors.slice(6, 6 + neuteredData.length),
                                borderColor: 'black',
                                data: neuteredData,
                            },
                            {
                                label: 'Vaccinated',
                                backgroundColor: health_backgroundColors.slice(2, 2 + vaccinatedData.length),
                                borderColor: 'black',
                                data: vaccinatedData
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
                        events: ['mousemove', 'mouseout', 'touchstart', 'touchmove'], //Exclude click event on Legends
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
                                reverse: true,
                                position: 'bottom',
                                labels: {
                                    font: {
                                        size: 17,
                                        weight: 'bold'
                                    },
                                    color: '#333333',
                                    generateLabels: function (chart) {
                                        let labels = [];
                                        let cumulativeIndex = 0;

                                        chart.data.datasets.slice().reverse().forEach((dataset, datasetIndexRev) => {
                                            let datasetIndex = chart.data.datasets.length - 1 - datasetIndexRev;

                                            dataset.data.slice().reverse().forEach((dataValue, dataIndexRev) => {
                                                if (dataValue !== 0) {
                                                    // Calculate the actual label index in the combinedLabels array
                                                    let dataIndex = dataset.data.length - 1 - dataIndexRev;
                                                    let actualLabelIndex = cumulativeIndex + dataIndex;

                                                    labels.unshift({ // Unshift to add to the beginning of the array
                                                        text: chart.data.labels[actualLabelIndex],
                                                        fillStyle: dataset.backgroundColor[dataIndex],
                                                        hidden: !chart.isDatasetVisible(datasetIndex),
                                                        datasetIndex: datasetIndex,
                                                        index: dataIndex
                                                    });
                                                }
                                            });

                                            // Update cumulative index for the next dataset
                                            cumulativeIndex += dataset.data.length;
                                        });

                                        return labels;
                                    },
                                    onClick: function (event, legendItem, legend) {
                                        // Explicitly do nothing and prevent default action
                                        null;

                                        // const ci = legend.chart;
                                        // const datasetMeta = ci.getDatasetMeta(legendItem.datasetIndex);
                                        // datasetMeta.hidden = !datasetMeta.hidden;
                                        // ci.update();
                                    },
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

// Function to create the Dog Stances by Day Chart
function createChartStancesByDay(topDogStances, daysOfWeek, stanceData) {
    if (chart_stances_by_days) {
        chart_stances_by_days.destroy(); // Destroy the old chart instance before creating a new one
    }

    var ctx_by_day = document.getElementById('chart_dogStances_by_day').getContext('2d');
    var sliderValue = parseInt(document.getElementById('stanceSlider').value);
    var filteredStances = topDogStances.slice(0, sliderValue);

    var gradient_by_day = ctx_by_day.createLinearGradient(0, 0, 0, 400);
    gradient_by_day.addColorStop(0, 'rgba(128, 0, 128, 1)');
    gradient_by_day.addColorStop(1, 'rgba(128, 0, 128, 0.5)');

    var datasets = filteredStances.map((stance, index) => {
    const colorIndex = index % colors.length;
    return {
        label: stance,
        data: daysOfWeek.map(day => stanceData[day] ? (stanceData[day][stance] || 0) : 0),
        borderColor: colors[colorIndex],
        borderWidth: 3,
        backgroundColor: backgroundColors[colorIndex],
        stack: 'stack1'
    };
});



    chart_stances_by_days = new Chart(ctx_by_day, {
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
}

// Initialize global variables for the Dog Stances by Day Chart
function initializeGlobalStancesVariables(data) {
    globalMaxDogStancesCount = data.top_dog_stances_limit;
    globalTopStancesPerYearLimits = data.top_stances_per_year_limits;
    globalStanceData = data.stance_count_by_day;
    globalDaysOfWeek = Object.keys(globalStanceData);
    globalTopDogStances = data.top_dog_stances;
}

// Populate the year dropdown for the "Top Stances by Day" chart
function populateYearDropdown(yearLimits) {
    var yearSelect = document.getElementById('year-select-stances');

    // Sort years in descending order
    var sortedYears = Object.keys(yearLimits).sort((a, b) => b - a);

    sortedYears.forEach(year => {
        var option = document.createElement('option');
        option.value = year;
        option.text = year;
        yearSelect.appendChild(option);
    });
}

// Update the stances limit for the "Top Stances by Day" chart slider and redraw the chart
function updateStanceLimit(value) {
    document.getElementById('stanceSliderValue').innerText = value;

    createChartStancesByDay(globalTopDogStances, globalDaysOfWeek, globalStanceData);
}

// Update the slider max value based on the selected year in the "Top Stances by Day" chart
function updateSliderForYear(year) {
    var slider = document.getElementById('stanceSlider');
    var sliderValueDisplay = document.getElementById('stanceSliderValue');
    var sliderLabel = document.getElementById('stanceSliderLabel')
    var showAllCheckBox = document.getElementById('showAllStances')

    // Check if 'All Years' is selected
    if (year === 'total') {
        slider.max = globalMaxDogStancesCount;
        globalTopDogStances = globalData.top_dog_stances;
        globalStanceData = globalData.stance_count_by_day;
    } else {
        slider.max = globalTopStancesPerYearLimits[year];
        globalTopDogStances = globalData.top_stances_per_year[year];
        globalStanceData = globalData.yearly_stance_count_by_day[year];
    }

    // Disable or enable the slider based on the max value
    slider.disabled = slider.max === '1';

    if (slider.disabled) {
    sliderLabel.style.color = '#aaa'; // Light grey color for disabled
    sliderLabel.style.cursor = 'not-allowed'; // Change cursor
} else {
    sliderLabel.style.color = 'initial'; // Default color
    sliderLabel.style.cursor = 'default'; // Default cursor
}

    // Set slider value within new max limit
    slider.value = slider.value > slider.max ? slider.max : slider.value;

    if (showAllCheckBox.checked) {
        slider.value = slider.max;
    }


    // Update the displayed slider value and redraw the chart
    sliderValueDisplay.innerText = slider.value;
    updateStanceLimit(slider.value);
    createChartStancesByDay(globalTopDogStances, globalDaysOfWeek, globalStanceData);

}
