const crypto = require("crypto");
const express = require('express');

//秘钥
function _r() {
    var _o = {
        'codes': {
            0: 'W',
            1: 'l',
            2: 'k',
            3: 'B',
            4: 'Q',
            5: 'g',
            6: 'f',
            7: 'i',
            8: 'i',
            9: 'r',
            10: 'v',
            11: '6',
            12: 'A',
            13: 'K',
            14: 'N',
            15: 'k',
            16: '4',
            17: 'L',
            18: '1',
            19: '8'
        },
        'n': 20
    }
    for (var e = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "/").toLowerCase(), t = e + e, n = "", i = 0; i < t.length; ++i) {
        var a = t[i].charCodeAt() % _o.n;
        n += _o.codes[a]
    }
    return n
};

function hmac(encrypt_str, key) {
    var hmac = crypto.createHmac("sha512", key);
    var signed = hmac.update(Buffer.from(encrypt_str, 'utf-8')).digest('hex')
    return signed
}

var _s = function () {
    var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {}
        , t = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "/").toLowerCase()
        , n = JSON.stringify(e).toLowerCase();
    return hmac(t + n, _r(t)).toLowerCase().substr(8, 20)
};

var _ss = function () {
    var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {}
        , t = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : ""
        , n = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "/").toLowerCase()
        , i = JSON.stringify(e).toLowerCase();
    return hmac(n + "pathString" + i + t, _r(n))
}

// url 地址加参数
function get_params(url, pid) {
    key = _s(url, undefined);
    value = _ss(url, undefined, pid);
    return {'key': key, 'value': value}
}


// const app = express()
// const port = 5001
//
// app.get('/get_params', (req, res) => {
//     var _data = req.query.url_params;
//     var _pid = req.query.pids
//     res.send(get_params(_data, _pid))
//
// })
// app.listen(port, () => {
//     console.log(`port : ${port}`)
// })
