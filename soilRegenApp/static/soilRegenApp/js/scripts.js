// api url
const api_url = "https://aravinds1811-neural-style-transfer.hf.space/+/api/predict/";
  
// Defining async function
async function getapi(url) {
    const params = "";
    // Storing response
    const response = await fetch(url + ", " + params);
    
    // Storing data in form of JSON
    var data = await response.json();
    console.log(data);
    if (response) {
        hideloader();
    }
    show(data);
}
// Calling that async function
// getapi(api_url);
  
// Function to hide the loader
function hideloader() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('loading').innerHTML = "Success!!";
    alert("check console for data")
}
// Function to define innerHTML for HTML table
function show(data) {
    let tab = "Test";
    
    // Setting innerHTML as tab variable
    document.getElementById("employees").innerHTML = tab;
}

function setActiveLink() {
    // Get all links with class='nav-choice'
    var navLinks = document.getElementsByClassName('nav-choice');

    // Loop through all navigation links
    for (var i = 0; i < navLinks.length; i++) {
        // If the navigation link matches the current URL, add the 'active' class
        if (navLinks[i].href === document.URL) {
            navLinks[i].className += ' active';
        }
    }
}

// Call the function when the page loads
window.onload = setActiveLink;