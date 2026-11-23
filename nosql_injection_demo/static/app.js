function sendLogin(mode, useInjection) {
    var username = document.getElementById(mode + "-username").value;
    var password = document.getElementById(mode + "-password").value;
    var resultBox = document.getElementById(mode + "-result");
    var payloadBox = document.getElementById(mode + "-payload");

    if (useInjection) {
        password = { "$gt": "" };
    }

    var loginData = {
        username: username,
        password: password
    };

    var previewData = {
        username: username,
        password: useInjection ? { "$gt": "" } : "[hidden]"
    };
    payloadBox.textContent = JSON.stringify(previewData, null, 2);
    resultBox.className = "result loading";
    resultBox.textContent = "Checking login...";

    fetch("/api/" + mode + "-login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(loginData)
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        if (data.success) {
            resultBox.className = "result result-success";
            resultBox.textContent = "SUCCESS: " + data.message;
        } else {
            resultBox.className = "result result-failure";
            resultBox.textContent = "FAILED: " + data.message;
        }
    })
    .catch(function () {
        resultBox.className = "result result-failure";
        resultBox.textContent = "Cannot connect to the server.";
    });
}

document.getElementById("vulnerable-form").addEventListener("submit", function (event) {
    event.preventDefault();
    sendLogin("vulnerable", false);
});

document.getElementById("secure-form").addEventListener("submit", function (event) {
    event.preventDefault();
    sendLogin("secure", false);
});

document.getElementById("vulnerable-attack").addEventListener("click", function () {
    sendLogin("vulnerable", true);
});

document.getElementById("secure-attack").addEventListener("click", function () {
    sendLogin("secure", true);
});

function showAttackPayload(mode) {
    var username = document.getElementById(mode + "-username").value;
    var attackData = {
        username: username,
        password: { "$gt": "" }
    };
    document.getElementById(mode + "-payload").textContent = JSON.stringify(attackData, null, 2);
}

showAttackPayload("vulnerable");
showAttackPayload("secure");

document.getElementById("vulnerable-username").addEventListener("input", function () {
    showAttackPayload("vulnerable");
});

document.getElementById("secure-username").addEventListener("input", function () {
    showAttackPayload("secure");
});
