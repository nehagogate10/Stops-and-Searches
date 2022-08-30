function log_location(event) {
    const url = "/loglocation";

    const data = {
        'CrimeID': document.getElementById('locationcrimeid').value,
        'Latitude': document.getElementById('locationlatitude').value,
        'Longitude': document.getElementById('locationlogitude').value,
        'CrimeLevel': document.getElementById('locationcrimelevel').value,
        'StreetName': document.getElementById('locationstreetname').value,
    };

    console.log(data);

    fetch("/loglocation", {
        "method": "POST",
        "mode" : "cors",
        "headers": {
            "Content-Type": "application/json; charset=UTF-8"
        },
        "body": JSON.stringify(data)
    })
    .then(function(response) {
        response.json().then((data) => {
            console.log(data);
            document.getElementById('message').innerHTML = data.message;
            document.getElementById('message').classList.add("alert", "alert-success");
        });
    })
    .catch(err => {
        console.error(err);
        document.getElementById('message').innerHTML = err.message;
    });
    return false;
}
