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