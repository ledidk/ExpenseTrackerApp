// Function to show selected page and store in sessionStorage
function showPage(pageId) {
  const pages = document.querySelectorAll(".content");
  pages.forEach((page) => {
    page.classList.remove("active"); // Hide all pages
  });

  // Show the selected page
  document.getElementById(pageId).classList.add("active");

  // Store the last active page ID in sessionStorage
  sessionStorage.setItem("lastPage", pageId);
}

// Function to show the update books page
function showUpdateBooks() {
  // Show the update books page
  showPage("add-books-page");
}

// Check for the last active page in sessionStorage and show it on page load
window.addEventListener("load", function () {
  const lastPage = sessionStorage.getItem("lastPage");

  if (lastPage) {
    // If there's a saved page, show it
    showPage(lastPage);
  } else {
    // Otherwise, show the default page (e.g., the dashboard or home page)
    showPage("dashboard-page"); // Replace with your default page ID
  }
});

// Optionally, if you want to clear the session when another div is selected
function selectAnotherDiv(divId) {
  sessionStorage.setItem("lastPage", divId);
  showPage(divId);
}

function editBook(button) {
  const row = button.closest("tr");
  const isEditing = row.classList.contains("editing");

  if (isEditing) {
    saveRow(row);
  } else {
    makeRowEditable(row);
  }
}

function makeRowEditable(row) {
  row.classList.add("editing");
  const cells = row.querySelectorAll("td");

  cells.forEach((cell, index) => {
    if (index > 0 && index < 8) {
      // Skip the checkbox and buttons columns
      const cellValue = cell.textContent.trim();
      cell.innerHTML = `<input type="text" value="${cellValue}">`;
    }
  });

  row.querySelector("button").textContent = "Save";
}

function saveRow(row) {
  row.classList.remove("editing");
  const cells = row.querySelectorAll("td");

  cells.forEach((cell, index) => {
    if (index > 0 && index < 8) {
      // Skip the checkbox and buttons columns
      const inputField = cell.querySelector("input");
      if (inputField) {
        const newValue = inputField.value;
        cell.textContent = newValue;
      }
    }
  });

  row.querySelector("button").textContent = "Edit";
}

function addBookRow() {
  // Get the table body
  const tableBody = document.getElementById("add-books-tbody");

  // Get the first row (template row) to clone it
  const firstRow = document.querySelector(".add-book-row");

  if (!firstRow) {
    console.error("No row to clone.");
    return;
  }

  // Clone the first row
  const newRow = firstRow.cloneNode(true);

  // Clear the values of the input fields in the new row
  const inputs = newRow.querySelectorAll("input");
  inputs.forEach((input) => (input.value = ""));

  const selects = newRow.querySelectorAll("select");
  selects.forEach((select) => (select.selectedIndex = 0)); // Reset the dropdown

  // Make sure the new row is appended to the table body
  tableBody.appendChild(newRow);
}

function saveBook(button) {
  // Placeholder function for saving the book data
  alert("Book details saved!");
}

function deleteRow(button) {
  const row = button.closest("tr");
  const bookId = row.querySelector('input[name="book_id"]').value;

  // Send AJAX request to delete the book
  fetch(`/delete_book/${bookId}/`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  }).then((response) => {
    if (response.ok) {
      row.remove(); // Remove the row from the table
    }
  });
}

// Toggles edit mode for input fields
function toggleEdit(fieldId, button) {
  const inputField = document.getElementById(fieldId);
  if (inputField.disabled) {
    inputField.disabled = false;
    button.innerText = "Save"; // Change button text to 'Save'
  } else {
    inputField.disabled = true;
    button.innerText = "Edit"; // Revert button text to 'Edit'
  }
}

// Save Changes Function (placeholder)
function saveChanges() {
  alert("Changes saved successfully!");
  // Add logic to send data to the server or update the profile info
}

// Cancel Changes Function (placeholder)
function cancelChanges() {
  // Logic to reset changes (optional)
  alert("Changes canceled!");
}

// Delete Account Function (placeholder)
function deleteAccount() {
  if (confirm("Are you sure you want to delete your account?")) {
    // Add logic to delete the account
    alert("Account deleted.");
  }
}

function addBookRow() {
  const tbody = document.getElementById("add-books-tbody");
  const newRow = document.createElement("tr");
  newRow.className = "add-book-row";
  newRow.innerHTML = `
                <td><input type="text" placeholder="Enter ISBN"></td>
                <td><input type="text" placeholder="Enter Book Title"></td>
                <td><input type="text" placeholder="Enter Subtitle"></td>
                <td><input type="text" placeholder="Enter Author"></td>
                <td><input type="text" placeholder="Enter Publisher"></td>
                <td><input type="date"></td>
                <td>
                    <select class="dropdown">
                        <option value="">All Categories</option>
                        <option value="Fiction">Fiction</option>
                        <option value="Non-Fiction">Non-Fiction</option>
                        <option value="Science">Science</option>
                        <!-- Add more categories as needed -->
                    </select>
                </td>
                <td><input type="number" placeholder="Expense"></td>
                <td>
                    <button type="button" onclick="saveBook(this)">Save</button>
                    <button type="button" onclick="deleteRow(this)">Delete</button>
                </td>
            `;
  tbody.appendChild(newRow);
}

// Function to save book data
function saveBook(button) {
  const row = button.parentElement.parentElement;
  const isbn = row.cells[0].children[0].value;
  const title = row.cells[1].children[0].value;
  const subtitle = row.cells[2].children[0].value;
  const authors = row.cells[3].children[0].value;
  const publisher = row.cells[4].children[0].value;
  const publishDate = row.cells[5].children[0].value;
  const category = row.cells[6].children[0].value;
  const expense = row.cells[7].children[0].value;

  const bookData = {
    isbn,
    title,
    subtitle,
    authors,
    publisher,
    publish_date: publishDate,
    category,
    distribution_expense: expense,
  };

  // Send the book data to the server using fetch
  fetch("/add-book/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"), // Get CSRF token for security
    },
    body: JSON.stringify(bookData),
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Failed to save book");
      }
    })
    .then((data) => {
      alert("Book added successfully!");
      // Optionally, you could clear the input fields after successful addition
      row.reset();
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Failed to save book. Please try again.");
    });
}

// Function to delete a book row
function deleteRow(button) {
  const row = button.parentElement.parentElement;
  row.remove();
}

// Function to get CSRF token for AJAX requests
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Check if this cookie string begins with the name we want
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function filterByCategory(category) {
  const sortBy =
    new URLSearchParams(window.location.search).get("sort_by") || "title";
  window.location.href = `?category=${category}&sort_by=${sortBy}`;
}

function searchBooks(query) {
  const sortBy =
    new URLSearchParams(window.location.search).get("sort_by") || "title";
  window.location.href = `?search=${query}&sort_by=${sortBy}`;
}

// Function to fetch data asynchronously
async function fetchData(url) {
  try {
    // Show the loading spinner
    document.getElementById("loading-spinner").style.display = "block";

    // Fetch data
    const response = await fetch(url);

    // Check if response is OK
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    // Parse data
    const data = await response.json();

    // Hide the loading spinner
    document.getElementById("loading-spinner").style.display = "none";

    // Call a function to handle the data (e.g., render it)
    renderData(data);
  } catch (error) {
    // Handle errors (e.g., network issues)
    console.error("There was a problem with the fetch operation:", error);
    document.getElementById("loading-spinner").style.display = "none";
    alert("Failed to fetch data");
  }
}

// Function to render data on the page (you'll need to customize this)
function renderData(data) {
  const contentContainer = document.getElementById("content-container");
  contentContainer.innerHTML = ""; // Clear existing content

  // Populate the container with fetched data (you can customize this)
  data.forEach((item) => {
    const div = document.createElement("div");
    div.textContent = `Item: ${item.name}`;
    contentContainer.appendChild(div);
  });
}

// Example usage: Call fetchData with your API URL
window.addEventListener("load", () => {
  fetchData("https://api.example.com/data"); // Replace with your actual API URL
});

// Function to add a new book row
function addBookRow() {
  const tbody = document.getElementById("add-books-tbody");
  const newRow = document.createElement("tr");
  newRow.className = "add-book-row";
  newRow.innerHTML = `
                <td><input type="text" placeholder="Enter ISBN"></td>
                <td><input type="text" placeholder="Enter Book Title"></td>
                <td><input type="text" placeholder="Enter Subtitle"></td>
                <td><input type="text" placeholder="Enter Author"></td>
                <td><input type="text" placeholder="Enter Publisher"></td>
                <td><input type="date"></td>
                <td>
                    <select class="dropdown">
                        <option value="">All Categories</option>
                        <option value="Fiction">Fiction</option>
                        <option value="Non-Fiction">Non-Fiction</option>
                        <option value="Science">Science</option>
                        <!-- Add more categories as needed -->
                    </select>
                </td>
                <td><input type="number" placeholder="Expense"></td>
                <td>
                    <button type="button" onclick="saveBook(this)">Save</button>
                    <button type="button" onclick="deleteRow(this)">Delete</button>
                </td>
            `;
  tbody.appendChild(newRow);
}

// Function to save book data
function saveBook(button) {
  const row = button.parentElement.parentElement;
  const isbn = row.cells[0].children[0].value;
  const title = row.cells[1].children[0].value;
  const subtitle = row.cells[2].children[0].value;
  const authors = row.cells[3].children[0].value;
  const publisher = row.cells[4].children[0].value;
  const publishDate = row.cells[5].children[0].value;
  const category = row.cells[6].children[0].value;
  const expense = row.cells[7].children[0].value;

  const bookData = {
    isbn,
    title,
    subtitle,
    authors,
    publisher,
    publish_date: publishDate,
    category,
    distribution_expense: expense,
  };

  // Send the book data to the server using fetch
  fetch("/add-book/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"), // Get CSRF token for security
    },
    body: JSON.stringify(bookData),
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Failed to save book");
      }
    })
    .then((data) => {
      alert("Book added successfully!");
      // Optionally, you could clear the input fields after successful addition
      row.reset();
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Failed to save book. Please try again.");
    });
}

// Function to delete a book row
function deleteRow(button) {
  const row = button.parentElement.parentElement;
  row.remove();
}

// Function to get CSRF token for AJAX requests
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Check if this cookie string begins with the name we want
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
