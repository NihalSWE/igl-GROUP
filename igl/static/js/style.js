document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.services-track');
    const cards = document.querySelectorAll('.service-card');
    const prevButton = document.getElementById('prevSlide');
    const nextButton = document.getElementById('nextSlide');
    const progressBar = document.getElementById('progressBar');
    
    let currentSlide = 0;
    let isAnimating = false;
    
    // Calculate slides per view based on screen width
    function getSlidesPerView() {
        if (window.innerWidth >= 1200) return 4;
        if (window.innerWidth >= 992) return 3;
        if (window.innerWidth >= 768) return 2;
        return 1;
    }

    // Update slider position and progress
    function updateSlider() {
        if (isAnimating) return;
        isAnimating = true;
        
        const slidesPerView = getSlidesPerView();
        const slideWidth = 100 / slidesPerView;
        const maxSlides = Math.ceil(cards.length / slidesPerView);

        // Update transform
        track.style.transform = `translateX(-${currentSlide * slideWidth}%)`;

        // Update progress bar
        const progress = ((currentSlide + 1) / maxSlides) * 100;
        progressBar.style.width = `${progress}%`;

        // Reset animation lock after transition
        setTimeout(() => {
            isAnimating = false;
        }, 500);
    }
    
    // Navigation handlers
    function nextSlide() {
        if (isAnimating) return;
        const slidesPerView = getSlidesPerView();
        const maxSlides = Math.ceil(cards.length / slidesPerView);
        currentSlide = (currentSlide + 1) % maxSlides;
        updateSlider();
    }
    
    function prevSlide() {
        if (isAnimating) return;
        const slidesPerView = getSlidesPerView();
        const maxSlides = Math.ceil(cards.length / slidesPerView);
        currentSlide = (currentSlide - 1 + maxSlides) % maxSlides;
        updateSlider();
    }

    // Event listeners for buttons
    prevButton.addEventListener('click', prevSlide);
    nextButton.addEventListener('click', nextSlide);

    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            currentSlide = 0;
            updateSlider();
        }, 250);
    });

    // Touch support
    let touchStartX = 0;
    let touchEndX = 0;

    track.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    });

    track.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                nextSlide();
            } else {
                prevSlide();
            }
        }
    }

    // Auto-play functionality
    const autoPlayInterval = 5000; // 5 seconds
    let autoPlayTimer = setInterval(nextSlide, autoPlayInterval);

    // Pause auto-play on hover
    track.addEventListener('mouseenter', () => {
        clearInterval(autoPlayTimer);
    });

    track.addEventListener('mouseleave', () => {
        autoPlayTimer = setInterval(nextSlide, autoPlayInterval);
    });

    // Initialize AOS animation library if present
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true
        });
    }

    // Initial setup
    updateSlider();
});
