local redis = require("resty.redis")

local redutils = {
    OK = 0,
    ERROR = 1,
    EXISTS = 10,
    NOT_EXISTS = 20,
    KEY_ERROR = 30,
}

function redutils.get_redis(host, port, password, database, log)
    -- set default parameter values
    if database == nil then
        database = 0
    end
    if log == nil then
        log = print
    end
    -- create redis isntance
    local red_sock_opts = {
        pool = host .. ":" .. port .. ":" .. database,
    }
    local red = redis.new()
    -- do connect
    local red_ready, red_err = red:connect(host, port, red_sock_opts)
    if not red_ready then
        log("get redis connection failed on connect: ", red_err)
        return nil
    end
    -- do auth
    if password then
        local red_ready, red_err = red:auth(password)
        if not red_ready then
            log("get redis connection failed on auth: " .. red_err)
            return nil
        end
    end
    -- do db select
    local ok, red_err = red:select(database)
    if red_err then
        log("get redis connection failed on select db: " .. red_err)
        return nil
    end
    -- done
    return red
end

function redutils.sismember(red, key, member, log)
    -- set default parameter values
    if log == nil then
        log = print
    end
    -- check redis instance
    if red == nil then
        log("Bad redis connection...")
        return redutils.ERROR, "Bad redis connection..."
    end
    -- check key exists
    local exists, op_err = red:exists(key)
    if op_err then
        log("call red:exists failed: " .. op_err)
        return redutils.ERROR, op_err
    end
    if exists == 1 then
        -- check sismember
        local ismember, op_err = red:sismember(key, member)
        if op_err then
            log("call red:sismember failed: " .. op_err)
            return redutils.ERROR, op_err
        end
        -- result
        if ismember == 1 then
            return redutils.EXISTS, nil
        else
            return redutils.NOT_EXISTS, nil
        end
    else
        return redutils.KEY_ERROR, "key=" .. key .. " not exists..."
    end
end


return redutils
