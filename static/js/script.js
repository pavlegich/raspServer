function gid(i) {return document.getElementById(i);}

gid("X").textContent = 0;
gid("Y").textContent = 0;
gid("Z").textContent = 0;
gid("time").textContent = 0;

var UAV2 = { lat: 0, lng: 0 };
var UAV3 = { lat: 0, lng: 0 };

let map;
let markers = [];

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 59.9574645, lng: 30.3083750 },
    zoom: 10
  });
}

function addMarker(label, location, map) {
  const marker = new google.maps.Marker({
    position: location,
    map: map,
    icon: "{{ url_for('static', filename='img/map_icon.png') }}",
    label: label
  });
  markers.push(marker);
}

function deleteMarkers() {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
}


// gid("UAV2").innerText = "UAV2 predict: \n(" + {{UAV2["x1"]}} + ", " + {{UAV2["y1"]}} + "), (" + {{UAV2["x2"]}} + ", " + {{UAV2["y2"]}} + "), \n(" + {{UAV2["x3"]}} + ", " + {{UAV2["y3"]}} + ")";
// gid("UAV3").innerText = "UAV3 predict: \n(" + {{UAV3["x1"]}} + ", " + {{UAV3["y1"]}} + "), (" + {{UAV3["x2"]}} + ", " + {{UAV3["y2"]}} + "), \n(" + {{UAV3["x3"]}} + ", " + {{UAV3["y3"]}} + ")";

var statusIntervalId = window.setInterval(update, 5000);

function update() {
    $.ajax({
      type: "GET",
      url: '/get_gps',
      dataType: 'json',
      success: function(data) {
        $("#X2").text(Math.round(data.x*1e4)/1e4);
        $("#Y2").text(Math.round(data.y*1e4)/1e4);
        $("#Z2").text(data.z);

        UAV2 = { lat: data.x, lng: data.y };
      }
    })

    $.ajax({
      type: "GET",
      url: '/get_gps3',
      dataType: 'json',
      success: function(data) {
        $("#X3").text(Math.round(data.x*1e4)/1e4);
        $("#Y3").text(Math.round(data.y*1e4)/1e4);
        $("#Z3").text(data.z);

        UAV3 = { lat: data.x, lng: data.y };
      }
    })

    $.ajax({
      type: "GET",
      url: '/status',
      dataType: 'json',
      success: function(data) {
        $("#time").text(data.time);
        $("#X").text(Math.round(data.x*1e4)/1e4);
        $("#Y").text(Math.round(data.y*1e4)/1e4);
        $("#Z").text(data.z);

        var UAV = { lat: data.x, lng: data.y };
        deleteMarkers();
        addMarker("UAV", UAV, map);
        addMarker("UAV2", UAV2, map);
        addMarker("UAV3", UAV3, map);

      }
    })
}

function openUAV(evt, UAVname) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(UAVname).style.display = "block";
  evt.currentTarget.className += " active";
}