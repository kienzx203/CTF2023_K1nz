# **Cookie-arena-CTF-seaaon-2**

| Challenge     | FLAG|
| ----------- | ----------- |
| [**Be Positive**](#be-positive)      | `CHH{BE_cAr3fUL_WitH_NE6ATIV3_NumBeR_3e87da18c5f0302fa2c467a9d5cd18f7}`      |
| [**Magic Login**](#magic-login)  | `CHH{PHP_m4g1c_tr1ck_0lD_but_g0lD_8f9e3b92113749568a033b1a5fb20a4e}`        |
| [**Youtube Downloader**](#youtube-downloader)  | `CHH{Ea5y_cOmmaND_inj3c7Ion_2916ac0127955a1d9953fb2cc712d33d}`        |
| [**Pass Code**](#web-1)  |`CHH{jAvAscRIP7_o8FuSCaTe_5e5d74922ec4bbd00af6023b6eb3b0c8}`        |
| [**Magic Login Harder**](#magic-login-harder)  | `CHH{7yPE_jU66lin9_hArdEr_df929768446acbfd50193567fa46ecdc}`        |
| [**Slow Down**](#slow-down)  | `CHH{PHP.................................}`        |
| [**Suck it**](#suck-it)  | `CHH{H4ve_y0u_re4d_th3_m3ssage_52884b3980fe5f6a2b5e93d9f9ee0de7}`        |

![](./img_cookie/Screenshot%202023-07-11%20175346.png)

## **Be Positive**

- Ở trang web này chúng ta có chức năng chuyển tiền giữa 2 người dùng `alice` và `bob` nhưng để tìm mua được flag thì tài khoản cần đền `3100$`. Hiện tại mỗi tài khoản alice và bob mỗi người có `1500$`. Câu hỏi đặt ra vậy làm sao mình kiếm thêm `1$` nữa.

![](./img_cookie/Screenshot%202023-07-10%20215554.png)

![](./img_cookie/Screenshot%202023-07-10%20220151.png)

- Sau khi gửi `1500$` của bob cho alice. Vì do sự xử lý lỗi phía trang web cho phép gửi tiền với `-1$` chính vì thế số dư của bob sẽ được tăng thêm `1$`

![](./img_cookie/Screenshot%202023-07-10%20220719.png)

![](./img_cookie/Screenshot%202023-07-10%20220749.png)

- Vậy chúng ta đã đủ `3100$` để mua flag: `CHH{BE_cAr3fUL_WitH_NE6ATIV3_NumBeR_3e87da18c5f0302fa2c467a9d5cd18f7}`

## **Magic Login**

- Sau khi quan sát source trang web chúng ta có được source code PHP như sau:

```php

if(isset($_POST['submit'])){ 
    $usr = mysql_real_escape_string($_POST['username']); 
    $pas = hash('sha256', mysql_real_escape_string($_POST['password'])); 
    
    if($pas == "0"){ 
        $_SESSION['logged'] = TRUE; 
        header("Location: upload.php"); // Modify to go to the page you would like 
        exit; 
    }else{ 
        header("Location: login_page.php"); 
        exit; 
    } 
}else{    //If the form button wasn't submitted go to the index page, or login page 
    header("Location: login_page.php");     
    exit; 
} 

```

- Ở đây chúng ta làm sao để bypass được `$pas == "0"`

- Sau khi tôi suy nghĩ và keyword để tôi tìm kiếm là `php variable comparison exploit` thì tôi đã tìm được cách bypass sau khi đọc một slide nói về vấn đề này: [**php variable comparison exploit**](https://owasp.org/www-pdf-archive/PHPMagicTricks-TypeJuggling.pdf)

- `For SHA-256(34250003024812) 0e46289032038065916139621039085883773413820991920706299695051332 == "0"`

- Từ đấy, với chuỗi `34250003024812` chúng ta có thể bypass thành công.

![](./img_cookie/Screenshot%202023-07-10%20224806.png)

- Sau khi đăng nhập thành công chúng ta có thể sử dụng chức năng upload file. Vì trang web không bảo mật tối việc uploadfile. Nên chúng ta có thể uploadfile php và RCE được trang web và lấy được flag.

## **Youtube Downloader**

- Sau khi tôi sử dụng chức năng tôi nghĩ ở đây chúng ta có khả năng tấn công command injection:

![](./img_cookie/Screenshot%202023-07-10%20230551.png)

![](./img_cookie/Screenshot%202023-07-10%20231106.png)

- Từ đấy, chúng ta có thể RCE để biết được thông tin flag nằm ở đâu.

## **Magic Login Harder**

- Ở đây challenges đã cung cấp chúng ta source để chúng ta biết việc sử lý đăng nhập như sau:

```php
<?php
    if(isset($_POST["submit"])){
        $username = base64_decode($_POST['username']);
        $password = base64_decode($_POST['password']);

        if(($username == $password)){
            echo 'Username and password are not the same';
        }
        else if((md5($username)===md5($password))){
            $_SESSION['username'] = $username;
            header('Location: admin.php?file=1.txt');
        } else {
            echo 'Username and password are wrong';
        }
    }
?>
```

- Ở đây chúng ta đã biết rằng để bypass được việc đăng nhập chúng ta cần md5 giống nhau. Chúng ta sẽ đi nghiên cứu về `Crypto_MD5_Collision`.

- Tôi đã nghiên cứu một tài liệu như sau để hiểu rõ về cách tấn công này : [**Crypto_MD5_Collision**](https://seedsecuritylabs.org/Labs_16.04/PDF/Crypto_MD5_Collision.pdf)

- Tôi đã sử dụng tool `md5collgen` để thực hiện phân tách 2 file bin khác nhau nhưng khi md5 chúng ta nhận được một mã giống nhau.

- Tôi tạo một file md5.txt như sau:

![](./img_cookie/Screenshot%202023-07-10%20233938.png)

- Thực hiện phân tách file:

![](./img_cookie/Screenshot%202023-07-10%20234125.png)

![](./img_cookie/Screenshot%202023-07-10%20235110.png)

- Từ đấy, sau khi đăng nhập thành công chúng ta đã đến được /`admin.php` và ở đây có một lỗ hổng lfi.

![](./img_cookie/Screenshot%202023-07-10%20235952.png)

- Từ đấy, tôi có thể đọc được với file `/tmp/sess_` + với session cookie của mình.

![](./img_cookie/Screenshot%202023-07-11%20000404.png)

- Và chúng ta có thể thực hiện thành công RCE.

![](./img_cookie/Screenshot%202023-07-11%20000457.png)

## **Pass Code**

- Ở challenges này chúng ta biết ở đây là `js Obfuscate`. Vậy để hiểu đoạn code này chúng ta phải thực hiện reverse lại bằng công cụ [**JS nice**](http://jsnice.org/). Và kèm theo đó thực hiện debug trên webtool.

![](./img_cookie/Screenshot%202023-07-11%20003342.png)

- Sau khi làm sạch code và ta được code js như sau:

```javascript
'use strict';
/**
 * @param {?} a
 * @param {number} fn
 * @return {?}
 */
function _0x50c7(a, fn) {
  var bouncy_terrain_verts = _0x55ef();
  return _0x50c7 = function(i, fn) {
    /** @type {number} */
    i = i - (7661 + 1 * -4099 + 1119 * -3);
    var b = bouncy_terrain_verts[i];
    if (_0x50c7["dmaofR"] === undefined) {
      /**
       * @param {!Object} fn
       * @return {?}
       */
      var testcase = function(fn) {
        /** @type {string} */
        var listeners = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=";
        /** @type {string} */
        var PL$13 = "";
        /** @type {string} */
        var escapedString = "";
        /** @type {string} */
        var data = PL$13 + testcase;
        /** @type {number} */
        var bc = 2 * -2501 + 278 * 11 + 648 * 3;
        var bs;
        var buffer;
        /** @type {number} */
        var i = 7 * -283 + 621 * 11 + -4850;
        for (; buffer = fn["charAt"](i++); ~buffer && (bs = bc % (-4778 * -1 + 8093 + -12867) ? bs * (7366 * -1 + -2650 + -224 * -45) + buffer : buffer, bc++ % (1 * 5351 + 2745 + -8092)) ? PL$13 = PL$13 + (data["charCodeAt"](i + (-3792 + 4501 + 699 * -1)) - (4 * -1621 + -8314 + 1234 * 12) !== -1 * 3163 + -1 * 9358 + 1 * 12521 ? String["fromCharCode"](-1 * -9733 + -7083 + -5 * 479 & bs >> (-(-152 * 6 + -1638 + -638 * -4) * bc & 5920 + 1 * -7634 + -10 * -172)) : bc) : 1814 * -2 + -32 * -22 + 2924) {
          buffer = listeners["indexOf"](buffer);
        }
        /** @type {number} */
        var PL$19 = 1299 * 5 + 8 * -769 + 1 * -343;
        var PL$15 = PL$13["length"];
        for (; PL$19 < PL$15; PL$19++) {
          /** @type {string} */
          escapedString = escapedString + ("%" + ("00" + PL$13["charCodeAt"](PL$19)["toString"](-4 * -1157 + -1427 * -1 + -9 * 671))["slice"](-(-3718 + 89 * 1 + 3631)));
        }
        return decodeURIComponent(escapedString);
      };
      /** @type {function(!Object): ?} */
      _0x50c7["wDBSLi"] = testcase;
      /** @type {!Arguments} */
      a = arguments;
      /** @type {boolean} */
      _0x50c7["dmaofR"] = !![];
    }
    var alen = bouncy_terrain_verts[-8230 + -9968 + 18198];
    var j = i + alen;
    var b2 = a[j];
    if (!b2) {
      /**
       * @param {?} deny
       * @return {undefined}
       */
      var WMCacheControl = function(deny) {
        this["DytWPB"] = deny;
        /** @type {!Array} */
        this["YhilVC"] = [-3 * -1379 + 5431 * -1 + -5 * -259, -1343 * 1 + 3173 + -1830, -1 * -6883 + -2762 * 3 + 1403];
        /**
         * @return {?}
         */
        this["kTMFMM"] = function() {
          return "newState";
        };
        /** @type {string} */
        this["nlZNXH"] = "\\w+ *\\(\\) *{\\w+ *";
        /** @type {string} */
        this["nDTZzB"] = "['|\"].+['|\"];? *}";
      };
      /**
       * @return {?}
       */
      WMCacheControl["prototype"]["uyeFQe"] = function() {
        /** @type {!RegExp} */
        var test = new RegExp(this["nlZNXH"] + this["nDTZzB"]);
        /** @type {number} */
        var artistTrack = test["test"](this["kTMFMM"]["toString"]()) ? --this["YhilVC"][-3147 + -61 * 1 + -3209 * -1] : --this["YhilVC"][-9619 + 7462 * 1 + 2157];
        return this["hfzizQ"](artistTrack);
      };
      /**
       * @param {?} canCreateDiscussions
       * @return {?}
       */
      WMCacheControl["prototype"]["hfzizQ"] = function(canCreateDiscussions) {
        if (!Boolean(~canCreateDiscussions)) {
          return canCreateDiscussions;
        }
        return this["pQDVJK"](this["DytWPB"]);
      };
      /**
       * @param {?} saveNotifs
       * @return {?}
       */
      WMCacheControl["prototype"]["pQDVJK"] = function(saveNotifs) {
        /** @type {number} */
        var fp = 246 * -10 + -9316 + 11776;
        var len = this["YhilVC"]["length"];
        for (; fp < len; fp++) {
          this["YhilVC"]["push"](Math["round"](Math["random"]()));
          len = this["YhilVC"]["length"];
        }
        return saveNotifs(this["YhilVC"][45 * 5 + -1 * 4987 + -2 * -2381]);
      };
      (new WMCacheControl(_0x50c7))["uyeFQe"]();
      b = _0x50c7["wDBSLi"](b);
      a[j] = b;
    } else {
      b = b2;
    }
    return b;
  }, _0x50c7(a, fn);
}
/**
 * @return {?}
 */
function _0x55ef() {
  /** @type {!Array} */
  var _0x4385a8 = ["Aog6Pw0GC+g7R2e", "zw5J", "kcGOlISPkYKRkq", "zM9YrwfJAa", "mti4nZK4AMvfBefN", "quvt", "CMvTB3zLqxr0CG", "mJqXmZq2oeLMwxrjsq", "mteXmtuXv0j1zMXp", "zgvJCNLWDa", "y29UC3rYDwn0BW", "z2v0qxr0CMLIDq", "ugDTsue", "v3vkzMq", "tw5hAgy", "DhnTEMe", "mJfksNrhAKK", "nZq3nJy0AKTRyxDT", "EMfhzLi", "zvvVr2C", "BwfW", "C2vHCMnO", "Agr0Eei", "vhDkwMW", "zNjVBq", "CxvLCNLtzwXLyW", "ySoHBMGGCxv5igm", "Dg9YqwXS", "mta4mdC2mdvgB0fyCMu", "sfz0yNK", "we5zyxa", "i2nOyxb0zxiTyW", "mJe4mZuZogryvw9tBa", 
  "B250zw50igLTzW", "vxrMoa", "yZaWA2LLlwfYmW", "yxbWBhK", "nK1JEujJAW", "Dg9tDhjPBMC", "mJuXmdm0nuPYywr0DW", "re1erhq", "Awj1Dgu", "DM1lr1a", "zw5JCNLWDgvKlq"];
  /**
   * @return {?}
   */
  _0x55ef = function() {
    return _0x4385a8;
  };
  return _0x55ef();
}
(function(groupingFunction, val) {
  /**
   * @param {number} dropTargetOptions
   * @param {number} draggableOptions
   * @param {number} date
   * @param {number} callback
   * @return {?}
   */
  function setup(dropTargetOptions, draggableOptions, date, callback) {
    return _0x50c7(draggableOptions - 131, callback);
  }
  /**
   * @param {number} uri
   * @param {number} data
   * @param {number} index
   * @param {number} prop
   * @return {?}
   */
  function getData(uri, data, index, prop) {
    return _0x50c7(data - -419, index);
  }
  var data = groupingFunction();
  for (; !![];) {
    try {
      /** @type {number} */
      var nodeval = -parseInt(setup(355, 357, 372, 352)) / (8598 + -4489 * -1 + -13086) + parseInt(getData(-188, -197, -195, -191)) / (5997 + -2430 + -3565) * (-parseInt(setup(347, 365, 345, 347)) / (29 * -181 + 882 * -7 + 11426)) + parseInt(getData(-174, -194, -191, -185)) / (-1 * -9326 + 1556 + -222 * 49) + -parseInt(setup(326, 344, 354, 338)) / (5976 + 223 * 37 + -1 * 14222) + -parseInt(setup(333, 342, 358, 349)) / (7118 + 451 * 15 + -13877) * (parseInt(setup(331, 337, 350, 327)) / (-6127 + -14 * 
      -438 + 2)) + -parseInt(getData(-177, -184, -178, -206)) / (-3 * 1878 + -8723 + 2873 * 5) + parseInt(setup(399, 377, 373, 373)) / (-8138 + -3613 + 784 * 15);
      if (nodeval === val) {
        break;
      } else {
        data["push"](data["shift"]());
      }
    } catch (_0x436618) {
      data["push"](data["shift"]());
    }
  }
})(_0x55ef, -618856 + 82182 + 67037 * 13), async function init() {
  /**
   * @param {number} data
   * @param {number} opData
   * @param {number} callback
   * @param {number} key
   * @return {?}
   */
  function apply(data, opData, callback, key) {
    return _0x50c7(data - 625, key);
  }
  /**
   * @param {?} key
   * @param {?} value
   * @return {?}
   */
  function init(key, value) {
    /**
     * @param {number} deps
     * @param {number} i
     * @param {number} size
     * @param {number} key
     * @return {?}
     */
    function fn(deps, i, size, key) {
      return get(key, i - 146, size - 252, size - -474);
    }
    /**
     * @param {number} dependency
     * @param {number} i
     * @param {number} control
     * @param {number} id
     * @return {?}
     */
    function get(dependency, i, control, id) {
      return get(id, i - 6, control - 464, control - -161);
    }
    if (properties["XIkzW"](properties[get(926, 918, 908, 897)], properties[fn(623, 589, 602, 606)])) {
      /** @type {!Function} */
      var _0x2c3e6f = _0x4004c5 ? function() {
        /**
         * @param {number} url
         * @param {number} code
         * @param {number} fn
         * @param {number} errorCode
         * @return {?}
         */
        function throwException(url, code, fn, errorCode) {
          return get(url - 444, code - 308, fn - -931, code);
        }
        if (_0x23acf2) {
          var cssobj = _0x230dff[throwException(-66, -36, -53, -46)](_0x4f44af, arguments);
          return _0x597eff = null, cssobj;
        }
      } : function() {
      };
      return _0x3eebc4 = ![], _0x2c3e6f;
    } else {
      var nonce = CryptoJS[get(883, 868, 887, 905)]["Utf8"]["parse"](properties["Gmpce"](value, properties[get(894, 894, 884, 885)]));
      var result = CryptoJS["AES"][fn(565, 599, 582, 579)](key, nonce, {
        "iv" : nonce
      });
      return result[fn(552, 584, 567, 548)](CryptoJS[get(869, 890, 887, 893)][get(894, 886, 876, 872)]);
    }
  }
  /**
   * @param {number} prop
   * @param {number} view
   * @param {number} layer
   * @param {number} data
   * @return {?}
   */
  function get(prop, view, layer, data) {
    return _0x50c7(data - 829, prop);
  }
  var properties = {
    "MnGhf" : apply(855, 845, 837, 851),
    "WuJfd" : apply(845, 830, 834, 842) + "+$",
    "XIkzW" : function(name, initialValue) {
      return name === initialValue;
    },
    "hdtxB" : "UQELD",
    "HVtby" : apply(839, 832, 856, 819),
    "Gmpce" : function(beforeZero, afterZero) {
      return beforeZero || afterZero;
    },
    "vmKGP" : get(1044, 1033, 1042, 1038) + "na-ctf",
    "PNJnP" : function(require, load, callback) {
      return require(load, callback);
    },
    "tsmza" : function(saveNotifs) {
      return saveNotifs();
    },
    "XNYap" : get(1051, 1056, 1045, 1034) + get(1035, 1024, 1033, 1036)
  };
  var value = function() {
    /**
     * @param {number} url
     * @param {number} params
     * @param {number} searchText
     * @param {number} callback
     * @return {?}
     */
    function get(url, params, searchText, callback) {
      return get(params, params - 147, searchText - 44, searchText - -83);
    }
    /**
     * @param {number} txt
     * @param {number} cursor
     * @param {number} node
     * @param {number} struc_store
     * @return {?}
     */
    function parse(txt, cursor, node, struc_store) {
      return apply(cursor - -1441, cursor - 267, node - 1, node);
    }
    var json = {};
    /**
     * @param {?} x_or_y
     * @param {?} y
     * @return {?}
     */
    json[get(998, 973, 983, 1E3)] = function(x_or_y, y) {
      return x_or_y === y;
    };
    json["zaGfR"] = properties[get(971, 975, 978, 996)];
    /** @type {string} */
    json["TwJZl"] = "KrqBM";
    var next = json;
    /** @type {boolean} */
    var y$$ = !![];
    return function(value, context) {
      /**
       * @param {number} params
       * @param {number} key
       * @param {number} layer
       * @param {number} data
       * @return {?}
       */
      function get(params, key, layer, data) {
        return parse(params - 143, data - 94, key, data - 332);
      }
      /**
       * @param {number} from
       * @param {number} id
       * @param {number} types
       * @param {number} fields
       * @return {?}
       */
      function getType(from, id, types, fields) {
        return get(from - 29, id, from - -261, fields - 246);
      }
      if (next["eUoGg"](next[get(-469, -464, -479, -486)], next[getType(726, 709, 735, 719)])) {
        var cssobj = _0x46e645["apply"](_0x47201f, arguments);
        return _0x2b5775 = null, cssobj;
      } else {
        /** @type {!Function} */
        var voronoi = y$$ ? function() {
          /**
           * @param {number} c
           * @param {number} data
           * @param {number} context
           * @param {number} layer
           * @return {?}
           */
          function exports(c, data, context, layer) {
            return get(c - 372, layer, context - 63, context - 1481);
          }
          if (context) {
            var string = context[exports(977, 950, 969, 977)](value, arguments);
            return context = null, string;
          }
        } : function() {
        };
        return y$$ = ![], voronoi;
      }
    };
  }();
  var query = properties["PNJnP"](value, this, function() {
    /**
     * @param {number} length
     * @param {number} cursor
     * @param {number} key
     * @param {number} cachePolicy
     * @return {?}
     */
    function get(length, cursor, key, cachePolicy) {
      return apply(cursor - -808, cursor - 435, key - 330, key);
    }
    /**
     * @param {number} payload
     * @param {number} delay
     * @param {number} force
     * @param {number} callback
     * @return {?}
     */
    function update(payload, delay, force, callback) {
      return apply(callback - -1114, delay - 133, force - 497, payload);
    }
    return query[get(22, 29, 19, 24)]()["search"](properties["WuJfd"])[update(-259, -277, -255, -277)]()[get(40, 45, 51, 27) + "r"](query)[update(-269, -268, -240, -250)](properties[get(67, 48, 36, 37)]);
  });
  properties[get(1056, 1043, 1045, 1062)](query);
  const base = properties[get(1063, 1059, 1061, 1077)];
  var hash = document[get(1071, 1071, 1058, 1072) + apply(870, 886, 890, 875)](base);
  hash = Array[get(1078, 1062, 1092, 1071)](hash);
  var data = hash[get(1070, 1057, 1049, 1067)]((express) => {
    return express[apply(854, 875, 836, 858) + "te"](get(1061, 1064, 1025, 1046) + "src");
  });
  data = data[get(1075, 1085, 1070, 1067)]((val) => {
    return CryptoJS[get(1040, 1044, 1031, 1052)][get(1068, 1040, 1051, 1056)](val, apply(869, 862, 851, 852) + apply(843, 845, 850, 865))["toString"](CryptoJS[apply(844, 855, 822, 822)]["Utf8"]);
  });
  hash[apply(846, 827, 850, 838)]((elem, style) => {
    return elem[get(1063, 1044, 1039, 1053) + apply(840, 833, 861, 846)](get(1030, 1037, 1033, 1046) + "src"), elem["setAttribu" + "te"]("src", data[style]);
  });
}();
```

- Tôi vừa debug thêm sau khi làm sạch code và được code như sau:

```javascript
;(async function main() {
  var _0x24b3ab = (function () {
      var _0x140877 = true
      return function (_0x36bc46, _0x3c9734) {
        var _0x54cdd4 = _0x140877
          ? function () {
              if (_0x3c9734) {
                var _0x505e3b = _0x3c9734.apply(_0x36bc46, arguments)
                return (_0x3c9734 = null), _0x505e3b
              }
            }
          : function () {}
        return (_0x140877 = false), _0x54cdd4
      }
    })(),
    _0x34b2c2 = _0x24b3ab(this, function () {
      return _0x34b2c2
        .toString()
        .search('(((.+)+)+)+$')
        .toString()
        .constructor(_0x34b2c2)
        .search('(((.+)+)+)+$')
    })
  _0x34b2c2()
  function _0x2e3fc4(_0x230fda, _0x10a57a) {
    var _0x3c12b2 = CryptoJS.enc.Utf8.parse(_0x10a57a || 'c00kie-ar3na-ctf'),
      _0x329fea = CryptoJS.AES.decrypt(_0x230fda, _0x3c12b2, { iv: _0x3c12b2 })
    return _0x329fea.toString(CryptoJS.enc.Utf8)
  }
  const _0x5f2a9b = '#chapter-content img'
  var _0x5df765 = document.querySelectorAll(_0x5f2a9b)
  _0x5df765 = Array.from(_0x5df765)
  var _0x46d3cf = _0x5df765.map((_0x2ffa3f) =>
    _0x2ffa3f.getAttribute('encrypted-src')
  )
  _0x46d3cf = _0x46d3cf.map((_0x294fdc) =>
    CryptoJS.AES.decrypt(_0x294fdc, 'bánh quy chấm sữa').toString(
      CryptoJS.enc.Utf8
    )
  )
  _0x5df765.forEach(
    (_0x3ae067, _0x18596f) => (
      _0x3ae067.removeAttribute('encrypted-src'),
      _0x3ae067.setAttribute('src', _0x46d3cf[_0x18596f])
    )
  )
})()
```

- Từ đấy ta biết được secretkey `bánh quy chấm sữa` và thực hiện lấy flag: `CHH{jAvAscRIP7_o8FuSCaTe_5e5d74922ec4bbd00af6023b6eb3b0c8}`

![](./img_cookie/Screenshot%202023-07-11%20101040.png)

## **Slow Down**

- `Phương pháp 1: Race Conditions`
  - Bài này tương tự với bài Be Positive, tuy nhiên filter của parameter amount đã chặt chẽ hơn, nên hướng pollute các parameter không khả thi.

  - Mình nghĩ đến việc tấn công bằng race condition, solution của mình là login 1 acc tại 2 trình duyệt khác nhau (lúc này mỗi trình duyệt có 1 cookie khác nhau), sau đó cả 2 trình duyệt cùng transfer tiền đến tài khoản còn lại. Lúc này tài khoản chuyển bị trừ 1, nhưng tài khoản nhận sẽ nhận được 2, và mình có thể mua flag.

![](./img_cookie/Screenshot%202023-07-11%20102051.png)

- `Phương pháp 2: Bypass amount`
  - Hãy chú ý ảnh sau:
![](./img_cookie/Screenshot%202023-07-11%20102309.png)

  - Vậy tôi có thể bypass chuyển tiền như sau:

![](./img_cookie/Screenshot%202023-07-11%20102550.png)

## **Suck it**

- Sau khi đọc source code tôi đã thấy những điểm khai thác để lấy flag:

```javascript
case "nguoiyeucuaADMIN":
        if(socket.userID !== "ADMIN"){
          message.content="I do not associate with n.....on-Admin";
        }else{
          message.content="Đêm qua em tuyệt lắm: \n"+FLAG;
        }
        message.from = to;
        message.to = socket.userID
        socket.emit("private message", message);
        break;
      case "buctuong":
        break;
      default:
        socket.to(to).to(socket.userID).emit("private message", message);
        messageStore.saveMessage(message);
    }

  });

  // admin force any user to disconnect
  socket.on("force disconnect",async (userID,secretKey)=>{
    // check valid account
    if (secretKey !== "574a94b04f303f5663e833b883cd2b23"){
      socket.emit("This secret key is wrong.")
    }
    else{
    const targetSocket = await sessionStore.findSessionsByUserID(userID);
    const matchingSockets = await io.in(targetSocket.userID).allSockets();
    const isDisconnected = matchingSockets.size === 0;
    if (isDisconnected) {
      // notify other users
      socket.broadcast.emit("user disconnected", targetSocket.userID);
      // update the connection status of the session
      socket.emit(targetSocket.sessionID);
      sessionStore.saveSession(targetSocket.sessionID, {
        userID: targetSocket.userID,
        username:targetSocket.username,
        connected: false,
      });
    }};
  });

```

- Nhờ chức năng `update the connection status of the session` tôi có thể lấy session admin và nhắn tin với người yêu admin như sau: `CHH{H4ve_y0u_re4d_th3_m3ssage_52884b3980fe5f6a2b5e93d9f9ee0de7}`

![](./img_cookie/Screenshot%202023-07-11%20104603.png)

![](./img_cookie/Screenshot%202023-07-11%20104818.png)
