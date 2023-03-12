function cv(e) {
    return function (e) {
        try {
            return btoa(e)
        } catch (t) {
            return Buffer.from(e).toString("base64")
        }
    }(encodeURIComponent(e).replace(/%([0-9A-F]{2})/g, (function (e, t) {
            return i("0x" + t)
        }
    )))
}

function i(e) {
    var t, a = (t = "",
        ["66", "72", "6f", "6d", "43", "68", "61", "72", "43", "6f", "64", "65"].forEach((function (e) {
                t += unescape("%u00" + e)
            }
        )),
        t);
    return String[a](e)
}

function oZ(e, t) {
    t || (t = s());
    for (var a = (e = e.split("")).length, n = t.length, o = "charCodeAt", r = 0; r < a; r++)
        e[r] = i(e[r][o](0) ^ t[(r + 10) % n][o](0));
    return e.join("")
}

function v(e, t, a) {
    var n, o, r = void 0 === a ? 2166136261 : a;
    for (n = 0,
             o = e.length; n < o; n++)
        r ^= e.charCodeAt(n),
            r += (r << 1) + (r << 4) + (r << 7) + (r << 8) + (r << 24);
    return t ? ("0000000" + (r >>> 0).toString(16)).substr(-16) : r >>> 0
}

function v(e, t, a) {
    var n, o, r = void 0 === a ? 2166136261 : a;
    for (n = 0,
             o = e.length; n < o; n++)
        r ^= e.charCodeAt(n),
            r += (r << 1) + (r << 4) + (r << 7) + (r << 8) + (r << 24);
    return t ? ("0000000" + (r >>> 0).toString(16)).substr(-16) : r >>> 0
}

var l = (0, v)("qimai|Technologyx", 1)

function get_aaa(url, params) {

    var baseURL = "https://api.qimai.cn",
        d = '@#',
        f = 652,
        h = 'analysis'
    var a, o = +new Date - (f || 0) - 1515125653845, r = [];
    Object.keys(params).forEach((function (t) {
        if (t == h)
            return !1;
        params.hasOwnProperty(t) && r.push(params[t])
    })),
        r = r.sort().join(""),
        r = (0, cv)(r),8
        r += d + url.replace(baseURL, ""),
        r += d + o,
        r += d + 1,
        a = (0, cv)((0, oZ)(r, l))
    return a
}

var url = "/rank/indexPlus/brand_id/2",
    params = {brand: 'all', device: 'iphone', country: 'cn', genre: '36'}

console.log(get_aaa(url, params))