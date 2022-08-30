function call_sp(event) {
    const url = "/storedproc";

    const data = {    };

    console.log(data);
    var btn = document.getElementById("stored-proc-button");
    var spinner = document.getElementById("stored-proc-spinner");
    var btn_text = document.getElementById("stored-proc-text");

    btn.disabled = true;
    btn_text.innerHTML = "Loading..."
    spinner.hidden = false;

    fetch(url, {
        "method": "POST",
        "mode" : "cors",
        "headers": {
            "Content-Type": "application/json; charset=UTF-8"
        },
        "body": JSON.stringify(data)
    })
    .then(function(response) {
        btn.disabled = false;
        btn_text.innerHTML = "Call Stored Procedure"
        spinner.hidden = true;
    })
    .catch(err => {
        console.error(err);
        btn.disabled = false;
        btn_text.innerHTML = "Call Stored Procedure"
        spinner.hidden = true;
    });
    return false;
}
