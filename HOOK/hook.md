## headers ##

```
(function(){
    var org = window.XMLHttpRequest.prototype.setRequestHeader;
    window.XMLHttpRequest.prototype.setRequestHeader = function(key,value){
        if(key=='authorization'){
            debugger;
        }
        return org.apply(this,arguments);
    }
})();
```



## cookie ##

```
(function (){
    'use strict';
    var document = window.document;
    var cookie_cache = document.cookie;
    Object.defineProperty(document, 'cookie',  {
        set: function (val) {
            if (val.indexOf('mars_cid') != -1){
                debugger;
            }
            console.log('获取到cookie设置-->',val);
            return cookie_cache;
        },
        get: function () {
            console.log('Getting cookie');
            return cookie_cache;
        }
    })
})()
```



## url ##

```
(function () {
    var open = window.XMLHttpRequest.prototype.open;
    window.XMLHttpRequest.prototype.open = function (method, url, async) {
        if (url.indexOf("qpres") != -1) {
            debugger;
        }
        return open.apply(this, arguments);
    };
})();
```

