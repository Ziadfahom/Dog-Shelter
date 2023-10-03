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


            // Hide loading spinner after successful fetch
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