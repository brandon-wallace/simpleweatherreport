// datetime.js


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
