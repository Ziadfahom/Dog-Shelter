const loadingElement = document.getElementById('loading');
var detailedData_with_kong = [];
var detailedData_without_kong = [];



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
            var stance_count_by_day = data.stance_count_by_day;
            var daysOfWeek = Object.keys(stance_count_by_day);
            var stances = Object.keys(stance_count_by_day[daysOfWeek[0]]);

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


            const backgroundColors = colors.map(color => color.replace('1)', '0.7)')); // Corresponding lighter colors for background



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
                }
            });

            Chart.register(ChartDataLabels);

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
                                size: 30
                            },
                            textShadowColor: 'rgba(255, 255, 255, 0.5)',
                            textShadowBlur: 5,
                            formatter: (value, context) => {
                                return value;
                            }
                        }
                    }
                }
            });

            var datasets = stances.map((stance, index) => {
                const colorIndex = index % colors.length;  // Loop through colors if there are more stances than colors
                return {
                    label: stance,
                    data: daysOfWeek.map(day => stance_count_by_day[day][stance]),
                    borderColor: colors[colorIndex],
                    borderWidth: 3,
                    borderSkipped: false,
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
                    scales: {
                        y: {
                            stacked: true // Enables stacking on the Y-axis
                        },
                        x: {
                            stacked: true // Enables stacking on the X-axis
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