'use strict'

let drawing = false;
let context;

document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('canvas');

    context = canvas.getContext('2d');

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mousemove', draw);
});

function startDrawing(e) {
    drawing = true;
    draw(e);
};

function stopDrawing() {
    drawing = false;
    context.beginPath();
};

function draw(e) {
    if (!drawing) return;

    context.lineWidth = 10;
    context.lineCap = 'round';
    context.strokeStyle = '#fff';

    context.lineTo(e.clientX - e.target.offsetLeft, e.clientY - e.target.offsetTop);
    context.stroke();
    context.beginPath();
    context.moveTo(e.clientX - e.target.offsetLeft, e.clientY - e.target.offsetTop);
};

function clearCanvas() {
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const recognizedDigitElement = document.getElementById('output1');
    const probabilityElement = document.getElementById('output2');

    context.clearRect(0, 0, canvas.width, canvas.height);

    recognizedDigitElement.textContent = `ㅤ`;
    probabilityElement.textContent = `ㅤ`;
};

function sendData() {
    const canvas = document.getElementById('canvas');
    const fileInput = document.createElement("input");
    fileInput.type = "file";

    canvas.toBlob(function (blob) {
        const file = new File([blob], "digit.png", { type: "image/png" });

    const formData = new FormData();
        formData.append("file", file);

    fetch('http://127.0.0.1:8000/upload-file/', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail);
                });
            }
            return response.json();
        })
        .then(data => updateResults(data))
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('output1').textContent = 'Ошибка сервера';
        });
    }, "image/png");
};

function updateResults(data) {
    const recognizedDigitElement = document.getElementById('output1');
    const probabilityElement = document.getElementById('output2');

    recognizedDigitElement.textContent = `${data.recognized_digit}`;
    probabilityElement.textContent = `${Number(data.probability) * 100} %`;
};
