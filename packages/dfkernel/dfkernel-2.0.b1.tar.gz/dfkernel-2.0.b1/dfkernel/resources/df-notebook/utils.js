// Copyright (c) Dataflow Notebook Development Team.
// Distributed under the terms of the BSD-3 License.

define(function() {
    "use strict";

    //String prototype from MDN
    //https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/startsWith
    if (!String.prototype.startsWith) {
        String.prototype.startsWith = function(search, pos) {
            return this.substr(!pos || pos < 0 ? 0 : +pos, search.length) === search;
        };
    }

    //String prototype from MDN
    //https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/repeat
    if (!String.prototype.repeat) {
      String.prototype.repeat = function(count) {
        'use strict';
        if (this == null) {
          throw new TypeError('can\'t convert ' + this + ' to object');
        }
        var str = '' + this;
        count = +count;
        if (count != count) {
          count = 0;
        }
        if (count < 0) {
          throw new RangeError('repeat count must be non-negative');
        }
        if (count == Infinity) {
          throw new RangeError('repeat count must be less than infinity');
        }
        count = Math.floor(count);
        if (str.length == 0 || count == 0) {
          return '';
        }
        // Ensuring count is a 31-bit integer allows us to heavily optimize the
        // main part. But anyway, most current (August 2014) browsers can't handle
        // strings 1 << 28 chars or longer, so:
        if (str.length * count >= 1 << 28) {
          throw new RangeError('repeat count must not overflow maximum string size');
        }
        var rpt = '';
        for (var i = 0; i < count; i++) {
          rpt += str;
        }
        return rpt;
      }
    }

    var pad_str_left = function(s, len, pad_char) {
        pad_char = (typeof pad_char !== 'undefined') ?  pad_char : "0";
        return (pad_char.repeat(len) + s).substr(-len);
    };

    var random_hex_str = function(len, start_letter) {
        var num;
        len = (typeof len !== 'undefined') ? len : 6;
        if (start_letter || (start_letter === undefined)) {
            var start_num = parseInt("a" + "0".repeat(len-1), 16);
             num = Math.floor(Math.random() *
                    (parseInt("f".repeat(len), 16) - start_num)) + start_num;
            // no need to pad
            return num.toString(16);
        } else {
            // generate value in [1, 0xf...f]
            num = Math.floor(Math.random() * parseInt("f".repeat(len), 16)) + 1;
            return pad_str_left(num.toString(16), len);
        }
    };

    var CODE_REGEX = /(^|[^A-Za-z0-9_])Out\[[\'\"]?([0-9a-f]+)[\'\"]?\]/g;

    var rewrite_code_ids = function(code, map) {
        // replace allows a function that passes parenthesized submatches
        return code.replace(CODE_REGEX, function(s, g1, g2) {
            if (g2 in map) {
                return g1 + "Out[" + map[g2] + "]";
            } else {
                return s;
            }
        });
    };

    return {
        pad_str_left: pad_str_left,
        random_hex_str: random_hex_str,
        rewrite_code_ids: rewrite_code_ids
    };
});
