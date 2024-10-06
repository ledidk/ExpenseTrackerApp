document.addEventListener("DOMContentLoaded", function () {
    const timeframeDropdown = document.getElementById("timeframeDropdown");
    const categoryDetailsDiv = document.getElementById("categoryDetails");

    let xCategories = [];
    let yCategoryExpenses = [];

    // Function to fetch and update chart data
// Function to fetch and update chart data
    function fetchChartData(timeframe) {
        console.log("Fetching chart data for timeframe:", timeframe); // Log the selected timeframe

        // Check if the timeframe is "all" and adjust the API endpoint accordingly
        const url = timeframe === "all" ? `/api/books/chart_data` : `/api/books/chart_data?timeframe=${timeframe}`;

        fetch(url)
            .then(response => {
                console.log("Response received from /api/books/chart_data:", response); // Log the raw response
                return response.json();
            })
            .then(data => {
                console.log("Chart data:", data); // Log the entire data object

                // Update the chart with fetched data
                xCategories = data.categories;
                console.log("Categories:", xCategories); // Log categories

                yCategoryExpenses = data.expenses;
                console.log("Expenses:", yCategoryExpenses); // Log expenses

                updateChart(xCategories, yCategoryExpenses);

                // Display total books and expense in the right div initially (no category selected)
                categoryDetailsDiv.innerHTML = `
                    <h3>Total Data (All Categories)</h3>
                    <p>Total Books: ${data.total_books}</p>
                    <p>Total Expense: ${data.total_expense}</p>
                `;
            })
            .catch(error => console.error('Error fetching chart data:', error)); // Log any error in fetching
    }

            
    
// Function to update the chart
    function updateChart(labels, data) {
        console.log("Updating chart with labels and data:", labels, data); // Log labels and data before updating the chart

        const chart = new Chart("myChart", {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    backgroundColor: [
                        "#b91d47", "#00aba9", "#2b5797", "#e8c3b9", "#1e7145",
                        "#ff5733", "#f4a261", "#6a0dad", "#ffc300", "#581845", "#3498db"
                    ],
                    data: data
                }]
            },
            options: {
                title: {
                    display: true,
                    text: "Book Expense"
                },
                onClick: function (event, elements) {
                    if (elements.length) {
                        const clickedIndex = elements[0]._index;
                        const clickedCategory = labels[clickedIndex];
                        console.log("Clicked category:", clickedCategory); // Log clicked category
                        displayCategoryDetails(clickedCategory);
                    }
                }
            }
        });
    }

    // Function to display category details when a category is clicked
    function displayCategoryDetails(category) {
        console.log("Fetching details for category:", category); // Log the category being fetched

        fetch(`/api/books/category_details?category=${category}`)
            .then(response => {
                console.log("Response received from /api/books/category_details:", response); // Log the raw response
                return response.json();
            })
            .then(data => {
                console.log("Category details data:", data); // Log category details

                categoryDetailsDiv.innerHTML = `
                    <h3>Category: ${category}</h3>
                    <p>Total Books: ${data.total_books}</p>
                    <p>Top 3 Books:</p>
                    <ul>
                        ${data.top_books.map(book => `<li>${book.title}</li>`).join('')}
                    </ul>
                    <p>Total Expense: ${data.total_expense}</p>
                `;
            })
            .catch(error => console.error('Error fetching category details:', error)); // Log any error in fetching
    }

    // Fetch initial data when the page loads
    fetchChartData(timeframeDropdown.value);

    // Update the chart when the timeframe is changed
    timeframeDropdown.addEventListener("change", function () {
        console.log("Timeframe changed to:", this.value); // Log the new timeframe
        fetchChartData(this.value);
    });
});