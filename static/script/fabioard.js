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
            const weatherIcon = document.getElementById('weatherIcon');
            weatherText.textContent = data.temperature + "/" + data.feels_like + "°C";
            weatherIcon.src =  "https://openweathermap.org/img/wn/"+data.icon+"@2x.png";
        })
        .catch(error => console.error('Erreur:', error));

    fetch('http://localhost:8090/fabioard-api/v1/forecast')
        .then(response => response.json())
        .then(data => {
            const forecastText1 = document.getElementById('forecastText1');
            const forecastIcon1 = document.getElementById('forecastIcon1');
            forecastText1.textContent = data[2].date.slice(11, 13) + "h :" + data[2].temperature + "/" + data[2].feels_like + "°C";
            forecastIcon1.src =  "https://openweathermap.org/img/wn/"+data[2].icon+"@2x.png";

            const forecastText2 = document.getElementById('forecastText2');
            const forecastIcon2 = document.getElementById('forecastIcon2');
            forecastText2.textContent = data[5].date.slice(11, 13) + "h :" + data[5].temperature + "/" + data[5].feels_like + "°C";
            forecastIcon2.src =  "https://openweathermap.org/img/wn/"+data[5].icon+"@2x.png";
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
            data.slice(0, 3).map((event) => {
                const span = document.createElement('span');
                const br = document.createElement('br');
                span.textContent = event.summary + " dans " + getCountdownevent(event.start);
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
        return "C'est aujourd'hui !";
    } else {
        const jours = Math.ceil(timeRemaining / (1000 * 60 * 60 * 24));
        return ` ${jours} jours`;
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
    const dateTimeElement = document.getElementById('dateTime');
    dateTimeElement.textContent = formatDate(now) + " " + formatTime(now);  // now.toLocaleString(); //Format de date et heure local
}

function formatDate(date) {
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    const formattedDate = date.toLocaleDateString('fr-FR', options);
    return formattedDate;
}

function formatTime(date) {
    const hours = String(date.getHours()).padStart(2, '0'); // Ajoute un zéro devant si nécessaire
    const minutes = String(date.getMinutes()).padStart(2, '0'); // Ajoute un zéro devant si nécessaire
    return `${hours}h${minutes}`;
}

// Appels initiaux
fetchRandomImage();
fetchWeather();
fetchBusTime();
fetchEvents();
// updateDateTime();

// Appels récurrents
setInterval(fetchRandomImage, 60000);  // Toutes les 5'
setInterval(fetchWeather, 600000); // Toutes les 10'
setInterval(fetchBusTime, 60000); // Toutes les minutes
setInterval(fetchEvents, 300000);  // Toutes les 5'
// setInterval(updateDateTime, 60000); // Toutes les minutes