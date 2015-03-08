Object.createHandled = function(proto, objDesc, noSuchMethod) {
  var handler = {
    get: function(rcvr, p) {
      return function() {
        var args = [].slice.call(arguments, 0);
        return noSuchMethod.call(this, p, args);
      };
    }
  };
  var p = Proxy.create(handler, proto);
  return Object.create(p, objDesc);
};
