function delete_crime(event) {
    const url = "/deletecrime";

    const data = {
        'CrimeID': document.getElementById('crimecrimeid').value,
        'CategoryCrime': document.getElementById('crimecategorycrime').value,
        'LastOutcome': document.getElementById('crimelastoutcome').value,
    };

    console.log(data);

    fetch("/deletecrime", {
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
