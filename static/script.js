// 1. Copy Menu for Mobile
function copyMenu() {
    var dptCategory = document.querySelector(".dpt-cat");
    var dptPlace = document.querySelector(".departments");
    if (dptCategory && dptPlace) dptPlace.innerHTML = dptCategory.innerHTML;
  
    var mainNav = document.querySelector(".header-nav nav");
    var navPlace = document.querySelector(".off-canvas nav");
    if (mainNav && navPlace) navPlace.innerHTML = mainNav.innerHTML;
  
    var topNav = document.querySelector(".header-top .wrapper");
    var topPlace = document.querySelector(".off-canvas .thetop-nav");
    if (topNav && topPlace) topPlace.innerHTML = topNav.innerHTML;
}
copyMenu();
  
// 2. Show Mobile Menu
const menuButton = document.querySelector('.trigger');
const closeButton = document.querySelector('.t-close');
const addclass = document.querySelector('.site');

if (menuButton && addclass) {
    menuButton.addEventListener('click', function(e) {
        e.preventDefault();
        addclass.classList.toggle('showmenu');
    });
}
if (closeButton && addclass) {
    closeButton.addEventListener('click', function(e) {
        e.preventDefault();
        addclass.classList.remove('showmenu');
    });
}

// 3. Show Sub Menu on Mobile
const submenu = document.querySelectorAll('.has-child .icon-small');
if (submenu.length > 0) {
    submenu.forEach((menu) => menu.addEventListener("click", function(e) {
        e.preventDefault();
        submenu.forEach((item) => item != this ? item.closest(".has-child").classList.remove("expand") : null);
        if (this.closest('.has-child').classList != 'expand');
        this.closest('.has-child').classList.toggle('expand');
    }));
}

// 4. Main Slider
const mainSwiper = document.querySelector('.myslider.swiper');
if (mainSwiper) {
    new Swiper('.myslider.swiper', {
        loop: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.swiper-pagination',
        },
        speed: 1500,
    });
}

// 5. Show Search
const searchButton = document.querySelector('.t-search');
const tClose = document.querySelector('.search-close');
const showClass = document.querySelector('.site');

if (searchButton && showClass) {
    searchButton.addEventListener('click', function(e) {
        e.preventDefault();
        showClass.classList.toggle('showsearch');
    });
}
if (tClose && showClass) {
    tClose.addEventListener('click', function(e) {
        e.preventDefault();
        showClass.classList.remove('showsearch');
    });
}

// 6. Show Department Menu
const dptButton = document.querySelector('.dpt-cat .dpt-trigger');
const dptClass = document.querySelector('.site');

if (dptButton && dptClass) {
    dptButton.addEventListener('click', function(e) {
        e.preventDefault();
        dptClass.classList.toggle('showdpt');
    });
}

// 7. Product Image Slider (Detail Page)
const thumbElement = document.querySelector('.small-image');
const bigElement = document.querySelector('.big-image');

if (thumbElement && bigElement) {
    var productThumb = new Swiper ('.small-image', {
        loop: true,
        spaceBetween: 10,
        slidesPerView: 3,
        freeMode: true,
        watchSlidesProgress: true,
        breakpoints: {
            481: { spaceBetween: 32 }
        }
    });
    var productBig = new Swiper ('.big-image', {
        loop: true,
        autoHeight: true,
        thumbs: {
            swiper: productThumb,
        }
    });
}

// =====================================================================
// 8. TRENDING OFFER COUNTDOWN TIMER
// =====================================================================

(function initOfferCountdown() {
    const timerEl = document.getElementById('offerCountdownTimer');
    if (!timerEl) return;

    // Read from the inline <script> variable — more reliable than data-attributes
    // which can be affected by template rendering or attribute parsing quirks.
    let secondsLeft = (typeof window.__offerSecondsRemaining === 'number')
        ? window.__offerSecondsRemaining
        : 0;

    // Resolve elements lazily so they're always current (ribbon appended later)
    function getOfferCard() { return document.getElementById('offerCard'); }
    function getMediaEl()   { const c = getOfferCard(); return c ? c.querySelector('.media') : null; }

    const dEl = document.getElementById('cd-days');
    const hEl = document.getElementById('cd-hours');
    const mEl = document.getElementById('cd-mins');
    const sEl = document.getElementById('cd-secs');

    function pad(n) { return String(n).padStart(2, '0'); }

    function render(s) {
        const days    = Math.floor(s / 86400);
        const hours   = Math.floor((s % 86400) / 3600);
        const minutes = Math.floor((s % 3600) / 60);
        const secs    = s % 60;
        if (dEl) dEl.querySelector('.cd-num').textContent = pad(days);
        if (hEl) hEl.querySelector('.cd-num').textContent = pad(hours);
        if (mEl) mEl.querySelector('.cd-num').textContent = pad(minutes);
        if (sEl) sEl.querySelector('.cd-num').textContent = pad(secs);
    }

    function onExpired() {
        const offerCard = getOfferCard();
        const mediaEl   = getMediaEl();

        // Blur image + show ribbon
        if (mediaEl) {
            mediaEl.classList.add('offer-expired');

            if (!mediaEl.querySelector('.offer-ended-ribbon')) {
                const ribbon = document.createElement('div');
                ribbon.className = 'offer-ended-ribbon';
                ribbon.innerHTML = '<span>OFFER ENDED</span>';
                // Guarantee positioning context in case CSS hasn't loaded yet
                mediaEl.style.position = 'relative';
                mediaEl.style.overflow = 'hidden';
                mediaEl.appendChild(ribbon);
            }
        }

        // Stop pulsing animation
        if (offerCard) offerCard.classList.remove('countdown-active');

        // Replace ticking numbers with a static pill
        timerEl.innerHTML =
            '<li style="background:#999;border-radius:6px;padding:6px 14px;' +
            'color:#fff;font-size:0.85rem;letter-spacing:1px;list-style:none;">' +
            'Offer Ended</li>';
    }

    if (secondsLeft <= 0) {
        render(0);
        onExpired();
        return;
    }

    // Start pulsing
    const offerCard = getOfferCard();
    if (offerCard) offerCard.classList.add('countdown-active');
    render(secondsLeft);

    const interval = setInterval(function () {
        secondsLeft -= 1;
        if (secondsLeft <= 0) {
            clearInterval(interval);
            render(0);
            onExpired();
        } else {
            render(secondsLeft);
        }
    }, 1000);
})();