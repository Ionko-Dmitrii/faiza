var countBasket = $('.cart-button .count-item');
var basketCookie = getCookieD('BASKET_FAIZA');
var productIdArr = [];
var productCountArr = [];

function getCookieD(name) {
  var cookieArr = document.cookie.split(";");
  for (var i = 0; i < cookieArr.length; i++) {
    var cookiePair = cookieArr[i].split("=");
    if (name == cookiePair[0].trim()) {
      return decodeURIComponent(cookiePair[1]);
    }
  }
  return null;
}

function getCookieProduct() {
  basketCookie = getCookieD('BASKET_FAIZA');
  if (basketCookie) {
    if (basketCookie.length > 4) {
      basketCookie = basketCookie.replace(/\\054/g, '')
        .replace('"[', '')
        .replace(']"', '')
        .replace(/\\/g, '')
        .replace(/} {/g, '}, {')
        .replace(/:\s/g, ':')
        .replace(/\s"/g, ',"').split(', ')

      productIdArr = []
      productCountArr = []

      basketCookie.forEach(function (item) {
        var t = item.replace(/,/g, ', ')
        var b = JSON.parse(t)
        productIdArr.push(b['product_id'])
        productCountArr.push(b['count'])
      })
    }
  }
}

function setCountProduct() {
  getCookieProduct();
  var productCount = $('.cart-product_all .cart-product__ajax');
  var productContainer = $('.cart-product-container input');
  var containerSum = 0;

  if (basketCookie) {
    var reverseArr = productCountArr.reverse()
    productCount.each(function (i, item) {
      $(item).find('.cost-dish-all').find('input').val(reverseArr[i]);
      containerSum += Number(reverseArr[i]);
      productContainer.val(containerSum)
    });
  }
}

function setActiveForProduct() {
  setCountProduct();
  productItem = $('.popular-dishes_card .dish-card');

  getCookieProduct();
  productItem.each(function (i, item) {
    var itemId = $(item).find('.add-cart').attr('data-product-id')
    if (basketCookie) {
      productIdArr.forEach(function (obj) {
        if (Number(obj) === Number(itemId)) {
          $(item).find('.add-cart').addClass('active');
          $(item).find('.add-cart').text('ДОБАВЛЕНО');
        }
      })
    }
  });
}

setActiveForProduct();

function getCountBasketProduct() {
  var itemBasket = $('.cart-product_all .cart-product').length;
  if (itemBasket < 1) {
    countBasket.text("0")
  } else {
    countBasket.text(itemBasket - 1)
  }
}

getCountBasketProduct();

$(document).on("click", '.open-card-detail', function (e) {
  e.stopPropagation();
  e.preventDefault();
  var url = $(this).data('url');
  var modal = $('.dish-card_detail-parent');
  var productId = $(this).data('product-id');
  var thisItem = $(this).siblings('.dish-card_description')
    .children('.add-cart');
  modal.html('');
  $.ajax({
    url: url,
    method: 'GET',
    data: {
      'csrfmiddlewaretoken': getCookie('csrftoken'),
      'productId': productId,
    },
    success: function (data) {
      modal.html(data['rendered_html']);
      modal.css('display', 'block');
      $("body").addClass("body-hidden");
      var modalProduct = $('.dish-card_detail .add-cart');
      if (thisItem.hasClass("active")) {
        modalProduct.addClass("active");
        modalProduct.text("ДОБАВЛЕНО");
      }
    },
    error: function (xhr, status) {
      alert("Sorry, there was a problem!");
    },
  });
})

$('.menu-page_tabs .link-menu').click(function () {
  var url = $(this).data('url');
  var urlLink = $(this).data('link-url');
  var products = $('.popular-dishes__inner');
  var categoryId = $(this).data('products-id');
  var categoriesItem = $('.menu-page_tabs .link-menu');
  var linkHeader = $('.menu-content-inner ul a');
  var linkCategoryNext = $('.menu-page_link a');
  $.ajax({
    url: url,
    method: 'GET',
    data: {
      'csrfmiddlewaretoken': getCookie('csrftoken'),
      'categoryId': categoryId,
    },
    success: function (data) {
      products.html(data['render_products_html']);
      window.history.pushState(window.location.pathname, "Your New Title", urlLink);
      var arrCategory = [];
      var indexObj = 0;
      categoriesItem.each(function (i, obj) {
        arrCategory.push($(obj))
        if ($(obj).attr('data-link-url') === window.location.pathname) {
          $(this).addClass('active');
          indexObj = i
        } else {
          $(obj).removeClass("active")
        }
      });

      var nextObj = arrCategory[0];

      if (indexObj >= arrCategory.length - 1) {
        nextObj = arrCategory[0]
      } else {
        nextObj = arrCategory[indexObj + 1]
      }

      var nextObjUrl = nextObj.attr('data-link-url');
      linkCategoryNext.text(nextObj.context.innerText)
      linkCategoryNext.attr('href', nextObjUrl)

      linkHeader.each(function (i, obj) {
        if ($(obj).attr('href') === window.location.pathname) {
          $(this).addClass('active')
        } else {
          $(obj).removeClass("active")
        }
      });
      setActiveForProduct();
    },
    error: function (xhr, status) {
      alert("Sorry, there was a problem!");
    },
  })
})

$(document).on("click", '.add-cart', function () {
  var url = $(this).data('url');
  var wrapperProducts = $('.cart-product_all');
  var productId = $(this).data('product-id');
  var thisItem = $(this);
  var sum = $('.cart-product_row .sum');
  thisItem.css('transform', 'scale(.9)');
  setTimeout(function () {
    thisItem.css('transform', 'scale(1)')
  }, 200)
  wrapperProducts.html('');
  $.ajax({
    url: url,
    method: 'POST',
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      'productId': productId,
    },
    success: function (data) {
      sum.text(data.sum_products);
      wrapperProducts.html(data.header_item);
      if (thisItem.hasClass("active")) {
        thisItem.text('добавить В заказ');
        thisItem.removeClass("active");
      } else {
        thisItem.text('ДОБАВЛЕНО');
        thisItem.addClass("active");
      }
      getCountBasketProduct();
      setCountProduct()
    },
    error: function (xhr, status) {
      alert("Sorry, there was a problem!");
    },
  });

})

$(document).on("click", '.button-count-ajax', function () {
  var thisItem = $(this)
  var url = $(this).data('url');
  var productId = $(this).closest('.dish-card_description')
    .children('.remove-card').data('product-id');
  var sumProducts = $('.cart-product_row .sum');

  if (timeout) clearTimeout(timeout);
  var timeout = setTimeout(function () {
    var countProduct = thisItem.siblings('.input').children('input').val();

    $.ajax({
      url: url,
      method: 'POST',
      data: {
        csrfmiddlewaretoken: getCookie('csrftoken'),
        'productId': productId,
        'count': countProduct,
      },
      success: function (data) {
        sumProducts.text(data.sum_products)
        setCountProduct();
      },
      error: function (xhr, status) {
        alert("Sorry, there was a problem!");
      },
    });
  }, 200)

})

$(document).on("click", '.remove-card', function () {
  var sum = $('.cart-product_row .sum');
  var url = $(this).data('url');
  var product_id = $(this).data('product-id');
  var wrapperProducts = $('.cart-product_all');
  productItem = $('.popular-dishes_card .dish-card');
  $.ajax({
    url: url,
    method: 'POST',
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      'productId': product_id,
    },
    success: function (data) {
      sum.text(data.sum_products);
      wrapperProducts.html(data.header_item);
      getCountBasketProduct();
      getCookieProduct();
      setCountProduct();
      productItem.each(function (i, obj) {
        if ($(obj).find('.add-cart').attr('data-product-id') === String(product_id)) {
          $(obj).find('.add-cart').removeClass('active');
          $(obj).find('.add-cart').text('добавить В заказ');
        }
      })
    },
    error: function (xhr, status) {
      alert("Sorry, there was a problem!");
    },
  })
});


$(document).on("click", '.dish-card_detail .add-cart', function () {
  productItem = $('.popular-dishes_card .dish-card');
  thisId = $(this).attr('data-product-id');
  thisItem = $(this);
  productItem.each(function (i, obj) {
    if (thisItem.hasClass("active")) {
      if ($(obj).find('.add-cart').attr('data-product-id') === String(thisId)) {
        $(obj).find('.add-cart').removeClass('active');
        $(obj).find('.add-cart').text('добавить В заказ');
      }
    } else {
      if ($(obj).find('.add-cart').attr('data-product-id') === String(thisId)) {
        $(obj).find('.add-cart').addClass('active');
        $(obj).find('.add-cart').text('ДОБАВЛЕНО');
      }
    }
  })
})


$(document).on("click", '.clear-cart', function () {
  var url = $(this).data('url');
  var wrapperProducts = $('.cart-product_all');

  $.ajax({
    url: url,
    method: 'POST',
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
    },
    success: function (data) {
      wrapperProducts.html(data.clear_basket);
      getCountBasketProduct();
      getCookieProduct();
      setCountProduct();
      productItem.each(function (i, obj) {
        $(obj).find('.add-cart').removeClass('active');
        $(obj).find('.add-cart').text('добавить В заказ');
      })
    },
    error: function (xhr, status) {
      alert("Sorry, there was a problem!");
    },
  })
});