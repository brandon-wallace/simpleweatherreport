// Display a loading icon while API query takes place.


window.addEventListener('pageshow', () => {
    document.querySelector('.dots').style.display = 'none';
});


const form = document.querySelector('form');


const revealLoader = () => {
    document.querySelector('.dots').style.display = 'block';
}


form.addEventListener('submit', revealLoader);
