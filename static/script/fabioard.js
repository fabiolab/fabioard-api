var ws = new WebSocket("ws://localhost:8090/fabioard-api/v1/ws");

ws.onmessage = function(event) {
    msg = JSON.parse(event.data);
    if (msg.label === 'next') {
        console.log(msg.label);
        fetchRandomImage();
    }
    if (msg.label === 'previous') {
        console.log(msg);
        displayImage(msg.data);
    }
}

document.getElementById('fullscreen-button').addEventListener('click', fullScreen);


var weatherIconMap = {
    "01d": "☀️",
    "01n": "🌙",
    "02d": "🌤️",
    "02n": "☁️",
    "03d": "🌥️",
    "03n": "☁️",
    "04d": "☁️",
    "04n": "☁️",
    "09d": "🌧️",
    "09n": "🌧️",
    "10d": "🌦️",
    "10n": "🌧️",
    "11d": "⛈️",
    "11n": "⛈️",
    "13d": "❄️",
    "13n": "❄️",
    "50d": "🌫️",
    "50n": "🌫️"
  }
  

function analyzeImage(img) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = img.width;img
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0, img.width, img.height);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    let r = 0, g = 0, b = 0;
    const pixelCount = data.length / 4;

    for (let i = 0; i < data.length; i += 4) {
        r += data[i];     // Red
        g += data[i + 1]; // Green
        b += data[i + 2]; // Blue
    }

    r = Math.floor(r / pixelCount);
    g = Math.floor(g / pixelCount);
    b = Math.floor(b / pixelCount);

    const brightness = (0.299 * r + 0.587 * g + 0.114 * b);
    const textColor = brightness > 128 ? 'black' : 'white';
    document.getElementById('infoContainer').style.color = textColor;
}

function displayImage(pic) {
    const imgElement = document.getElementById('randomImage');
    imgElement.src = `${pic.url}?t=${new Date().getTime()}`; // Add a fake t param to force image reload
    imgElement.onload = () => analyzeImage(imgElement);

    const pictureDate = document.getElementById('pictureDate');
    const pictureLocation = document.getElementById('pictureLocation');
    pictureDate.textContent = formatDate(new Date(pic.date));
    pictureLocation.textContent = pic.location;
}

function fetchRandomImage() {
    fetch('http://localhost:8090/fabioard-api/v1/pictures/random')
        .then(response => response.json())
        .then(data => {
            displayImage(data);
        })
        .catch(error => console.error('Erreur:', error));
}

function fetchWeather() {
    fetch('http://localhost:8090/fabioard-api/v1/weather')
        .then(response => response.json())
        .then(data => {
            const weatherText = document.getElementById('weatherText');
            weatherText.textContent = weatherIconMap[data.icon] + " " + data.temperature + "°C";
        })
        .catch(error => console.error('Erreur:', error));

    fetch('http://localhost:8090/fabioard-api/v1/forecast/by_day')
        .then(response => response.json())
        .then(data => {
            const forecastTemp1 = document.getElementById('forecastTemp1');
            const forecastIcon1 = document.getElementById('forecastIcon1');
            const forecastDay1 = document.getElementById('forecastDay1');
            forecastTemp1.textContent = data[0].min.temperature + "° " + data[0].max.temperature + "°";
            forecastIcon1.textContent = weatherIconMap[data[0].max.icon];
            forecastDay1.textContent = data[0].day_of_week;

            const forecastTemp2 = document.getElementById('forecastTemp2');
            const forecastIcon2 = document.getElementById('forecastIcon2');
            const forecastDay2 = document.getElementById('forecastDay2');
            forecastTemp2.textContent = data[1].min.temperature + "° " + data[1].max.temperature + "°";
            forecastIcon2.textContent = weatherIconMap[data[1].max.icon];
            forecastDay2.textContent = data[1].day_of_week;

            const forecastTemp3 = document.getElementById('forecastTemp3');
            const forecastIcon3 = document.getElementById('forecastIcon3');
            const forecastDay3 = document.getElementById('forecastDay3');
            forecastTemp3.textContent = data[2].min.temperature + "° " + data[2].max.temperature + "°";
            forecastIcon3.textContent = weatherIconMap[data[2].max.icon];
            forecastDay3.textContent = data[2].day_of_week;

            const forecastTemp4 = document.getElementById('forecastTemp4');
            const forecastIcon4 = document.getElementById('forecastIcon4');
            const forecastDay4 = document.getElementById('forecastDay4');
            forecastTemp4.textContent = data[3].min.temperature + "° " + data[3].max.temperature + "°";
            forecastIcon4.textContent = weatherIconMap[data[3].max.icon];
            forecastDay4.textContent = data[3].day_of_week;
        })
        .catch(error => console.error('Erreur:', error));
}

function fetchBusTime() {
    console.log("fetchBusTime");
    fetch('http://localhost:8090/fabioard-api/v1/bus/next')
        .then(response => response.json())
        .then(data => {
            data.slice(0, 3).map((schedule, index) => {
                updateCountdown(schedule.departure_time, index+1);
            });
        })
        .catch(error => console.error('Erreur:', error));
}

function fetchEvents() {
    console.log("fetchEvents");
    const events = document.getElementById("events");
    events.innerHTML = '';
    fetch('http://localhost:8090/fabioard-api/v1/events')
        .then(response => response.json())
        .then(data => {
            data.slice(0, 5).map((event) => {
                const span = document.createElement('span');
                const br = document.createElement('br');
                span.textContent = event.summary + " - " + getCountdownevent(event.start) + " jours";
                events.appendChild(span);
                events.appendChild(br);
            });
        })
        .catch(error => console.error('Erreur:', error));
}

function getCountdownevent(eventDateStr) {
    const eventDate = new Date(eventDateStr);
    const countdownElement = document.getElementById('eventsDate');

    const now = new Date();
    const timeRemaining = eventDate - now;

    if (timeRemaining <= 0) {
        clearInterval(interval);
        return "aujourd'hui !";
    } else {
        const jours = Math.ceil(timeRemaining / (1000 * 60 * 60 * 24));
        return `${jours}`;
    }
}


function updateCountdown(departureTime, index) {
    const departureDate = new Date(departureTime);
    const now = new Date();
    const timeRemaining = departureDate - now;
    const busTime = document.getElementById("busTime"+index);

    if (timeRemaining <= 0) {
        busTime.textContent = "⚠️ 0'";
    } else {
        const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
        // const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);
        if (hours > 0) {
            busTime.textContent = `${minutes + hours * 60}'`;
        } else {
            busTime.textContent = `${minutes}'`;
        }
    }
}

function updateDateTime() {
    const now = new Date();
    const timeElement = document.getElementById('time');
    const datelement = document.getElementById('date');
    timeElement.textContent = formatTime(now);
    datelement.innerHTML = formatDate(now, false);
}

function formatDate(date, year = true) {
    const options = { day: 'numeric', month: 'long' };
    if (year) {
        options.year = 'numeric';
    }
    const formattedDate = date.toLocaleDateString('fr-FR', options);
    return formattedDate;
}

function formatTime(date) {
    const hours = String(date.getHours()).padStart(2, '0'); // Ajoute un zéro devant si nécessaire
    const minutes = String(date.getMinutes()).padStart(2, '0'); // Ajoute un zéro devant si nécessaire
    return `${hours}h${minutes}`;
}

function fullScreen() {
    const elem = document.documentElement;
    const fsIcon = document.getElementById('fullscreen-button');
    if (document.fullscreenElement) {
        document.exitFullscreen();
        fsIcon.src = "/static/fullscreen.png";
    } else {
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.webkitRequestFullscreen) { /* Safari */
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) { /* IE11 */
            elem.msRequestFullscreen();
        }
        fsIcon.src = "/static/fullscreen_exit.png";
    }
}

 function nextPic() {
    fetch('/fabioard-api/v1/slideshow/next', {
        method: 'POST'
    })
    .then(response => console.log('Appel API réussi'))
    .catch(error => console.error('Erreur lors de l\'appel API:', error));
}

function previousPic() {
    fetch('/fabioard-api/v1/slideshow/previous', {
        method: 'POST'
    })
    .then(response => console.log('Appel API réussi'))
    .catch(error => console.error('Erreur lors de l\'appel API:', error));
}

// Appels initiaux
fetchRandomImage();
fetchWeather();
fetchBusTime();
fetchEvents();
updateDateTime();

// Appels récurrents
setInterval(fetchRandomImage, 300000);  // Toutes les 5'
setInterval(fetchWeather, 600000); // Toutes les 10'
setInterval(fetchBusTime, 60000); // Toutes les minutes
setInterval(fetchEvents, 300000);  // Toutes les 5'
setInterval(updateDateTime, 60000); // Toutes les minutes