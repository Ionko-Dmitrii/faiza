var countBasket = $('.cart-button .count-item');
var basketCookie = getCookieD('BASKET_FAIZA');
var productItem = $('.popular-dishes_card .dish-card');
var productIdArr = [];
var productCountArr = [];
var productCountTwoArr = [];

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

      productIdArr = [];
      productCountArr = [];
      productCountTwoArr = [];

      basketCookie.forEach(function (item) {
        var t = item.replace(/,/g, ', ')
        var b = JSON.parse(t)
        productIdArr.push(b['product_id'])
        productCountArr.push(b['count'])
        productCountTwoArr.push(b['count_two'])
      })
    } else {
      basketCookie = [];
      productIdArr = [];
      productCountArr = [];
      productCountTwoArr = [];
    }
  } else {
    basketCookie = [];
    productIdArr = [];
    productCountArr = [];
    productCountTwoArr = [];
  }
}

function setActiveForProduct() {
  productItem = $('.popular-dishes_card .dish-card');

  getCookieProduct();
  var selectorDict = {};
  var selectorList = []
  productItem.each(function (i, item) {
    var itemId = $(item).find('.add-cart').attr('data-product-id')
    if (basketCookie) {
      productIdArr.forEach(function (obj) {
        if (Number(obj) === Number(itemId)) {
          selectorDict[itemId] = $(item)
        }
      })
    }
  });

  productIdArr.forEach(function (id) {
    selectorList.push(selectorDict[id])
  })
  productCountArr.forEach(function (count, index) {
    if (count > 0) {
      selectorList[index].find('.add-cart-one').addClass("active")
        .text('ДОБАВЛЕНО')
    }
  })
  productCountTwoArr.forEach(function (count, index) {
    if (count > 0) {
      selectorList[index].find('.add-cart-two').addClass("active")
        .text('ДОБАВЛЕНО')
    }
  })
}

setActiveForProduct();

function setCountBasketProduct() {
  var sumProduct = 0;
  getCookieProduct();

  productCountArr.forEach(function (count) {
    sumProduct += count
  })
  productCountTwoArr.forEach(function (count) {
    sumProduct += count
  })

  countBasket.text(sumProduct)
}

setCountBasketProduct();

function setActiveForProductAjax(thisItem, productId) {
  productItem.each(function () {
    var thisProductId = $(this).find(".open-card-detail")
      .attr('data-product-id');
    if (productId === Number(thisProductId)) {
      if (thisItem.hasClass("active")) {
        $(this).find(".add-cart-one").addClass("active")
          .text('ДОБАВЛЕНО')
      } else {
        $(this).find(".add-cart-one").removeClass("active")
          .text('добавить В заказ')
      }
    }
  })
}

function setActiveForProductAjaxTwo(thisItem, productId) {
  productItem.each(function () {
    var thisProductId = $(this).find(".open-card-detail")
      .attr('data-product-id');
    if (productId === Number(thisProductId)) {
      if (thisItem.hasClass("active")) {
        $(this).find(".add-cart-two").addClass("active")
          .text('ДОБАВЛЕНО')
      } else {
        $(this).find(".add-cart-two").removeClass("active")
          .text('добавить В заказ')
      }
    }
  })
}

function addActiveClassForCartProduct(thisItem) {
  if (thisItem.parent('.cost-dish_number').siblings('.cost-dish_number')
    .children('.cart-portion-selection').hasClass("active")) {
    thisItem.toggleClass("active");
    thisItem.siblings(".number-block").toggleClass("show")
  } else {
    thisItem.addClass("active");
    thisItem.siblings(".number-block").addClass("show")
  }
}

//================open preview product================

$(document).on("click", '.open-card-detail', function (e) {
  e.stopPropagation();
  e.preventDefault();
  var url = $(this).data('url');
  var modal = $('.dish-card_detail-parent');
  var productId = $(this).data('product-id');
  var thisButOne = $(this).siblings('.dish-card_description')
    .find('.add-cart-one');
  var thisButTwo = $(this).siblings('.dish-card_description')
    .find('.add-cart-two');
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
      var previewButOne = $('.dish-card_detail .add-cart-one');
      var previewButTwo = $('.dish-card_detail .add-cart-two');
      if (thisButOne.hasClass("active")) {
        previewButOne.addClass("active").text("ДОБАВЛЕНО");
      }
      if (thisButTwo.hasClass("active")) {
        previewButTwo.addClass("active").text("ДОБАВЛЕНО");
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
      window.history.pushState(window.location.pathname, "Your New Title",
        urlLink);
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

$(document).on("click",
  '.add_cart_but_wrapper .add-cart-one',
  function () {
    var url = $(this).data('url');
    var wrapperProducts = $('.cart-product_all');
    var productId = $(this).data('product-id');
    var thisItem = $(this);
    var sum = $('.cart-product_row .sum');
    thisItem.css('transform', 'scale(.9)');
    setTimeout(function () {
      thisItem.css('transform', 'scale(1)')
    }, 300)
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
          thisItem.text('добавить В заказ').removeClass("active");
        } else {
          thisItem.text('ДОБАВЛЕНО').addClass("active");
        }
        setActiveForProductAjax(thisItem, productId);
        setCountBasketProduct();
      },
      error: function (xhr, status) {
        alert("Sorry, there was a problem!");
      },
    });

  })

$(document).on("click",
  '.add_cart_but_wrapper .add-cart-two',
  function () {
    var url = $(this).data('url');
    var wrapperProducts = $('.cart-product_all');
    var productId = $(this).data('product-id');
    var thisItem = $(this);
    var sum = $('.cart-product_row .sum');
    thisItem.css('transform', 'scale(.9)');
    setTimeout(function () {
      thisItem.css('transform', 'scale(1)')
    }, 300)
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
          thisItem.text('добавить В заказ').removeClass("active");
        } else {
          thisItem.text('ДОБАВЛЕНО').addClass("active");
        }
        setActiveForProductAjaxTwo(thisItem, productId)
        setCountBasketProduct();
      },
      error: function (xhr, status) {
        alert("Sorry, there was a problem!");
      },
    });

  })

$(document).on(
  "click", '.portion_big .button-count-ajax', function () {
    var thisItem = $(this)
    var url = $(this).data('url');
    var productId = $(this).closest('.dish-card_description')
      .children('.remove-card').data('product-id');
    var countProductVal = $('.count_product');
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
          countProductVal.val(data.count_product);
          setCountBasketProduct()
        },
        error: function (xhr, status) {
          alert("Sorry, there was a problem!");
        },
      });
    }, 200)

  })

$(document).on(
  "click", '.portion_small .button-count-ajax', function () {
    var thisItem = $(this)
    var url = $(this).data('url');
    var productId = $(this).closest('.dish-card_description')
      .children('.remove-card').data('product-id');
    var countProductVal = $('.count_product');
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
          'count_two': countProduct,
        },
        success: function (data) {
          sumProducts.text(data.sum_products)
          countProductVal.val(data.count_product);
          setCountBasketProduct();
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
      setCountBasketProduct();
      getCookieProduct();
      productItem.each(function (i, obj) {
        if ($(obj).find('.add-cart')
          .attr('data-product-id') === String(product_id)) {
          $(obj).find('.add-cart').removeClass('active')
            .text('добавить В заказ');
        }
      })
    },
    error: function (xhr, status) {
      alert("Sorry, there was a problem!");
    },
  })
});


$(document).on("click", '.clear-cart', function () {
  var url = $(this).data('url');
  var wrapperProducts = $('.cart-product_all');
  var sumProducts = $('.cart-product_row .sum');

  $.ajax({
    url: url,
    method: 'POST',
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
    },
    success: function (data) {
      wrapperProducts.html(data.clear_basket);
      sumProducts.text(data.sum_products);
      productItem.each(function (i, obj) {
        $(obj).find('.add-cart').removeClass('active')
          .text('добавить В заказ');
      });
      setCountBasketProduct();
    },
    error: function (xhr, status) {
      alert("Sorry, there was a problem!");
    },
  })
});

$(document).on('click', '.portion_big .cost-dish ', function () {
  var url = $(this).data('url');
  var productId = $(this).data('product-id');
  var sumProducts = $('.cart-product_row .sum');
  var countProductVal = $('.count_product');
  var thisItem = $(this);
  var thisCount = $(this).siblings('.number-block').find('input');

  $.ajax({
    url: url,
    method: 'POST',
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      productId: productId,
    },
    success: function (data) {
      sumProducts.text(data.sum_products);
      countProductVal.val(data.count_product);
      thisCount.val(data.count_one);
      addActiveClassForCartProduct(thisItem)
      setActiveForProductAjax(thisItem, productId);
      setCountBasketProduct();
    },
    error: function (xhr, status) {
      alert("Sorry, there was a problem!");
    }
  })
})

$(document).on('click', '.portion_small .cost-dish ', function () {
  var url = $(this).data('url');
  var productId = $(this).data('product-id');
  var sumProducts = $('.cart-product_row .sum');
  var countProductVal = $('.count_product');
  var thisItem = $(this);
  var thisCount = $(this).siblings('.number-block').find('input');

  $.ajax({
    url: url,
    method: 'POST',
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      productId: productId,
    },
    success: function (data) {
      sumProducts.text(data.sum_products);
      countProductVal.val(data.count_product);
      thisCount.val(data.count_two);
      addActiveClassForCartProduct(thisItem)
      setActiveForProductAjaxTwo(thisItem, productId)
      setCountBasketProduct();
    },
    error: function (xhr, status) {
      alert("Sorry, there was a problem!");
    }
  })
})


$('.modal-ordering form').on('submit', function (e) {
  e.preventDefault()
  var form = $(this);
  var modal = $(".modal-ordering ");
  var modalFinish = $(".modal-finish_content");
  var cleanContextBasket = $('.cart-product_all');
  var sumProducts = $('.cart-product_row .sum');
  var countContainer = $('.count_product').val();
  var formSerializeArr = form.serializeArray();
  var formSerializeDict = {};
  for (let i of formSerializeArr) {
    formSerializeDict[i['name']] = i['value']
  }

  $.ajax({
    url: form.attr('action'),
    method: 'POST',
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      product_sum: sumProducts.text(),
      form_fields: JSON.stringify(formSerializeDict),
      count_container: countContainer,
    },

    success: function (data) {
      form[0].reset();
      modal.hide();
      cleanContextBasket.html(data.clear_basket);
      sumProducts.text(data.sum_products);
      modalFinish.addClass("show");
      setCountBasketProduct();
      productItem.each(function (i, obj) {
        $(obj).find('.add-cart').removeClass('active')
          .text('добавить В заказ');
      });
    },

    error: function (error) {
      error.responseJSON.message.forEach(function (item) {
        form.find(`.input_form[name=${item[0]}]`).siblings('span')
          .text(item[1]);
      })
    },
  })
})