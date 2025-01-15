let TimeofDay = document.getElementById("time_of_day");
let miles = document.getElementById("miles");

function getLocation(event) { 
    event.preventDefault();
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (pos) {
            const crd = pos.coords;

            console.log(`Latitude : ${crd.latitude}`);
            console.log(`Longitude: ${crd.longitude}`);

            const hiddenInput = document.getElementById("location-input");
            hiddenInput.value = crd.latitude + "," + crd.longitude;

        });
    } else { 
        console.log("Geolocation is not supported by this browser.");
    }
}




function addressbarLocation(event) {
    if (event) event.preventDefault(); // Prevent default form submission

    const address = document.getElementById("addressbar").value;

    console.log(miles.innerHTML) // check if not number
    // Send POST request with the address
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ address: address , miles: miles.innerHTML,TimeofDay: TimeofDay.innerHTML }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to update map: ${response.statusText}`);
        }
        return response.json(); // Parse the response as JSON
    })
    .then(data => {
       // console.log('Full response:', data);  // Log the entire response to check the structure

        const { map_html, report } = data;
        console.log('Map HTML:', map_html);
        console.log('Report:', report);

        const iframe = document.getElementById("map");
        const reportText = document.getElementById("Report");

        iframe.srcdoc = map_html;
        reportText.innerHTML = report;
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error updating the map. Please try again.");
    });
}
