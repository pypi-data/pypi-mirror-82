package = "lua-fastutils"
version = "0.1.0-1"
source = {
    url = "lua-fastutils-0.1.0-1.zip"
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
        ["fastutils.strutils"] = "lua/strutils.lua",
    }
}