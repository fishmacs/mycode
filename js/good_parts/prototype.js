// 函数的constructor调用模式
if (typeof Object.beget !== 'function') {
  Object.beget = function (o) {
    var F = function() {};
    F.prototype = o;
    return new F();
  };
}

var another_stooge = Object.beget(stooge);

var Quo = function(str) {
  this.status = str;
};

Quo.prototype.get_status = function() {
  return this.status;
};

var myQuo = new Quo('confused');
console.log(myQuo.get_status());

// apply调用模式
var statusObject = {
  status: 'A-OK'
};

var status = Quo.prototype.get_status.apply(statusObject);


Function.prototype.method = function(name, func) {
  if (!this.prototype[name])
    this.prototype[name] = func;
  return this;
};

Number.method('int', function() {
  return Math[this < 0 ? 'ceiling' : 'floor'](this);
});

String.method('trim', function() {
  return this.replace(/^\s+|\s+$/g, '');
});


var fade = (node) => {
  var level = 1;
  var step = () => {
    var hex = level.toString(16);
    node.style.backgroundColor = '#FFFF' + hex + hex;
    if (level < 15) {
      level += 1;
      setTimeout(setp, 100);
    }
  };
  setTimeout(step, 100);
};

fade(document.body);


// 糟糕的例子: alert的都是nodes.length
var add_the_handlers = (nodes) => {
  var i;
  for (i=0; i<nodes.length; i++) {
    nodes[i].onclick = (e) => {
      alert(i);
    };
  }
};

var add_the_handlers1 = (nodes) => {
  var i;
  for (i=0; i<nodes.length; i++) {
    nodes[i].onclick = (i) => {
      return (e) => {
        alert(e);
      };
    }(i);
  }
};


String.method('deentityify', () => {
  var entity = {
    quot: '"',
    lt: '<',
    gt: '>'
  };
  return () => {
    return this.replace(
      /&([^&;]+);/g,
      (a, b) => {
        var r = entity[b];
        return typeof r === 'string' ? r : a;
      }
    );
  };
}());


var serial_maker = () => {
  var prefix = '';
  var seq = 0;
  return {
    set_prefix: (p) => {
      prefix = String(p);
    },
    set_seq: (s) => {
      seq = s ;
    },
    gensym: () => {
      var result = prefix + seq;
      seq += 1;
      return result;
    }
  };
};

var seqer = serial_marker();
seqer.set_prefix('Q');
seqer.set_seq(1000);
var unique = seqer.gensym();


Function.method('curry', () => {
  var slice = Array.prototype.slice,
      args = slice.apply(arguments),
      that = this;
  return () => {
    return that.apply(null, args.concat(slice.apply(arguments)));
  };
});


function memoizer(memo, fundamental) {
  function shell(n) {
    var result = memo[n];
    if(typeof result !== 'number') {
      result = fundamental(shell, n);
      memo[n] = result;
    }
    return result;
  }
  return shell;
}

var fibonacci = memoizer([0, 1], (shell, n) => {
  return shell(n - 1) + shell(n - 2);
});


Function.method('inherites', (Parent) => {
  this.prototype = new Parent();
  return this;
});


function mammal(spec) {
  var that = {};

  that.get_name = () => {
    return spec.name;
  };

  that.says = () => {
    return spec.saying || '';
  };

  return that;
}

function cat(spec) {
  spec.saying = spec.saying || 'meow';
  var that = mammal(spec);

  that.purr = (n) => {
    let s = '';
    for(let i=0; i<n; i++) {
      if (s)
        s += '-';
      s += 'r';
    }
    return s;
  };

  that.get_name = () => {
    return that.says() + ' ' + spec.name + ' ' + that.says();
  };

  return that;
}

Object.method('superior', (name) => {
  var that = this, method = that[name];
  return () => {
    return method.apply(that, arguments);
  };
});

function coolcat(spec) {
  var that = cat(spec),
      super_get_name = that.superior('get_name');
  that.get_name = (n) => {
    return 'like ' + super_get_name() + ' baby';
  };
}


Function.method('new', () => {
  var that = Object.beget(this.prototype);
  var other = this.apply(that, arguments);
  return typeof other === 'object' && other || that;
});

Object.prototype.clone = () => {
  let copy = this.constructor();
  for (let attr in this) {
    if (this.hasOwnProperty(attr))
      copy[attr] = this[attr];
  }
  return copy;
};
