// Display date.

let loader = document.querySelector('.dots');

(function() {

    let today = new Date();

    let now = today.toLocaleString('en-US', {
        year: "numeric",
        month: "short",
        day: "numeric",
        weekday: "short",
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        timeZoneName: "short"
    });

    document.querySelector('.today__text').textContent = now;

})();


// Display a loading icon while API query takes place.

if (loader) {
    window.addEventListener('pageshow', () => {
        document.querySelector('.dots').style.display = 'none';
    });
}


const form = document.querySelector('form');


const revealLoader = () => {
    document.querySelector('.dots').style.display = 'block';
}


form.addEventListener('submit', revealLoader);
