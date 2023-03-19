from enum import Enum
from typing import Union, Literal
from fastapi import Request


class http_method(Enum):
    get = "get"
    post = "post"
    put = "put"
    patch = "patch"
    delete = "delete"
    head = "head"
    options = "options"
    trace = "trace"


class content_type(Enum):
    json = "application/json"
    text = "text/plain"
    html = "text/html"
    xml = "application/xml"
    yaml = "application/yaml"


class container_event(Enum):
    attach = "attach"
    commit = "commit"
    copy = "copy"
    create = "create"
    destroy = "destroy"
    detach = "detach"
    die = "die"
    exec_create = "exec_create"
    exec_detach = "exec_detach"
    exec_die = "exec_die"
    exec_start = "exec_start"
    export = "export"
    health_status = "health_status"
    kill = "kill"
    oom = "oom"
    pause = "pause"
    rename = "rename"
    resize = "resize"
    restart = "restart"
    start = "start"
    stop = "stop"
    top = "top"
    unpause = "unpause"
    update = "update"


class image_event(Enum):
    create = "create"
    delete = "delete"
    import_ = "import"
    load = "load"
    pull = "pull"
    push = "push"
    save = "save"
    tag = "tag"
    untag = "untag"


class network_event(Enum):
    connect = "connect"
    create = "create"
    destroy = "destroy"
    disconnect = "disconnect"
    enable_ipv6 = "enable_ipv6"
    enable_ip_masquerade = "enable_ip_masquerade"
    ingress_sbox = "ingress_sbox"
    join = "join"
    leave = "leave"
    remove = "remove"
    update = "update"


class volume_event(str, Enum):
    create = "create"
    mount = "mount"
    remove = "remove"
    unmount = "unmount"


CloudEvent = Union[
                container_event, 
                image_event,
                network_event,
                volume_event
            ]