document.addEventListener("DOMContentLoaded", () => {
    let TimeofDay = document.getElementById("time_of_day");
    let time_of_day_up = document.getElementById("time_of_day_up");
    let time_of_day_down = document.getElementById("time_of_day_down");

    let miles = document.getElementById("miles");
    let miles_up = document.getElementById("miles_up");
    let miles_down = document.getElementById("miles_down");

    let time_of_day_count = 0;
    let miles_count = 1; 
    let times = ['Any', 'Midnight', 'Day', 'Evening'];

    function updateTimeOfDay(direction) {

        time_of_day_count = (time_of_day_count + direction + times.length) % times.length;
        TimeofDay.innerHTML = times[time_of_day_count];
    }

    function updateMiles(direction) {
        miles_count = Math.max(1, miles_count + direction);
        miles.innerHTML = miles_count;
    }

    miles_up.addEventListener("click", () => updateMiles(1));
    miles_down.addEventListener("click", () => updateMiles(-1));
    time_of_day_up.addEventListener("click", () => updateTimeOfDay(1));
    time_of_day_down.addEventListener("click", () => updateTimeOfDay(-1));
});
