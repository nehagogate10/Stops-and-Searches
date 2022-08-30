function check(event) {
    const url = "/update";

    const data = {
        'PersonID' : parseInt(document.getElementById('personidupdate').value),
        'AgeRange': document.getElementById('personageupdate').value,
        'SelfDescribedEthnicity': document.getElementById('personselfethupdate').value,
        'OfficerDescribedEthnicity': document.getElementById('personofficerethupdate').value,
        'Gender': document.getElementById('persongender').value
    };

    console.log(data);

    fetch("/update", {
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
        });
    })
    .catch(err => {
        console.error(err);
        document.getElementById('message').innerHTML = err.message;
    });
    return false;
}
