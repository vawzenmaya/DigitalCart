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
    const page      = document.getElementById('page');
    const dptButton = document.querySelector('.dpt-cat .dpt-trigger');
    if (!page || !dptButton) return;

    dptButton.addEventListener('click', (e) => {
        e.preventDefault();
        page.classList.toggle('showdpt');
    });

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
        const d   = Math.floor(s / 86400);
        const h   = Math.floor((s % 86400) / 3600);
        const m   = Math.floor((s % 3600) / 60);
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
            if (this.getAttribute('href') && this.getAttribute('href') !== '#') return;
            e.preventDefault();
        });
    });
})();


// =============================================================
// 13. Quantity +/- controls (product detail & cart)
// =============================================================
(function initQtyControls() {
    document.querySelectorAll('.qty-control').forEach((ctrl) => {
        const input   = ctrl.querySelector('input[type="number"], input[type="text"]');
        const minusBtn = ctrl.querySelector('.minus');
        const plusBtn  = ctrl.querySelector('.plus');
        if (!input) return;

        const getMax = () => parseInt(input.max || '9999', 10);
        const getMin = () => parseInt(input.min || '1', 10);

        minusBtn?.addEventListener('click', (e) => {
            if (minusBtn.tagName === 'A' || minusBtn.type === 'submit') return;
            
            e.preventDefault();
            const val = parseInt(input.value, 10) || 1;
            if (val > getMin()) {
                input.value = val - 1;
                input.dispatchEvent(new Event('change'));
            }
        });

        plusBtn?.addEventListener('click', (e) => {
            if (plusBtn.tagName === 'A' || plusBtn.type === 'submit') return;
            
            e.preventDefault();
            const val = parseInt(input.value, 10) || 1;
            if (val < getMax()) {
                input.value = val + 1;
                input.dispatchEvent(new Event('change'));
            }
        });

        input.addEventListener('change', () => {
            let val = parseInt(input.value, 10);
            if (isNaN(val) || val < getMin()) val = getMin();
            if (val > getMax()) val = getMax();
            input.value = val;
        });
    });
})();


// =============================================================
// 14. Toast notification system
// =============================================================
(function initToasts() {
    window.showToast = function (message, type = 'info', duration = 3000) {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.style.cssText =
                'position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;' +
                'display:flex;flex-direction:column;gap:0.5rem;';
            document.body.appendChild(container);
        }

        const colors = {
            success: '#10ac84',
            error:   '#e74c3c',
            info:    '#794afa',
            warning: '#f39c12',
        };

        const toast = document.createElement('div');
        toast.style.cssText =
            `background:${colors[type] || colors.info};color:#fff;` +
            'padding:0.75rem 1.25rem;border-radius:8px;font-size:13px;' +
            'box-shadow:0 4px 16px rgba(0,0,0,0.2);max-width:320px;' +
            'opacity:0;transform:translateX(20px);' +
            'transition:opacity 0.25s,transform 0.25s;';
        toast.textContent = message;
        container.appendChild(toast);

        requestAnimationFrame(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateX(0)';
        });

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(20px)';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    };
})();


// =============================================================
// 15. "Add to Cart" / Wishlist hover-button feedback
// =============================================================
(function initCartWishlistButtons() {
    document.querySelectorAll('.social-info').forEach((btn) => {
        const icon = btn.querySelector('i');
        if (!icon) return;

        if (icon.classList.contains('ri-heart-line')) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                icon.classList.replace('ri-heart-line', 'ri-heart-fill');
                btn.closest('li')?.classList.add('active');
                window.showToast?.('Added to Wishlist', 'success');
            });
        }

        if (icon.classList.contains('ri-shopping-cart-line')) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                window.showToast?.('Added to Cart', 'success');
            });
        }
    });

    const cartForm = document.querySelector('.single-product form');
    cartForm?.addEventListener('submit', () => {
        window.showToast?.('Adding to Cart...', 'success');
    });
});


// =============================================================
// 16. Share button — Web Share API with clipboard fallback
// =============================================================
(function initShareButton() {
    const shareLinks = document.querySelectorAll('a[data-share], a[onclick*="clipboard"]');
    shareLinks.forEach((btn) => {
        btn.removeAttribute('onclick');
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const url   = window.location.href;
            const title = document.title;
            if (navigator.share) {
                try {
                    await navigator.share({ title, url });
                } catch (_) { /* user cancelled */ }
            } else {
                try {
                    await navigator.clipboard.writeText(url);
                    window.showToast?.('Link copied to clipboard!', 'info');
                } catch (_) {
                    window.showToast?.('Copy this link: ' + url, 'info', 5000);
                }
            }
        });
    });
})();


// =============================================================
// 17. Back-to-top button
// =============================================================
(function initBackToTop() {
    const btn = document.createElement('button');
    btn.id = 'back-to-top';
    btn.innerHTML = '<i class="ri-arrow-up-line"></i>';
    btn.setAttribute('aria-label', 'Back to top');
    btn.style.cssText =
        'position:fixed;bottom:5rem;right:1.5rem;z-index:999;' +
        'width:42px;height:42px;border-radius:50%;border:none;cursor:pointer;' +
        'background:var(--secondary-dark-color);color:#fff;font-size:1.2rem;' +
        'display:flex;align-items:center;justify-content:center;' +
        'opacity:0;transform:translateY(10px);' +
        'transition:opacity 0.3s,transform 0.3s;box-shadow:0 4px 12px rgba(0,0,0,0.2);';
    document.body.appendChild(btn);

    const toggle = () => {
        const visible = window.scrollY > 400;
        btn.style.opacity  = visible ? '1' : '0';
        btn.style.transform = visible ? 'translateY(0)' : 'translateY(10px)';
        btn.style.pointerEvents = visible ? 'auto' : 'none';
    };

    window.addEventListener('scroll', toggle, { passive: true });
    btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
})();