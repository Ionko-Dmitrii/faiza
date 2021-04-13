// Get Cookie Method
const getCookie = function (name) {
  var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined // s if r == 2 else b тернарный оператор
};

// =============menu desktop==============

$(document).ready(function () {

// ==========menu hamburger============

  var activeMenu = ".open-menu";
  var menuHamburger = $(".menu .menu-hamburger");
  var backgroundHidden = $(".background-hidden");
  var body = $("body");
  var menuContent = $(".header .menu-content-parent");
  var cartContent = $(".header  .cart-content-parent");
  var menu = $(".header .menu");
  var mobileLanguageCon = $(".header .mobile-language_content");
  var mobileLanguage = $(".mobile-menu .mobile-language");
  var mobileMenu = $(".mobile-menu .menu-hamburger");
  var mobileCart = $(".mobile-menu .mobile-cart-but");
  var mobileContact = $(".mobile-menu .mobile-contact");
  var main = $("main");

  $(document).on("click", activeMenu, function () {
    $(this).toggleClass('active-mobil-menu');
    menuContent.toggleClass("show");
    body.toggleClass("body-hidden");
    main.toggleClass("paddingCon");
    backgroundHidden.toggleClass("show");
  });

// ================open cart=====================

  $(".cart-button").click(function () {
    cartContent.addClass("show");
    menuHamburger.addClass("active-cart");
    menuHamburger.removeClass("open-menu");
    menuHamburger.addClass("active-mobil-menu");
    body.addClass("body-hidden");
    main.addClass("paddingCon");
    backgroundHidden.addClass("show");
    menuContent.removeClass("show");
    menu.addClass("activeCart");
  });

  // ================close cart=====================

  var activeCart = ".active-cart";

  $(document).on("click", activeCart, function () {
    cartContent.removeClass("show");
    menuHamburger.removeClass("active-cart");
    menuHamburger.addClass("open-menu");
    menuHamburger.removeClass("active-mobil-menu");
    body.removeClass("body-hidden");
    main.removeClass("paddingCon");
    backgroundHidden.removeClass("show");
    menu.removeClass("activeCart");
  });

// ================close all ==============

  backgroundHidden.click(function () {
    $(this).removeClass("show");
    body.removeClass("body-hidden");
    main.removeClass("paddingCon");
    cartContent.removeClass("show");
    menu.removeClass("activeCart");
    menuHamburger.removeClass("active-cart");
    menuHamburger.addClass("open-menu");
    menuHamburger.removeClass("active-mobil-menu");
    menuContent.removeClass("show");
    mobileLanguageCon.removeClass("show");
    mobileLanguage.removeClass("active");
    mobileMenu.toggleClass("close-mobile-content");
    mobileCart.toggleClass("close-mobile-content");
    mobileContact.toggleClass("close-mobile-content");
  });
});

// =============menu mobile==============

$(document).ready(function () {
  var mobileMenu = $(".mobile-menu .menu-hamburger");
  var mobileCart = $(".mobile-menu .mobile-cart-but");
  var mobileContact = $(".mobile-menu .mobile-contact");
  var mobileHome = $(".mobile-menu .mobile-home");
  var mobileLanguage = $(".mobile-menu .mobile-language");
  var backgroundHidden = $(".background-hidden");
  var body = $("body");
  var menuContent = $(".header .menu-content-parent");
  var cartContent = $(".header  .cart-content-parent");
  var callContent = $(".header .mobile-call-parent");
  var closeCall = $(".header .close-mobile-call");
  var mobileLanguageCon = $(".header .mobile-language_content");

  mobileMenu.click(function () {
    $(this).toggleClass("active-mobil-menu");
    mobileLanguage.toggleClass("close-mobile-content");
    mobileCart.toggleClass("close-mobile-content");
    mobileContact.toggleClass("close-mobile-content");
    menuContent.toggleClass("show");
    body.toggleClass("body-hidden");
    cartContent.removeClass("show");
    mobileCart.removeClass("active");
  });

  mobileHome.click(function () {
    $(this).toggleClass("active");
  });

  mobileContact.click(function () {
    $(this).addClass("active");
    mobileLanguage.addClass("close-mobile-content");
    mobileCart.addClass("close-mobile-content");
    mobileMenu.addClass("close-mobile-content");
    body.addClass("body-hidden");
    callContent.addClass("show");
    mobileMenu.removeClass("show");
    mobileMenu.removeClass("active-mobil-menu");
    menuContent.removeClass("show");
    mobileLanguageCon.removeClass("show");
    mobileLanguage.removeClass("active");
    backgroundHidden.removeClass("show");
    cartContent.removeClass("show");
    mobileCart.removeClass("active");
  });

  closeCall.click(function () {
    mobileLanguage.removeClass("close-mobile-content");
    mobileCart.removeClass("close-mobile-content");
    mobileMenu.removeClass("close-mobile-content");
    mobileContact.removeClass("active");
    body.removeClass("body-hidden");
    callContent.removeClass("show");
  });

  mobileLanguage.click(function () {
    $(this).toggleClass("active");
    mobileMenu.toggleClass("close-mobile-content");
    mobileCart.toggleClass("close-mobile-content");
    mobileContact.toggleClass("close-mobile-content");
    body.toggleClass("body-hidden");
    backgroundHidden.toggleClass("show");
    mobileLanguageCon.toggleClass("show");
  });

  mobileCart.click(function () {
    $(this).toggleClass("active");
    mobileMenu.toggleClass("close-mobile-content");
    mobileLanguage.toggleClass("close-mobile-content");
    mobileContact.toggleClass("close-mobile-content");
    cartContent.toggleClass("show");
    body.toggleClass("body-hidden");
    menuContent.removeClass("show");
    mobileMenu.removeClass("active-mobil-menu");
  });

  // ===============select language==============

  $(".mobile-language_content .language-content a").click(function () {
    var textLang = $(this).text();
    $(".header .mobile-language").text(textLang);

  });

});

$(document).ready(function () {

  // ===============select language=============

  var buttonLang = $(".language-selection .language-button");

  buttonLang.click(function () {
    $(this).addClass("hide");
    $(this).siblings(".language-content").addClass("show");
    $(".decor").addClass("active");
    $(this).closest(".language-selection").addClass("active");
  });

  var selectLang = $(".language-selection .language-content a");
  var langText = "";

  $(".language-selection .language-content a:eq(0)").addClass("active");

  selectLang.click(function () {
    $(".decor").removeClass("active");
    $(this).closest(".language-selection").removeClass("active");
    selectLang.removeClass("active");
    $(this).addClass("active");
    langText = $(this).text();
    buttonLang.text(langText);
    $(this).closest(".language-content").removeClass("show");
    $(this).closest(".language-selection").find(".language-button").removeClass("hide");
  });

  // ===============add active for dish==============

  var costDish = ".portion-selection";

  $(".cost-dish-all").each(function (i, obj) {
    $(obj).children(".portion-selection:eq(0)").addClass("active");
  });


  $(document).on("click", costDish, function () {
    var indexItem = $(this).index()
    $(this).siblings(".cost-dish").removeClass("active");
    $(this).addClass("active");
    if ($(this).parent('.cost-dish-all').siblings('.add_cart_but_wrapper')
      .children('.add-cart').length > 1) {
      $(this).parent('.cost-dish-all').siblings('.add_cart_but_wrapper')
        .children('.add-cart').addClass('hide')
      $(this).parent('.cost-dish-all').siblings('.add_cart_but_wrapper')
        .children(`.add-cart:eq(${indexItem})`).removeClass('hide')
    }
  });

  var cartCostDish = ".cart-portion-selection";

  $(document).on("click", cartCostDish, function () {
    if ($(this).parent('.cost-dish_number').siblings('.cost-dish_number')
      .children('.cart-portion-selection').hasClass("active")) {
      $(this).toggleClass("active");
      $(this).siblings(".number-block").toggleClass("show")
    } else {
      $(this).addClass("active");
      $(this).siblings(".number-block").addClass("show")
    }
  });

  // ==============close card detail=============

  $(document).on("click", ".close-card-detail", function () {
    $(".dish-card_detail-parent").hide();
    $("body").removeClass("body-hidden");
  });

  // ========basket input=======

  var minus = ".minus-js";
  var plus = ".plus-js";
  $(document).on('click', minus, function () {
    var val = $(this).siblings(".input").find("input");
    if (val.val() <= val.attr("min")) {
      val.val(val.attr("min"));
    } else {
      var minusNum = val.val();
      minusNum--;
      val.val(minusNum)
    }
  });

  $(document).on('click', plus, function () {
    var val = $(this).siblings(".input").find("input");
    if (val.val() >= val.attr("max")) {
      val.val(val.attr("max"))
    } else {
      var plusNum = val.val();
      plusNum++;
      val.val(plusNum)
    }
  });

});


// ==============mask-tel==============

maskPhoneField();

function maskPhoneField() {
  $.each(document.getElementsByClassName("phone-mask"), function (i, obj) {
    new IMask(
      obj, {
        mask: '+{996} 000 000-000'
      });
  });
}


// ==============validation form================

$(document).ready(function () {

  $(".modal input").on("keyup", function () {

    var isValidInput = false;

    $(".modal .input input").each(function (i, obj) {
      if ($(obj).val() === "") {
        return isValidInput = false
      } else {
        isValidInput = true
      }
    });

    $(".modal").find('.disabled-btn').prop('disabled', !isValidInput);
  });

});


// ================open and close ordering================

var orderingCon = $(".modal-ordering ");

$(".open-ordering").on("click", function () {
  orderingCon.show();
});

$(".close-modal-ordering").on("click", function () {
  orderingCon.hide();
});


// =============open and close modal finish==============

var modalFinish = $(".modal-finish_content");

$(".close-modal_finish ").on("click", function () {
  modalFinish.removeClass("show");
});
