var crypto = require('crypto-js');

function o(t, n) {
    var e = undefined
                        t = this.words = t || [],
                        this.sigBytes = n != e ? n : 4 * t.length
                    }
function a(t) {
                        if (t instanceof ArrayBuffer && (t = new Uint8Array(t)),
                        (t instanceof Int8Array || "undefined" !== typeof Uint8ClampedArray && t instanceof Uint8ClampedArray || t instanceof Int16Array || t instanceof Uint16Array || t instanceof Int32Array || t instanceof Uint32Array || t instanceof Float32Array || t instanceof Float64Array) && (t = new Uint8Array(t.buffer,t.byteOffset,t.byteLength)),
                        t instanceof Uint8Array) {
                            for (var e = t.byteLength, n = [], r = 0; r < e; r++)
                                n[r >>> 2] |= t[r] << 24 - r % 4 * 8;
                            o.call(this, n, e)
                        } else
                            o.apply(this, arguments)
                    }

function s(t) {
                        for (var e = t.length, n = [], r = 0; r < e; r++)
                            n[r >>> 2] |= (255 & t.charCodeAt(r)) << 24 - r % 4 * 8;
                        return new a(n,e)
                    }
function parse(t) {
                        return s(unescape(encodeURIComponent(t)))
                    }

K = function() {
            var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "";
            return e.replace(/\s+/g, "")
        }

T = function(e) {
            var n = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
            if (e && "string" === typeof e) {
                var t = n.text || "0"
                  , a = n.length || 24;
                if (e.length < a)
                    for (var r = e.length; r < a; r++)
                        e += t;
                else
                    e = e.substring(0, a);
                return e
            }
        }

_ = function(e) {
            var n = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : ""
              , t = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {}
              , a = t.enc
              , r = void 0 === a ? "Utf8" : a
              , i = t.mode
              , o = void 0 === i ? "ECB" : i
              , c = t.padding
              , u = void 0 === c ? "Pkcs7" : c
              , d = crypto.enc[r].parse(n)
              , l = {
                mode: crypto.mode[o],
                padding: crypto.pad[u]
            }
              , s = crypto.TripleDES.encrypt(e, d, l);
            return s.toString()
        }

// 加密
function pwd(pwds,user){
    password = encodeURI(_(pwds, T(K(user))))
    return password
}


