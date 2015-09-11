EventEmitter = require('events').EventEmitter
redisPool = require 'sol-redis-pool'
stamp = require 'stampit'

promisify = require('app/lib/promisify').promisify1

defaultPoolOpts =
  max: 16
  min: 4

acquire = (pool, priority) ->
  new Promise (resolve, reject) ->
    pool.acquire (error, conn) ->
      if error then reject error
      else resolve conn
    ,
    priority

get = (conn, key) -> promisify(conn.get, conn) key

set = (conn, key, value, ttl) ->
  if typeof ttl is 'number'
    promisify(conn.setex, conn) key, ttl, value
  else
    promisify(conn.set, conn) key, value
  
del = (conn, key) -> promisify(conn.del, conn) key

keys = (conn, pattern) -> promisify(conn.keys, conn) pattern
  

factory = stamp
  .methods EventEmitter.prototype
  .init ({args, instance, stamp}) ->
    options = args[0] or {}
    options.host = options.host or 'localhost'
    options.port = options.port or 6379

    poolOpts = args[1] or defaultPoolOpts
    defaultTtl = poolOpts.ttl

    pool = redisPool options, poolOpts
    pool.on 'error', @emit.bind @, 'error'

    functions =
      'get': (conn, key) ->
        data = yield get conn, key
        data = JSON.parse data if data
        data

      'set': (conn, key, value, ttl) ->
        ttl = ttl or defaultTtl
        yield set conn, key, JSON.stringify value, ttl

      'del': (conn, key) ->
        yield del conn, key
        
      'keys': (conn, pattern) ->
        pattern = pattern or '*'
        yield keys conn, pattern

      'reset': (conn) ->
        for key in yield keys conn, '*'
          yield del conn, key
        return

    for name, func of functions
      @[name] = ((f) -> (args...) ->
        conn = yield acquire pool
        args.unshift conn
        try
          ret = yield f.apply null, args
        finally
          pool.release conn
        ret) func
    return
    
module.exports = (options, poolOpts) ->
  factory(null, options, poolOpts)
