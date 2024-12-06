export function throttle(func, delay = 1000) {
    let lastCallTime = 0;
    let timeout;

    return function (...args) {
        const currentTime = Date.now();
        const remainingTime = delay - (currentTime - lastCallTime);

        if (remainingTime <= 0) {
            clearTimeout(timeout);
            lastCallTime = currentTime;
            func.apply(this, args);
        } else {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                lastCallTime = Date.now();
                func.apply(this, args);
            }, remainingTime);
        }
    };
}

