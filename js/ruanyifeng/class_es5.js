"use strict";

var _inherits = function (subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) subClass.__proto__ = superClass; };

var _classCallCheck = function (instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } };

var A = function A() {
  _classCallCheck(this, A);
};

var B = (function (A) {
  function B() {
    _classCallCheck(this, B);

    if (A != null) {
      A.apply(this, arguments);
    }
  }

  _inherits(B, A);

  return B;
})(A);

var C = (function (Object) {
  function C() {
    _classCallCheck(this, C);

    if (Object != null) {
      Object.apply(this, arguments);
    }
  }

  _inherits(C, Object);

  return C;
})(Object);

var a = new A();
var b = new B();

console.log(A.prototype, A.__proto__);
console.log(B.__proto__ === A);
console.log(C.__proto__ === Object);
// false
console.log(b.__proto__.__proto__ === a.__proto__);
// true
console.log(b.__proto__);
console.log(b.__proto__.__proto__);

