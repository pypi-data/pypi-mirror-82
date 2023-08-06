package = "lua-resty-fastutils"
version = "0.2.0-1"
source = {
    url = "lua-resty-fastutils-0.2.0-1.zip"
}
description = {
    summary = "Collection of simple utils.",
}
dependencies = {
    "lua >= 5.1, < 5.4",
}
build = {
    type = "builtin",
    modules = {
        ["resty.fastutils.httputils"] = "lua/httputils.lua",
        ["resty.fastutils.redisutils"] = "lua/redisutils.lua",
    }
}