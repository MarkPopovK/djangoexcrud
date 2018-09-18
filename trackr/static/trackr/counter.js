function timedCount() {
    postMessage(true);
    setTimeout(timedCount, 1000);
}

timedCount();