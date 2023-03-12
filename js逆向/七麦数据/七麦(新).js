const jsdom = require('jsdom')
const {JSDOM} = jsdom
const dom = new JSDOM('<!DOCTYPE html>');
window = dom.window

function v(t) {
    t = encodeURIComponent(t)['replace'](/%([0-9A-F]{2})/g, function (n, t) {
        return o('0x' + t)
    });
    return window.btoa(t)
}

function o(n) {
    t = '',
        ['66', '72', '6f', '6d', '43', '68', '61', '72', '43', '6f', '64', '65']['forEach'](function (n) {
            t += escape("%u00" + n)
        });
    var t, e = t;
    return String.fromCharCode(n)
}

function h(n, t) {
    for (var e = (n = n['split'](''))['length'], r = t['length'], a = 'charCodeAt', i = 0; i < e; i++)
        n[i] = o(n[i][a](0) ^ t[(i + 10) % r][a](0));
    return n['join']('')
}

function get_analysis(url, time) {
    t = Date.now() - ((time * 1000) - Date.now()) - 1661224081041
    a = `@#${url}@#${t}@#3`
    // a = '@#/rank/indexPlus/brand_id/1@#17415837463@#3'
    analysis = v(h(a, 'xyz517cda96abcd'))
    return analysis
}

// analysis = (0,[jt])((0,i[qt])(a, 'xyz517cda96abcd'))
console.log(get_analysis(1, 2))