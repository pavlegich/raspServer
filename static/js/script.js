

let map;

function initMap() {
  const UAV = { lat: {{UAV["x"]}}, lng: {{UAV["y"]}} };
  const UAV2 = { lat: {{UAV2["x"]}}, lng: {{UAV2["y"]}} };
  const UAV3 = { lat: {{UAV3["x"]}}, lng: {{UAV3["y"]}} };
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 60.031, lng: 30.360 },
    zoom: 8
  });

  addMarker("UAV", UAV, map);
  addMarker("UAV2", UAV2, map);
  addMarker("UAV3", UAV3, map);
}

function addMarker(label, location, map) {
  new google.maps.Marker({
    position: location,
    map: map,
    icon: "{{ url_for('static', filename='img/map_icon.png') }}",
    label: label
  });
}

function gid(i) {return document.getElementById(i);}

gid("X").textContent = 60.031;
gid("Y").textContent = 30.360;
gid("Z").textContent = 20;
gid("time").textContent = 0;

// gid("UAV2").innerText = "UAV2 predict: \n(" + {{UAV2["x1"]}} + ", " + {{UAV2["y1"]}} + "), (" + {{UAV2["x2"]}} + ", " + {{UAV2["y2"]}} + "), \n(" + {{UAV2["x3"]}} + ", " + {{UAV2["y3"]}} + ")";
// gid("UAV3").innerText = "UAV3 predict: \n(" + {{UAV3["x1"]}} + ", " + {{UAV3["y1"]}} + "), (" + {{UAV3["x2"]}} + ", " + {{UAV3["y2"]}} + "), \n(" + {{UAV3["x3"]}} + ", " + {{UAV3["y3"]}} + ")";


var statusIntervalId = window.setInterval(update, 1000);


function update() {
    $.ajax({
        url: '/',
        dataType: 'text',
        success: function(data) {
            var now = new Date();
            $("#time").text(now);
            // $("#time").text(Math.round((Date.now()*1e-3)*100)/100);
        }
    })
}