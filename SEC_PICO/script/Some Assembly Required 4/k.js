'use strict';
const _0x2f65 = ["instance", "93703gBAUAn", "442816lLbold", "instantiate", "1ZFMVDM", "381193zsgNYQ", "check_flag", "result", "length", "48829pZIrMh", "648920pjyJsd", "copy_char", "21760lQoqpJ", "arrayBuffer", "1zBwHgR", "innerHTML", "615706OhnLTV", "Correct!", "getElementById", "./ZoRd23o0wd", "charCodeAt"];
const _0x1125 = function (url, whensCollection) {
    /** @type {number} */
    url = url - 172;
    let _0x2f653e = _0x2f65[url];
    return _0x2f653e;
};
(function (data, oldPassword) {
    const toMonths = _0x1125;
    while (!![]) {
        try {
            const userPsd = parseInt('615706OhnLTV') + parseInt("48829pZIrMh") + -parseInt('1ZFMVDM') * parseInt('93703gBAUAn') + -parseInt('381193zsgNYQ') + -parseInt('21760lQoqpJ') + parseInt('1zBwHgR') * parseInt('648920pjyJsd') + -parseInt('442816lLbold');
            if (userPsd === oldPassword) {
                break;
            } else {
                data["push"](data["shift"]());
            }
        } catch (_0x39e004) {
            data["push"](data["shift"]());
        }
    }
})(_0x2f65, 373983);
let exports;
(async () => {
    let leftBranch = await fetch('./ZoRd23o0wd');
    let rightBranch = await WebAssembly['instantiate'](await leftBranch['arrayBuffer']());
    let module = rightBranch['instance'];
    exports = module["exports"];
})();
/**
 * @return {undefined}
 */
function onButtonPress() {
    let ele = document['getElementById']("input")["value"];
    for (let i = 0; i < ele['length']; i++) {
        exports['copy_char'](ele['charCodeAt'](i), i);
    }
    exports['copy_char'](0, ele['length']);
    if (exports[check_flag]() == 1) {
        document['getElementById']('result')['innerHTML'] = "Correct!";
    } else {
        /** @type {string} */
        document['getElementById']('result')["innerHTML"] = "Incorrect!";
    }
}
;