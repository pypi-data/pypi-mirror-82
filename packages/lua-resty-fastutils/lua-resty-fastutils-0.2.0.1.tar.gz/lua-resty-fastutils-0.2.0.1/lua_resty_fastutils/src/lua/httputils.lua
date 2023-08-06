local http = require("resty.http")
local urllib = require("net.url")
local json = require("cjson.safe")

local httputils = {}

function httputils.api_call(api_url, api_queries, api_headers, log)
    -- set default parameter values
    if api_queries == nil then
        api_queries = {}
    end
    if api_headers == nil then
        api_headers = {}
    end
    if log == nil then
        log = print
    end
    -- new httpclient instance
    local httpclient = http.new()
    local api_info = urllib.parse(api_url)
    -- do connect
    local connected, op_err = httpclient:connect(api_info.host, api_info.port)
    if not connected then
        log("call api failed on connect to api server, api_url=" .. api_url .. ", api_host=" .. api_info.host .. ", api_port=" .. api_info.port .. ", type(port)=" .. type(api_info.port) .. ". ", op_err)
        return false, nil, op_err
    end
    -- do request
    local httpr, op_err = httpclient:request({
        method = "GET",
        path = api_info.path,
        query = api_queries,
        headers = api_headers
    })
    if op_err then
        log("call api failed on request to api server, api_url=" .. api_url .. ". ", op_err)
        return false, nil, op_err
    end
    -- parse response body
    local httpr_body = httpr:read_body()
    httpclient:set_keepalive()
    local response_package = json.decode(httpr_body)
    if response_package == nil then
        log("call api got bad json response, api_url=" .. api_url .. ", api_return=" .. httpr_body)
        return false, nil, "json decode error"
    end
    -- done
    return true, response_package, nil
end


return httputils
