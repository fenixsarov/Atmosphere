var WIDGET_KEY = "944904f5d9ddcfe57136d73460d512e0";
var aeWidgetIframe;

Array.prototype.forEach || (Array.prototype.forEach = function (a, b) {
  var c, d;
  if (null == this) throw new TypeError(" this is null or not defined");
  var e = Object(this),
    f = e.length >>> 0;
  if ("function" != typeof a) throw new TypeError(a + " is not a function");
  for (arguments.length > 1 && (c = b), d = 0; f > d;) {
    var g;
    d in e && (g = e[d], a.call(c, g, d, e)), d++
  }
});

function parseQueryString(a) {
  var b = {};
  return a.split("&").forEach(function (a) {
    var c = a.split("=");
    0 !== c[0].length && c[1] && (b[c[0]] = c[1])
  }), b
};

function encodeData(data) {
  return Object.keys(data).map(function (key) {
    return [key, data[key]].map(encodeURIComponent).join("=");
  }).join("&");
}

var aeHandle = function (win, doc, loc, cur_script) {
  function Sweety() {

    var sweety = function (element) {
      return new SweetyElement(element);
    };

    var SweetyElement = function (element) {
      var elem;
      if (typeof element === 'string' && element.length > 0) {
        if (element.substr(0, 1) === '<') {
          elem = fn.create(element);
        } else {
          elem = fn.find(document, element);
        }
      } else if (typeof element === 'object' && element !== null) {
        elem = element;
      }
      this.elements = [];
      var type = Object.prototype.toString.call(elem);
      if (elem) {
        if (
          type === '[object HTMLCollection]' ||
          type === '[object NodeList]'
        ) {
          this.elements = Array.prototype.slice.call(elem);
        } else if (
          type === '[object Array]'
        ) {
          this.elements = elem;
        } else if (
          elem.toString() === '[SweetyElement]'
        ) {
          this.elements = elem.elements;
        } else {
          this.elements = [elem];
        }
      }
      return this;
    };

    var fn = sweety.fn = {

      create: function (html) {
        var a = document.createElement('div');
        a.innerHTML = html;
        return a.children;
      },

      find: function (parent, selector) {
        var elem;
        switch (selector.substr(0, 1)) {
          case '.':
            elem = parent.getElementsByClassName(selector.substr(1));
            break;
          case '#':
            elem = parent.getElementById(selector.substr(1));
            break;
          case '@':
            elem = parent.getElementsByName(selector.substr(1));
            break;
          default:
            elem = parent.getElementsByTagName(selector);
        }
        return elem;
      },

      each: function (elems, cb) {
        for (var i = 0, l = elems.length; i < l; i++) {
          cb(elems[i], i, elems);
        }
      },

      objEach: function (elems, cb) {
        for (var i in elems) {
          if (elems.hasOwnProperty(i)) {
            cb(i, elems[i]);
          }
        }
      },

      contains: function (subject, search) {
        return subject.indexOf(search) !== -1;
      },

      getClasses: function (elem) {
        if (elem.className === '') {
          return [];
        }
        return elem.className.split(/\s+/);
      },
      saveClasses: function (elem, elemClasses) {
        elem.className = elemClasses.join(' ');
      },

      getStyles: function (elem) {
        var styles = elem.style.cssText.split(/;\s*/);
        var stylesObject = {};
        this.each(styles, function (item) {
          var pair = item.split(/:\s*/);
          if (pair.length !== 2) {
            return;
          }
          stylesObject[pair[0]] = pair[1];
        });
        return stylesObject;
      },
      saveStyles: function (elem, stylesObject) {
        var stylesArray = [];
        this.objEach(stylesObject, function (styleName, styleValue) {
          stylesArray.push(styleName + ':' + styleValue);
        });
        elem.style.cssText = stylesArray.join(';');
      }

    };

    SweetyElement.prototype = {

      toArray: function () {
        return this.elements;
      },

      findChild: function (selector) {
        if (!this.elements[0]) {
          return sweety();
        }
        return sweety(fn.find(this.elements[0], selector));
      },
      findParent: function (selector) {
        if (!this.elements[0]) {
          return sweety();
        }
        var elem = this.elements[0];
        if (!selector) {
          return this.parent();
        }
        if (selector.substr(0, 1) === '.') {
          do {
            elem = elem.parentElement;
          } while (!fn.contains(fn.getClasses(elem), selector.substr(1)));
        } else {
          do {
            elem = elem.parentElement;
          } while (!(elem.tagName.toUpperCase() === selector.toUpperCase()));
        }
        return sweety(elem);
      },
      parent: function () {
        if (!this.elements[0]) {
          return sweety();
        }
        return sweety(this.elements[0].parentElement);
      },

      forEach: function (cb) {
        fn.each(this.elements, cb);
        return this;
      },

      getProp: function (key) {
        if (!this.elements[0]) {
          return undefined;
        }
        return this.elements[0][key];
      },
      setProp: function (key, value) {
        var properties = {};
        if (typeof key === 'object') {
          properties = key;
        } else {
          properties[key] = value;
        }
        this.forEach(function (elem) {
          fn.objEach(properties, function (key, value) {
            elem[key] = value;
          });
        });
        return this;
      },
      prop: function (key, value) {
        if (
          typeof value !== 'undefined' ||
          typeof key === 'object'
        ) {
          return this.setProp(key, value);
        }
        return this.getProp(key);
      },

      getAttr: function (key) {
        if (!this.elements[0]) {
          return null;
        }
        return this.elements[0].getAttribute(key);
      },
      setAttr: function (key, value) {
        var attributes = {};
        if (key.toString() === '[object Object]') {
          attributes = key;
        } else {
          attributes[key] = value;
        }
        this.forEach(function (elem) {
          fn.objEach(attributes, function (key, value) {
            elem.setAttribute(key, value);
          });
        });
        return this;
      },
      removeAttr: function (key) {
        var attributes = [];
        if (typeof key === 'object') {
          attributes = key;
        } else {
          attributes.push(key);
        }
        this.forEach(function (elem) {
          fn.each(attributes, function (key) {
            elem.removeAttribute(key);
          });
        });
        return this;
      },
      hasAttr: function (key) {
        if (!this.elements[0]) {
          return false;
        }
        return this.elements[0].hasAttribute(key);
      },
      attr: function (key, value) {
        if (
          typeof value !== 'undefined' ||
          typeof key === 'object'
        ) {
          this.setAttr(key, value);
          return this;
        }
        return this.getAttr(key);
      },

      val: function (value) {
        var result;
        if (this.elements[0] &&
          this.elements[0].tagName === 'SELECT' &&
          this.elements[0].multiple
        ) {
          if (typeof value !== 'undefined') {
            if (typeof value === 'string') {
              value = value.split(' ');
            }
            this.findChild('option').forEach(function (elem) {
              if (fn.contains(value, elem.value)) {
                elem.selected = true;
              } else {
                elem.selected = false;
              }
            });
            return this;
          } else {
            result = [];
            this.findChild('option').forEach(function (elem) {
              if (elem.selected) {
                result.push(elem.value);
              }
            });
            return result.length > 0 ? result : null;
          }
        }

        if (this.elements[0] &&
          this.elements[0].tagName === 'INPUT' &&
          this.elements[0].type === 'radio') {
          if (typeof value !== 'undefined') {
            this.forEach(function (elem) {
              if (elem.value === value) {
                elem.checked = true;
              } else {
                elem.checked = false;
              }
            });
            return this;
          } else {
            result = null;
            this.forEach(function (elem) {
              if (elem.checked) {
                result = elem.value;
              }
            });
            return result;
          }
        }

        if (this.elements[0] &&
          this.elements[0].tagName === 'INPUT' &&
          this.elements[0].type === 'checkbox') {
          if (typeof value !== 'undefined') {
            if (typeof value === 'string') {
              value = value.split(' ');
            }
            this.forEach(function (elem) {
              if (fn.contains(value, elem.value)) {
                elem.checked = true;
              } else {
                elem.checked = false;
              }
            });
            return this;
          } else {
            result = [];
            this.forEach(function (elem) {
              if (elem.checked) {
                result.push(elem.value);
              }
            });
            return result.length > 0 ? result : null;
          }
        }

        if (typeof this.prop('value') !== 'undefined') {
          return this.prop('value', value);
        }
        return this.attr('value', value);
      },

      addClass: function (classes) {
        if (typeof classes === 'string') {
          classes = classes.split(/\s+/);
        }

        this.forEach(function (elem) {
          var elemClasses = fn.getClasses(elem);
          fn.each(classes, function (className) {
            if (elemClasses.indexOf(className) === -1) {
              elemClasses.push(className);
            }
          });
          fn.saveClasses(elem, elemClasses);
        });
        return this;
      },
      removeClass: function (classes) {
        if (typeof classes === 'string') {
          classes = classes.split(/\s+/);
        }

        this.forEach(function (elem) {
          var elemClasses = fn.getClasses(elem);
          fn.each(classes, function (className) {
            var index = elemClasses.indexOf(className);
            if (index !== -1) {
              elemClasses.splice(index, 1);
            }
          });
          fn.saveClasses(elem, elemClasses);
        });
        return this;
      },
      hasClass: function (className) {
        if (!this.elements[0]) {
          return false;
        }
        return fn.contains(fn.getClasses(this.elements[0]), className);
      },
      toggleClass: function (className) {
        if (this.hasClass(className)) {
          this.removeClass(className);
        } else {
          this.addClass(className);
        }
        return this;
      },

      addStyle: function (style, styleValue) {
        this.forEach(function (elem) {
          var styles = fn.getStyles(elem);
          if (typeof styleValue !== 'undefined') {
            styles[style] = styleValue;
          } else if (typeof style === 'object') {
            fn.objEach(style, function (styleName, styleValue) {
              styles[styleName] = styleValue;
            });
          }
          fn.saveStyles(elem, styles);
        });
        return this;
      },
      removeStyle: function (style) {
        if (typeof style === 'string') {
          style = [style];
        }
        this.forEach(function (elem) {
          var styles = fn.getStyles(elem);
          fn.each(style, function (styleItem) {
            delete styles[styleItem];
          });
          fn.saveStyles(elem, styles);
        });
        return this;
      },
      css: function (style, styleValue) {
        return this.addStyle(style, styleValue);
      },

      html: function (html) {
        if (typeof html !== 'undefined') {
          this
            .empty()
            .forEach(function (elem) {
              elem.innerHTML = html;
            });
          return this;
        }
        if (!this.elements[0]) {
          return undefined;
        }
        return this.elements[0].innerHTML;
      },
      empty: function () {
        this.forEach(function (elem) {
          while (elem.firstChild) {
            elem.removeChild(elem.firstChild);
          }
        });
        return this;
      },

      append: function (elem) {
        if (!this.elements[0] || !elem) {
          return this;
        }
        if (elem.toString() === '[SweetyElement]') {
          fn.each(elem.elements, function (item) {
            this.elements[0].appendChild(item);
          }.bind(this));
        } else {
          this.elements[0].appendChild(elem);
        }
        return this;
      },
      remove: function () {
        this.forEach(function (elem) {
          elem.parentNode.removeChild(elem);
        });
        this.elements = [];
      },

      on: function (events, cb) {
        if (typeof events === 'string') {
          events = events.split(' ');
        }
        fn.each(events, function (eventName) {
          this.forEach(function (elem) {
            elem.addEventListener(eventName, cb, false);
            elem.sweetyEvents = elem.sweetyEvents || {};
            elem.sweetyEvents[eventName] =
              elem.sweetyEvents[eventName] || [];
            elem.sweetyEvents[eventName].push(cb);
          });
        }.bind(this));
        return this;
      },
      off: function (events, cb) {
        if (typeof events === 'string') {
          events = events.split(' ');
        }
        fn.each(events, function (eventName) {
          this.forEach(function (elem) {
            if (cb) {
              elem.removeEventListener(eventName, cb, false);
            } else if (
              elem.sweetyEvents &&
              elem.sweetyEvents[eventName]
            ) {
              elem.sweetyEvents[eventName].forEach(function (cb) {
                elem.removeEventListener(eventName, cb, false);
              });
              elem.sweetyEvents[eventName] = [];
            }
          });
        }.bind(this));
        return this;
      },

      exists: function () {
        if (this.elements.length === 0) {
          return false;
        }
        return true;
      },
      toString: function () {
        return '[SweetyElement]';
      }

    };

    fn.each(arguments, function (extension) {
      if (typeof extension === 'object') {
        fn.objEach(extension, function (name, func) {
          if (typeof func !== 'function') {
            return;
          }
          SweetyElement.prototype[name] = func;
        });
      }
    });

    return sweety;
  }

  var aeWidget = {
    params: {},
    open: function (widget_key, handler) {
      console.log('Open widget');

      aeWidget.params['hall_id'] = 0;
      aeWidget.params['photosession_id'] = 0;
      aeWidget.params['order_type'] = '';

      if (handler) {
        aeWidget.params['hall_id'] = handler.attr('hall_id') || 0;
        aeWidget.params['photosession_id'] = handler.attr('photosession_id') || 0;
        aeWidget.params['order_type'] = handler.attr('order_type') || '';
      }
      console.log(aeWidget.params);
      aeWidgetIframe = doc.createElement("div");
      aeWidgetIframe.className = 'aeWidgetIFrameDIV';

      var iframe = doc.createElement("iframe");
      iframe.className = 'aeWidgetIFrame';

      iframe.src = url + "/widget?widget_key=" + widget_key + '&' + encodeData(aeWidget.params);

      aeWidgetIframe.appendChild(iframe);
      doc.body.appendChild(aeWidgetIframe);
      $('body').addClass('aeWidgetParentActive');
    }
  };

  var $ = Sweety();
  var AE_DEV = false;
  var c = parseQueryString(cur_script.src.replace(/^[^\?]+\??/, ""));

  aeWidget.params = c;

  var url = "https://appevent.ru";
  if (c.url) {
    url = c.url;
  }
  var type = 'undefined' != typeof c.type ? c.type : '';

  // var css = doc.createElement("link");
  // css.type = "text/css";
  // css.href = url + (
  //   AE_DEV ? '/widgets/widget_front.css' :
  //   '/widgets/widget_front.min.css'
  // );
  // css.rel = "stylesheet";
  // doc.body.appendChild(css);

  $('.aeWidgetBtn')
    .attr('href', `${url}/widget/landing?widget_key=${WIDGET_KEY}`)
    .on('click', function (evt) {
      evt.preventDefault();
      aeWidget.open(WIDGET_KEY);
      $('body').css('overflow', 'hidden');
    });
  // if ('undefined' === typeof c.silent) {
  //   var btn = type == 'landing' ?
  //     $("<a class='aeWidgetBtn' href='" + url + "/widget/landing?widget_key=" + c.widget_key + "' target='_blank'></a>") :
  //     $("<div class='aeWidgetBtn'></div>");
  //   btn.append($('<div class="aeWidgetBtn-Wave"></div>'));

  //   var widgetIconAnimation = function () {
  //     var rotate_class = "aeWidgetBtn-rotate-icon",
  //       icon_timer,
  //       icons = {},
  //       first_icon,
  //       started = false,
  //       init = function () {
  //         var list = [{
  //             name: 'book',
  //             text: 'БРОНЬ<br/>ОНЛАЙН',
  //             duration: 3000
  //           },
  //           {
  //             name: 'logo',
  //             text: '',
  //             duration: 3000
  //           }
  //         ];

  //         list.forEach(function (icon, index, list) {
  //           var element = $("<div></div>");
  //           element.addClass('aeWidgetBtn-icon aeWidgetBtn-icon_' + icon.name);
  //           element.html(icon.text);
  //           btn.append(element);

  //           first_icon || (first_icon = icon.name),
  //             icons[icon.name] = {
  //               element: element,
  //               next: list[(index + 1) % list.length].name,
  //               duration: icon.duration
  //             };
  //         });
  //         startTimers();
  //       },
  //       startTimers = function () {
  //         started = true;

  //         var iconTick = function (icon) {
  //           $('.aeWidgetBtn').findChild('.aeWidgetBtn-icon').removeClass(rotate_class);
  //           icons[icon].element.addClass(rotate_class),
  //             function (icon) {
  //               icon_timer = setTimeout(function () {
  //                 started && (icons[icon].element.removeClass(rotate_class), iconTick(icons[icon].next))
  //               }, icons[icon].duration)
  //             }(icon);
  //         };
  //         iconTick(first_icon)
  //       },
  //       reset = function () {
  //         clearTimeout(icon_timer);
  //         setTimeout(function () {
  //           started || startTimers()
  //         }, 30);
  //       },
  //       stop = function () {
  //         started = false;
  //         clearTimeout(icon_timer);
  //         $('.aeWidgetBtn').findChild('.aeWidgetBtn-icon').removeClass(rotate_class);
  //       };

  //     return {
  //       init: init,
  //       reset: reset,
  //       stop: stop
  //     }
  //   }();

  //   btn
  //     .on("mouseover", function () {
  //       widgetIconAnimation.stop()
  //     })
  //     .on("mouseleave", function () {
  //       widgetIconAnimation.reset()
  //     });

  //   widgetIconAnimation.init();

  //   if (type != 'landing') {
  //     btn.on('click', function () {
  //       aeWidget.open(c.widget_key);
  //     });
  //   }
  // }

  $('.aeWidgetOpen').on('click', function () {
    aeWidget.open($(this).attr('widget_key'), $(this));
  });

  window.onmessage = function (event) {
    if (event.data === "close_ae_widget") {
      console.log('Close widget');
      aeWidgetIframe.remove();

      $('body').removeClass('aeWidgetParentActive')
        .css('overflow', 'auto');
    }
  };

  // $(doc.body).append(btn);
}(window, window.document, window.location, function () {
  return window.document.currentScript || function () {
    var a = window.document.getElementById("aeWidgetScript");
    if (a) {
      return a;
    } else {
      var a = window.document.getElementsByTagName("script");
      return a[a.length - 1];
    }
  }()
}());