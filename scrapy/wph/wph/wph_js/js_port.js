const express = require('express')
const app = express()
const port = 5555

app.get('/mars_cid', (req, res) => {
    var data = mars_cid()
    res.send(data)
})

app.listen(port, () => {
    console.log(`app listening on port: ${port}`)
})

//
var Mar = {}
Mar.Util = {
    detect: function () {
        var a, b, c, d = !1, e = window.navigator.userAgent;
        return /MSIE/.test(e) ? (b = "MSIE",
        /IEMobile/.test(e) && (d = !0),
            c = /MSIE \d+[.]\d+/.exec(e)[0].split(" ")[1]) : navigator.userAgent.match(/Trident.*rv[ :]*11\./) ? (b = "MSIE",
            c = 11) : /Chrome/.test(e) ? (b = "Chrome",
            c = /Chrome\/[\d\.]+/.exec(e)[0].split("/")[1]) : /Opera/.test(e) ? (b = "Opera",
        (/mini/.test(e) || /Mobile/.test(e)) && (d = !0)) : /Android/.test(e) ? (b = "Android Webkit Browser",
            d = !0) : /Firefox/.test(e) ? (b = "Firefox",
        /Fennec/.test(e) && (d = !0),
            c = /Firefox\/[\.\d]+/.exec(e)[0].split("/")[1]) : /Safari/.test(e) && (b = "Safari",
        (/iPhone/.test(e) || /iPad/.test(e) || /iPod/.test(e)) && (d = !0)),
        c || (c = /Version\/[\.\d]+/.exec(e),
            c = c ? c[0].split("/")[1] : void 0),
            a = {
                browser: b,
                version: c,
                mobile: d
            }
    },
    isElement: function (a) {
        return !(!a || "function" != typeof HTMLElement && "object" != typeof HTMLElement || !(a instanceof HTMLElement)) || !(!a || !a.nodeType || 1 !== a.nodeType)
    },
    encryptCid: function (a) {
        var b = a.split("_")
            , c = b[0]
            , d = b[1];
        if (!c || !d)
            return a;
        for (var e = 0, f = c.length, g = 0; g < f; g++)
            e += parseInt(c[g]);
        for (var h = e % 32, i = e, j = d.length, g = 0; g < j; g++)
            g !== h && (i += parseInt(d[g], 16));
        var k = (i % 16).toString(16);
        return c + "_" + d.substr(0, h) + k.toString() + d.substr(h + 1, j)
    },
    pad: function (a, b) {
        for (var c = a.toString().length; c < b;)
            a = "0" + a,
                c++;
        return a
    },
};
Mar.Random = {
    guid: function () {
        for (var a = 0, b = []; a < 8;)
            b.push((65536 * (1 + Math.random()) | 0).toString(16).substring(1)),
                a++;
        return b.join("").toUpperCase()
    },
    rand: function (a) {
        var b = "0123456789abcdef"
            , c = ""
            , d = 0;
        for (a = a || 32; d < a; d++)
            c += b.charAt(Math.ceil(1e8 * Math.random()) % b.length);
        return c
    }
};

function mars_cid() {
    _a = Mar.Util.encryptCid(Mar.Util.pad((new Date).getTime(), 13) + "_" + Mar.Random.rand())
    return _a
}