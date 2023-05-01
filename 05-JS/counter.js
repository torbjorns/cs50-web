let counter = 0

function count() {
    counter ++;
    document.querySelector('h1').innerHTML = counter;

    if (counter % 10 === 0) {
        alert(`The count is now ${counter}`); // ${ } adds the variable to the string
    }
}

document.addEventListener('DOMContentLoaded', function() { // aEL takes two arguments: the event and the function that should be run, in this case an anonymous function
    document.querySelector('button').onclick = count;
});