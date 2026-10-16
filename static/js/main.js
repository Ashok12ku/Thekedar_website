// Simple counter animation for the stats/counter section on the Home page.
// Works with numeric prefixes like "20+", "100+", "₹30L+" — it animates the
// numeric part and keeps any suffix (like "+", "L+", "₹") static at the end.
document.addEventListener("DOMContentLoaded", function () {
    const counters = document.querySelectorAll(".counter");

    const animateCounter = (el) => {
        const raw = el.getAttribute("data-target") || el.textContent;
        const match = raw.match(/\d+/);
        if (!match) return; // no numeric part, leave as-is (e.g. plain text)

        const target = parseInt(match[0], 10);
        const prefix = raw.slice(0, match.index);
        const suffix = raw.slice(match.index + match[0].length);

        let current = 0;
        const duration = 1200; // ms
        const stepTime = Math.max(Math.floor(duration / target), 15);

        const timer = setInterval(() => {
            current += Math.ceil(target / (duration / stepTime));
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = `${prefix}${current}${suffix}`;
        }, stepTime);
    };

    if ("IntersectionObserver" in window && counters.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach((counter) => observer.observe(counter));
    }
});
