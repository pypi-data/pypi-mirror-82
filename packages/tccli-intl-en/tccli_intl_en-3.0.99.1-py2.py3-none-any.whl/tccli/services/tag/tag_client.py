# -*- coding: utf-8 -*-
import os
import json
import tccli.options_define as OptionsDefine
import tccli.format_output as FormatOutput
from tccli.nice_command import NiceCommand
import tccli.error_msg as ErrorMsg
import tccli.help_template as HelpTemplate
from tccli import __version__
from tccli.utils import Utils
from tccli.configure import Configure
from tencentcloud.common import credential
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.tag.v20180813 import tag_client as tag_client_v20180813
from tencentcloud.tag.v20180813 import models as models_v20180813
from tccli.services.tag import v20180813
from tccli.services.tag.v20180813 import help as v20180813_help


def doDescribeResourceTagsByTagKeys(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeResourceTagsByTagKeys", g_param[OptionsDefine.Version])
        return

    param = {
        "ServiceType": argv.get("--ServiceType"),
        "ResourcePrefix": argv.get("--ResourcePrefix"),
        "ResourceRegion": argv.get("--ResourceRegion"),
        "ResourceIds": Utils.try_to_json(argv, "--ResourceIds"),
        "TagKeys": Utils.try_to_json(argv, "--TagKeys"),
        "Limit": Utils.try_to_json(argv, "--Limit"),
        "Offset": Utils.try_to_json(argv, "--Offset"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeResourceTagsByTagKeysRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeResourceTagsByTagKeys(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeTagValuesSeq(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeTagValuesSeq", g_param[OptionsDefine.Version])
        return

    param = {
        "TagKeys": Utils.try_to_json(argv, "--TagKeys"),
        "CreateUin": Utils.try_to_json(argv, "--CreateUin"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeTagValuesSeqRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeTagValuesSeq(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDetachResourcesTag(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DetachResourcesTag", g_param[OptionsDefine.Version])
        return

    param = {
        "ServiceType": argv.get("--ServiceType"),
        "ResourceIds": Utils.try_to_json(argv, "--ResourceIds"),
        "TagKey": argv.get("--TagKey"),
        "ResourceRegion": argv.get("--ResourceRegion"),
        "ResourcePrefix": argv.get("--ResourcePrefix"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DetachResourcesTagRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DetachResourcesTag(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeTagValues(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeTagValues", g_param[OptionsDefine.Version])
        return

    param = {
        "TagKeys": Utils.try_to_json(argv, "--TagKeys"),
        "CreateUin": Utils.try_to_json(argv, "--CreateUin"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeTagValuesRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeTagValues(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeResourceTagsByResourceIds(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeResourceTagsByResourceIds", g_param[OptionsDefine.Version])
        return

    param = {
        "ServiceType": argv.get("--ServiceType"),
        "ResourcePrefix": argv.get("--ResourcePrefix"),
        "ResourceIds": Utils.try_to_json(argv, "--ResourceIds"),
        "ResourceRegion": argv.get("--ResourceRegion"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeResourceTagsByResourceIdsRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeResourceTagsByResourceIds(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeResourceTags(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeResourceTags", g_param[OptionsDefine.Version])
        return

    param = {
        "CreateUin": Utils.try_to_json(argv, "--CreateUin"),
        "ResourceRegion": argv.get("--ResourceRegion"),
        "ServiceType": argv.get("--ServiceType"),
        "ResourcePrefix": argv.get("--ResourcePrefix"),
        "ResourceId": argv.get("--ResourceId"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),
        "CosResourceId": Utils.try_to_json(argv, "--CosResourceId"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeResourceTagsRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeResourceTags(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doModifyResourceTags(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("ModifyResourceTags", g_param[OptionsDefine.Version])
        return

    param = {
        "Resource": argv.get("--Resource"),
        "ReplaceTags": Utils.try_to_json(argv, "--ReplaceTags"),
        "DeleteTags": Utils.try_to_json(argv, "--DeleteTags"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.ModifyResourceTagsRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.ModifyResourceTags(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeTagKeys(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeTagKeys", g_param[OptionsDefine.Version])
        return

    param = {
        "CreateUin": Utils.try_to_json(argv, "--CreateUin"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),
        "ShowProject": Utils.try_to_json(argv, "--ShowProject"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeTagKeysRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeTagKeys(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doUpdateResourceTagValue(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("UpdateResourceTagValue", g_param[OptionsDefine.Version])
        return

    param = {
        "TagKey": argv.get("--TagKey"),
        "TagValue": argv.get("--TagValue"),
        "Resource": argv.get("--Resource"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.UpdateResourceTagValueRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.UpdateResourceTagValue(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDeleteResourceTag(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DeleteResourceTag", g_param[OptionsDefine.Version])
        return

    param = {
        "TagKey": argv.get("--TagKey"),
        "Resource": argv.get("--Resource"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DeleteResourceTagRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DeleteResourceTag(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeResourcesByTagsUnion(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeResourcesByTagsUnion", g_param[OptionsDefine.Version])
        return

    param = {
        "TagFilters": Utils.try_to_json(argv, "--TagFilters"),
        "CreateUin": Utils.try_to_json(argv, "--CreateUin"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),
        "ResourcePrefix": argv.get("--ResourcePrefix"),
        "ResourceId": argv.get("--ResourceId"),
        "ResourceRegion": argv.get("--ResourceRegion"),
        "ServiceType": argv.get("--ServiceType"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeResourcesByTagsUnionRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeResourcesByTagsUnion(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeResourceTagsByResourceIdsSeq(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeResourceTagsByResourceIdsSeq", g_param[OptionsDefine.Version])
        return

    param = {
        "ServiceType": argv.get("--ServiceType"),
        "ResourcePrefix": argv.get("--ResourcePrefix"),
        "ResourceIds": Utils.try_to_json(argv, "--ResourceIds"),
        "ResourceRegion": argv.get("--ResourceRegion"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeResourceTagsByResourceIdsSeqRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeResourceTagsByResourceIdsSeq(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeTags(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeTags", g_param[OptionsDefine.Version])
        return

    param = {
        "TagKey": argv.get("--TagKey"),
        "TagValue": argv.get("--TagValue"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),
        "CreateUin": Utils.try_to_json(argv, "--CreateUin"),
        "TagKeys": Utils.try_to_json(argv, "--TagKeys"),
        "ShowProject": Utils.try_to_json(argv, "--ShowProject"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeTagsRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeTags(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeTagsSeq(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeTagsSeq", g_param[OptionsDefine.Version])
        return

    param = {
        "TagKey": argv.get("--TagKey"),
        "TagValue": argv.get("--TagValue"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),
        "CreateUin": Utils.try_to_json(argv, "--CreateUin"),
        "TagKeys": Utils.try_to_json(argv, "--TagKeys"),
        "ShowProject": Utils.try_to_json(argv, "--ShowProject"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeTagsSeqRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeTagsSeq(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeResourcesByTags(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeResourcesByTags", g_param[OptionsDefine.Version])
        return

    param = {
        "TagFilters": Utils.try_to_json(argv, "--TagFilters"),
        "CreateUin": Utils.try_to_json(argv, "--CreateUin"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),
        "ResourcePrefix": argv.get("--ResourcePrefix"),
        "ResourceId": argv.get("--ResourceId"),
        "ResourceRegion": argv.get("--ResourceRegion"),
        "ServiceType": argv.get("--ServiceType"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeResourcesByTagsRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeResourcesByTags(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doAddResourceTag(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("AddResourceTag", g_param[OptionsDefine.Version])
        return

    param = {
        "TagKey": argv.get("--TagKey"),
        "TagValue": argv.get("--TagValue"),
        "Resource": argv.get("--Resource"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.AddResourceTagRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.AddResourceTag(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDeleteTag(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DeleteTag", g_param[OptionsDefine.Version])
        return

    param = {
        "TagKey": argv.get("--TagKey"),
        "TagValue": argv.get("--TagValue"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DeleteTagRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DeleteTag(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doAttachResourcesTag(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("AttachResourcesTag", g_param[OptionsDefine.Version])
        return

    param = {
        "ServiceType": argv.get("--ServiceType"),
        "ResourceIds": Utils.try_to_json(argv, "--ResourceIds"),
        "TagKey": argv.get("--TagKey"),
        "TagValue": argv.get("--TagValue"),
        "ResourceRegion": argv.get("--ResourceRegion"),
        "ResourcePrefix": argv.get("--ResourcePrefix"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.AttachResourcesTagRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.AttachResourcesTag(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doCreateTag(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("CreateTag", g_param[OptionsDefine.Version])
        return

    param = {
        "TagKey": argv.get("--TagKey"),
        "TagValue": argv.get("--TagValue"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.CreateTagRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.CreateTag(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doModifyResourcesTagValue(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("ModifyResourcesTagValue", g_param[OptionsDefine.Version])
        return

    param = {
        "ServiceType": argv.get("--ServiceType"),
        "ResourceIds": Utils.try_to_json(argv, "--ResourceIds"),
        "TagKey": argv.get("--TagKey"),
        "TagValue": argv.get("--TagValue"),
        "ResourceRegion": argv.get("--ResourceRegion"),
        "ResourcePrefix": argv.get("--ResourcePrefix"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.TagClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.ModifyResourcesTagValueRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.ModifyResourcesTagValue(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


CLIENT_MAP = {
    "v20180813": tag_client_v20180813,

}

MODELS_MAP = {
    "v20180813": models_v20180813,

}

ACTION_MAP = {
    "DescribeResourceTagsByTagKeys": doDescribeResourceTagsByTagKeys,
    "DescribeTagValuesSeq": doDescribeTagValuesSeq,
    "DetachResourcesTag": doDetachResourcesTag,
    "DescribeTagValues": doDescribeTagValues,
    "DescribeResourceTagsByResourceIds": doDescribeResourceTagsByResourceIds,
    "DescribeResourceTags": doDescribeResourceTags,
    "ModifyResourceTags": doModifyResourceTags,
    "DescribeTagKeys": doDescribeTagKeys,
    "UpdateResourceTagValue": doUpdateResourceTagValue,
    "DeleteResourceTag": doDeleteResourceTag,
    "DescribeResourcesByTagsUnion": doDescribeResourcesByTagsUnion,
    "DescribeResourceTagsByResourceIdsSeq": doDescribeResourceTagsByResourceIdsSeq,
    "DescribeTags": doDescribeTags,
    "DescribeTagsSeq": doDescribeTagsSeq,
    "DescribeResourcesByTags": doDescribeResourcesByTags,
    "AddResourceTag": doAddResourceTag,
    "DeleteTag": doDeleteTag,
    "AttachResourcesTag": doAttachResourcesTag,
    "CreateTag": doCreateTag,
    "ModifyResourcesTagValue": doModifyResourcesTagValue,

}

AVAILABLE_VERSION_LIST = [
    v20180813.version,

]
AVAILABLE_VERSIONS = {
     'v' + v20180813.version.replace('-', ''): {"help": v20180813_help.INFO,"desc": v20180813_help.DESC},

}


def tag_action(argv, arglist):
    if "help" in argv:
        versions = sorted(AVAILABLE_VERSIONS.keys())
        opt_v = "--" + OptionsDefine.Version
        version = versions[-1]
        if opt_v in argv:
            version = 'v' + argv[opt_v].replace('-', '')
        if version not in versions:
            print("available versions: %s" % " ".join(AVAILABLE_VERSION_LIST))
            return
        action_str = ""
        docs = AVAILABLE_VERSIONS[version]["help"]
        desc = AVAILABLE_VERSIONS[version]["desc"]
        for action, info in docs.items():
            action_str += "        %s\n" % action
            action_str += Utils.split_str("        ", info["desc"], 120)
        helpstr = HelpTemplate.SERVICE % {"name": "tag", "desc": desc, "actions": action_str}
        print(helpstr)
    else:
        print(ErrorMsg.FEW_ARG)


def version_merge():
    help_merge = {}
    for v in AVAILABLE_VERSIONS:
        for action in AVAILABLE_VERSIONS[v]["help"]:
            if action not in help_merge:
                help_merge[action] = {}
            help_merge[action]["cb"] = ACTION_MAP[action]
            help_merge[action]["params"] = []
            for param in AVAILABLE_VERSIONS[v]["help"][action]["params"]:
                if param["name"] not in help_merge[action]["params"]:
                    help_merge[action]["params"].append(param["name"])
    return help_merge


def register_arg(command):
    cmd = NiceCommand("tag", tag_action)
    command.reg_cmd(cmd)
    cmd.reg_opt("help", "bool")
    cmd.reg_opt(OptionsDefine.Version, "string")
    help_merge = version_merge()

    for actionName, action in help_merge.items():
        c = NiceCommand(actionName, action["cb"])
        cmd.reg_cmd(c)
        c.reg_opt("help", "bool")
        for param in action["params"]:
            c.reg_opt("--" + param, "string")

        for opt in OptionsDefine.ACTION_GLOBAL_OPT:
            stropt = "--" + opt
            c.reg_opt(stropt, "string")


def parse_global_arg(argv):
    params = {}
    for opt in OptionsDefine.ACTION_GLOBAL_OPT:
        stropt = "--" + opt
        if stropt in argv:
            params[opt] = argv[stropt]
        else:
            params[opt] = None
    if params[OptionsDefine.Version]:
        params[OptionsDefine.Version] = "v" + params[OptionsDefine.Version].replace('-', '')

    config_handle = Configure()
    profile = config_handle.profile
    if ("--" + OptionsDefine.Profile) in argv:
        profile = argv[("--" + OptionsDefine.Profile)]

    is_conexist, conf_path = config_handle._profile_existed(profile + "." + config_handle.configure)
    is_creexist, cred_path = config_handle._profile_existed(profile + "." + config_handle.credential)
    config = {}
    cred = {}
    if is_conexist:
        config = config_handle._load_json_msg(conf_path)
    if is_creexist:
        cred = config_handle._load_json_msg(cred_path)
    if os.environ.get(OptionsDefine.ENV_SECRET_ID):
        cred[OptionsDefine.SecretId] = os.environ.get(OptionsDefine.ENV_SECRET_ID)
    if os.environ.get(OptionsDefine.ENV_SECRET_KEY):
        cred[OptionsDefine.SecretKey] = os.environ.get(OptionsDefine.ENV_SECRET_KEY)
    if os.environ.get(OptionsDefine.ENV_REGION):
        config[OptionsDefine.Region] = os.environ.get(OptionsDefine.ENV_REGION)

    for param in params.keys():
        if param == OptionsDefine.Version:
            continue
        if params[param] is None:
            if param in [OptionsDefine.SecretKey, OptionsDefine.SecretId]:
                if param in cred:
                    params[param] = cred[param]
                else:
                    raise Exception("%s is invalid" % param)
            else:
                if param in config:
                    params[param] = config[param]
                elif param == OptionsDefine.Region:
                    raise Exception("%s is invalid" % OptionsDefine.Region)
    try:
        if params[OptionsDefine.Version] is None:
            version = config["tag"][OptionsDefine.Version]
            params[OptionsDefine.Version] = "v" + version.replace('-', '')

        if params[OptionsDefine.Endpoint] is None:
            params[OptionsDefine.Endpoint] = config["tag"][OptionsDefine.Endpoint]
    except Exception as err:
        raise Exception("config file:%s error, %s" % (conf_path, str(err)))
    versions = sorted(AVAILABLE_VERSIONS.keys())
    if params[OptionsDefine.Version] not in versions:
        raise Exception("available versions: %s" % " ".join(AVAILABLE_VERSION_LIST))
    return params


def show_help(action, version):
    docs = AVAILABLE_VERSIONS[version]["help"][action]
    desc = AVAILABLE_VERSIONS[version]["desc"]
    docstr = ""
    for param in docs["params"]:
        docstr += "        %s\n" % ("--" + param["name"])
        docstr += Utils.split_str("        ", param["desc"], 120)

    helpmsg = HelpTemplate.ACTION % {"name": action, "service": "tag", "desc": desc, "params": docstr}
    print(helpmsg)


def get_actions_info():
    config = Configure()
    new_version = max(AVAILABLE_VERSIONS.keys())
    version = new_version
    try:
        profile = config._load_json_msg(os.path.join(config.cli_path, "default.configure"))
        version = profile["tag"]["version"]
        version = "v" + version.replace('-', '')
    except Exception:
        pass
    if version not in AVAILABLE_VERSIONS.keys():
        version = new_version
    return AVAILABLE_VERSIONS[version]["help"]
