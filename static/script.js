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