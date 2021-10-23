function encrypt(e) {
    var i, t, r, n = [];
    if (void 0 === e)
        return "";
    for (r = function (e) {
        var code, t = [], i = 0, r = 0;
        for (i = 0; i < e.length; i++)
            0 <= (code = e.charCodeAt(i)) && code <= 127 ? t.push(code) : 128 <= code && code <= 2047 ? (t.push(192 | 31 & code >> 6),
                t.push(128 | 63 & code)) : (2048 <= code && code <= 55295 || 57344 <= code && code <= 65535) && (t.push(224 | 15 & code >> 12),
                t.push(128 | 63 & code >> 6),
                t.push(128 | 63 & code));
        for (r = 0; r < t.length; r++)
            t[r] &= 255;
        return t
    }(e += ""),
             i = 0,
             t = r.length; i < t; ++i)
        n.push((5 ^ r[i]).toString(16));
    return n.join("");
}
