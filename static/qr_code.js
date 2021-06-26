function docReady(fn) {
  if (
    document.readyState === "complete" ||
    document.readyState === "interactive"
  ) {
    setTimeout(fn, 1);
  } else {
    document.addEventListener("DOMContentLoaded", fn);
  }
}

docReady(function () {
  var resultContainer = document.getElementById("qr-reader-results");
  var lastResult,
    countResults = 0;
  function onScanSuccess(decodedText, decodedResult) {
    if (decodedText !== lastResult) {
      ++countResults;
      lastResult = decodedText;
      // Handle on success condition with the decoded message.
      console.log(`Scan result ${decodedText}`, decodedResult);
      var drink_id = "{{ data.drink_id }}";
      alert("Placing order for " + drink_id);
      $.ajax({
        data: {
          drink: drink_id,
          id: decodedResult["decodedText"],
          password: "36fb75181c26195f01aff5144aa1464b",
        },
        type: "POST",
        url: "http://127.0.0.1:5000/add_drink",
      }).done(function (data) {
        console.log("Request sent");
        alert(data);
      });
      var elem = document.getElementById("qr-reader");
      elem.parentNode.removeChild(elem);
    }
  }
  var html5QrcodeScanner = new Html5QrcodeScanner("qr-reader", {
    fps: 10,
    qrbox: 250,
  });
  html5QrcodeScanner.render(onScanSuccess);
});
