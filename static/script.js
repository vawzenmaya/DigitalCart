// =============================================================
// 1. Copy department/nav menus into mobile off-canvas drawer
// =============================================================
(function copyMenu() {
    const dptCategory = document.querySelector('.dpt-cat');
    const dptPlace    = document.querySelector('.departments');
    if (dptCategory && dptPlace) dptPlace.innerHTML = dptCategory.innerHTML;

    const mainNav  = document.querySelector('.header-nav nav');
    const navPlace = document.querySelector('.off-canvas nav');
    if (mainNav && navPlace) navPlace.innerHTML = mainNav.innerHTML;

    const topNav   = document.querySelector('.header-top .wrapper');
    const topPlace = document.querySelector('.off-canvas .thetop-nav');
    if (topNav && topPlace) topPlace.innerHTML = topNav.innerHTML;
})();


// =============================================================
// 2. Mobile menu open / close
// =============================================================
(function initMobileMenu() {
    const site        = document.querySelector('.site');
    const menuButton  = document.querySelector('.trigger');
    const closeButton = document.querySelector('.t-close');
    if (!site) return;

    menuButton?.addEventListener('click', (e) => {
        e.preventDefault();
        site.classList.toggle('showmenu');
    });
    closeButton?.addEventListener('click', (e) => {
        e.preventDefault();
        site.classList.remove('showmenu');
    });
})();


// =============================================================
// 3. Mobile sub-menu accordion
// =============================================================
(function initSubMenus() {
    document.querySelectorAll('.has-child .icon-small').forEach((toggle) => {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            const parent = this.closest('.has-child');
            // Collapse all siblings first
            document.querySelectorAll('.has-child').forEach((el) => {
                if (el !== parent) el.classList.remove('expand');
            });
            parent.classList.toggle('expand');
        });
    });
})();


// =============================================================
// 4. Hero slider
// =============================================================
(function initHeroSlider() {
    const el = document.querySelector('.myslider.swiper');
    if (!el) return;
    new Swiper('.myslider.swiper', {
        loop: true,
        autoplay: { delay: 3500, disableOnInteraction: false },
        pagination: { el: '.swiper-pagination' },
        speed: 1200,
    });
})();


// =============================================================
// 5. Search overlay toggle
// =============================================================
(function initSearch() {
    const site         = document.querySelector('.site');
    const searchButton = document.querySelector('.t-search');
    const closeButton  = document.querySelector('.search-close');
    if (!site) return;

    searchButton?.addEventListener('click', (e) => {
        e.preventDefault();
        site.classList.toggle('showsearch');
    });
    closeButton?.addEventListener('click', (e) => {
        e.preventDefault();
        site.classList.remove('showsearch');
    });
})();


// =============================================================
// 6. Department menu toggle (category / product pages)
// =============================================================
(function initDptMenu() {
    const page      = document.getElementById('page');   // #page — what the CSS targets
    const dptButton = document.querySelector('.dpt-cat .dpt-trigger');
    if (!page || !dptButton) return;

    dptButton.addEventListener('click', (e) => {
        e.preventDefault();
        page.classList.toggle('showdpt');
    });

    // Close when clicking anywhere outside the dpt-cat panel
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dpt-cat') && page.classList.contains('showdpt')) {
            page.classList.remove('showdpt');
        }
    });
})();


// =============================================================
// 7. Product detail image slider
// =============================================================
(function initProductSlider() {
    const thumbEl = document.querySelector('.small-image');
    const bigEl   = document.querySelector('.big-image');
    if (!thumbEl || !bigEl) return;

    const productThumb = new Swiper('.small-image', {
        loop: true,
        spaceBetween: 10,
        slidesPerView: 3,
        freeMode: true,
        watchSlidesProgress: true,
        breakpoints: { 481: { spaceBetween: 32 } },
    });

    new Swiper('.big-image', {
        loop: true,
        autoHeight: true,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        thumbs: { swiper: productThumb },
    });
})();


// =============================================================
// 8. Mini cart popup
// =============================================================
(function initMiniCart() {
    const popup   = document.querySelector('.mini-cart');
    const trigger = document.querySelector('.cart-trigger');
    if (!popup || !trigger) return;

    trigger.addEventListener('click', () => {
        setTimeout(() => popup.classList.add('show'), 250);
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.mini-cart') && popup.classList.contains('show')) {
            popup.classList.remove('show');
        }
    });
})();


// =============================================================
// 9. Filter panel popup (category page)
// =============================================================
(function initFilterPanel() {
    const panel   = document.querySelector('.filter');
    const trigger = document.querySelector('.filter-trigger');
    if (!panel || !trigger) return;

    trigger.addEventListener('click', () => {
        setTimeout(() => panel.classList.add('show'), 250);
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.filter') && panel.classList.contains('show')) {
            panel.classList.remove('show');
        }
    });
})();


// =============================================================
// 10. Offer countdown timer
// =============================================================
(function initOfferCountdown() {
    const timerEl = document.getElementById('offerCountdownTimer');
    if (!timerEl) return;

    let secondsLeft = parseInt(timerEl.dataset.seconds || '0', 10);

    const dEl = document.getElementById('cd-days');
    const hEl = document.getElementById('cd-hours');
    const mEl = document.getElementById('cd-mins');
    const sEl = document.getElementById('cd-secs');

    function pad(n) { return String(n).padStart(2, '0'); }

    function render(s) {
        const d = Math.floor(s / 86400);
        const h = Math.floor((s % 86400) / 3600);
        const m = Math.floor((s % 3600) / 60);
        const sec = s % 60;
        if (dEl) dEl.querySelector('.cd-num').textContent = pad(d);
        if (hEl) hEl.querySelector('.cd-num').textContent = pad(h);
        if (mEl) mEl.querySelector('.cd-num').textContent = pad(m);
        if (sEl) sEl.querySelector('.cd-num').textContent = pad(sec);
    }

    function onExpired() {
        const offerCard = document.getElementById('offerCard');
        const mediaEl   = offerCard?.querySelector('.offer-media');

        if (mediaEl) {
            mediaEl.classList.add('offer-expired');
            if (!mediaEl.querySelector('.offer-ended-ribbon')) {
                const ribbon = document.createElement('div');
                ribbon.className = 'offer-ended-ribbon';
                ribbon.innerHTML = '<span>OFFER<br>ENDED</span>';
                mediaEl.appendChild(ribbon);
            }
        }

        const offerBlock = timerEl.closest('.offer');
        if (offerBlock) {
            offerBlock.innerHTML =
                '<p style="font-size:0.8rem;color:#999;letter-spacing:1px;text-transform:uppercase;margin:0;">' +
                '<span>Offer Ended</span><br>Wait for the next offer</p>';
        }
    }

    if (secondsLeft <= 0) {
        render(0);
        onExpired();
        return;
    }

    render(secondsLeft);

    const interval = setInterval(() => {
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


// =============================================================
// 11. Stock bar widths (set via data-width attribute)
// =============================================================
document.querySelectorAll('.available[data-width]').forEach((el) => {
    el.style.width = el.dataset.width + '%';
});


// =============================================================
// 12. Category sort dropdown (non-form click-to-redirect)
// =============================================================
(function initSortDropdown() {
    document.querySelectorAll('.item-sortir ul li a').forEach((link) => {
        link.addEventListener('click', function (e) {
            // Only intercept if it already has an href (the template sets them)
            if (this.getAttribute('href') && this.getAttribute('href') !== '#') return;
            e.preventDefault();
        });
    });
})();