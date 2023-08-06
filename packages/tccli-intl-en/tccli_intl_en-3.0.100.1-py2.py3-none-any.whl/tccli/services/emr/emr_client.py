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
from tencentcloud.emr.v20190103 import emr_client as emr_client_v20190103
from tencentcloud.emr.v20190103 import models as models_v20190103
from tccli.services.emr import v20190103
from tccli.services.emr.v20190103 import help as v20190103_help


def doTerminateTasks(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("TerminateTasks", g_param[OptionsDefine.Version])
        return

    param = {
        "InstanceId": argv.get("--InstanceId"),
        "ResourceIds": Utils.try_to_json(argv, "--ResourceIds"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.EmrClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.TerminateTasksRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.TerminateTasks(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeInstances(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeInstances", g_param[OptionsDefine.Version])
        return

    param = {
        "DisplayStrategy": argv.get("--DisplayStrategy"),
        "InstanceIds": Utils.try_to_json(argv, "--InstanceIds"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),
        "ProjectId": Utils.try_to_json(argv, "--ProjectId"),
        "OrderField": argv.get("--OrderField"),
        "Asc": Utils.try_to_json(argv, "--Asc"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.EmrClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeInstancesRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeInstances(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doInquiryPriceUpdateInstance(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("InquiryPriceUpdateInstance", g_param[OptionsDefine.Version])
        return

    param = {
        "TimeUnit": argv.get("--TimeUnit"),
        "TimeSpan": Utils.try_to_json(argv, "--TimeSpan"),
        "UpdateSpec": Utils.try_to_json(argv, "--UpdateSpec"),
        "PayMode": Utils.try_to_json(argv, "--PayMode"),
        "Placement": Utils.try_to_json(argv, "--Placement"),
        "Currency": argv.get("--Currency"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.EmrClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.InquiryPriceUpdateInstanceRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.InquiryPriceUpdateInstance(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeClusterNodes(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("DescribeClusterNodes", g_param[OptionsDefine.Version])
        return

    param = {
        "InstanceId": argv.get("--InstanceId"),
        "NodeFlag": argv.get("--NodeFlag"),
        "Offset": Utils.try_to_json(argv, "--Offset"),
        "Limit": Utils.try_to_json(argv, "--Limit"),
        "HardwareResourceType": argv.get("--HardwareResourceType"),
        "SearchFields": Utils.try_to_json(argv, "--SearchFields"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.EmrClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeClusterNodesRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.DescribeClusterNodes(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doInquiryPriceRenewInstance(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("InquiryPriceRenewInstance", g_param[OptionsDefine.Version])
        return

    param = {
        "TimeSpan": Utils.try_to_json(argv, "--TimeSpan"),
        "ResourceIds": Utils.try_to_json(argv, "--ResourceIds"),
        "Placement": Utils.try_to_json(argv, "--Placement"),
        "PayMode": Utils.try_to_json(argv, "--PayMode"),
        "TimeUnit": argv.get("--TimeUnit"),
        "Currency": argv.get("--Currency"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.EmrClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.InquiryPriceRenewInstanceRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.InquiryPriceRenewInstance(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doCreateInstance(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("CreateInstance", g_param[OptionsDefine.Version])
        return

    param = {
        "ProductId": Utils.try_to_json(argv, "--ProductId"),
        "VPCSettings": Utils.try_to_json(argv, "--VPCSettings"),
        "Software": Utils.try_to_json(argv, "--Software"),
        "ResourceSpec": Utils.try_to_json(argv, "--ResourceSpec"),
        "SupportHA": Utils.try_to_json(argv, "--SupportHA"),
        "InstanceName": argv.get("--InstanceName"),
        "PayMode": Utils.try_to_json(argv, "--PayMode"),
        "Placement": Utils.try_to_json(argv, "--Placement"),
        "TimeSpan": Utils.try_to_json(argv, "--TimeSpan"),
        "TimeUnit": argv.get("--TimeUnit"),
        "LoginSettings": Utils.try_to_json(argv, "--LoginSettings"),
        "COSSettings": Utils.try_to_json(argv, "--COSSettings"),
        "SgId": argv.get("--SgId"),
        "PreExecutedFileSettings": Utils.try_to_json(argv, "--PreExecutedFileSettings"),
        "AutoRenew": Utils.try_to_json(argv, "--AutoRenew"),
        "ClientToken": argv.get("--ClientToken"),
        "NeedMasterWan": argv.get("--NeedMasterWan"),
        "RemoteLoginAtCreate": Utils.try_to_json(argv, "--RemoteLoginAtCreate"),
        "CheckSecurity": Utils.try_to_json(argv, "--CheckSecurity"),
        "ExtendFsField": argv.get("--ExtendFsField"),
        "Tags": Utils.try_to_json(argv, "--Tags"),
        "DisasterRecoverGroupIds": Utils.try_to_json(argv, "--DisasterRecoverGroupIds"),
        "CbsEncrypt": Utils.try_to_json(argv, "--CbsEncrypt"),
        "MetaType": argv.get("--MetaType"),
        "UnifyMetaInstanceId": argv.get("--UnifyMetaInstanceId"),
        "MetaDBInfo": Utils.try_to_json(argv, "--MetaDBInfo"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.EmrClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.CreateInstanceRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.CreateInstance(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doInquiryPriceCreateInstance(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("InquiryPriceCreateInstance", g_param[OptionsDefine.Version])
        return

    param = {
        "TimeUnit": argv.get("--TimeUnit"),
        "TimeSpan": Utils.try_to_json(argv, "--TimeSpan"),
        "ResourceSpec": Utils.try_to_json(argv, "--ResourceSpec"),
        "Currency": argv.get("--Currency"),
        "PayMode": Utils.try_to_json(argv, "--PayMode"),
        "SupportHA": Utils.try_to_json(argv, "--SupportHA"),
        "Software": Utils.try_to_json(argv, "--Software"),
        "Placement": Utils.try_to_json(argv, "--Placement"),
        "VPCSettings": Utils.try_to_json(argv, "--VPCSettings"),
        "MetaType": argv.get("--MetaType"),
        "UnifyMetaInstanceId": argv.get("--UnifyMetaInstanceId"),
        "MetaDBInfo": Utils.try_to_json(argv, "--MetaDBInfo"),
        "ProductId": Utils.try_to_json(argv, "--ProductId"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.EmrClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.InquiryPriceCreateInstanceRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.InquiryPriceCreateInstance(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doInquiryPriceScaleOutInstance(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("InquiryPriceScaleOutInstance", g_param[OptionsDefine.Version])
        return

    param = {
        "TimeUnit": argv.get("--TimeUnit"),
        "TimeSpan": Utils.try_to_json(argv, "--TimeSpan"),
        "ZoneId": Utils.try_to_json(argv, "--ZoneId"),
        "PayMode": Utils.try_to_json(argv, "--PayMode"),
        "InstanceId": argv.get("--InstanceId"),
        "CoreCount": Utils.try_to_json(argv, "--CoreCount"),
        "TaskCount": Utils.try_to_json(argv, "--TaskCount"),
        "Currency": argv.get("--Currency"),
        "RouterCount": Utils.try_to_json(argv, "--RouterCount"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.EmrClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.InquiryPriceScaleOutInstanceRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.InquiryPriceScaleOutInstance(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doScaleOutInstance(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("ScaleOutInstance", g_param[OptionsDefine.Version])
        return

    param = {
        "TimeUnit": argv.get("--TimeUnit"),
        "TimeSpan": Utils.try_to_json(argv, "--TimeSpan"),
        "InstanceId": argv.get("--InstanceId"),
        "PayMode": Utils.try_to_json(argv, "--PayMode"),
        "ClientToken": argv.get("--ClientToken"),
        "PreExecutedFileSettings": Utils.try_to_json(argv, "--PreExecutedFileSettings"),
        "TaskCount": Utils.try_to_json(argv, "--TaskCount"),
        "CoreCount": Utils.try_to_json(argv, "--CoreCount"),
        "UnNecessaryNodeList": Utils.try_to_json(argv, "--UnNecessaryNodeList"),
        "RouterCount": Utils.try_to_json(argv, "--RouterCount"),
        "SoftDeployInfo": Utils.try_to_json(argv, "--SoftDeployInfo"),
        "ServiceNodeInfo": Utils.try_to_json(argv, "--ServiceNodeInfo"),
        "DisasterRecoverGroupIds": Utils.try_to_json(argv, "--DisasterRecoverGroupIds"),
        "Tags": Utils.try_to_json(argv, "--Tags"),
        "HardwareResourceType": argv.get("--HardwareResourceType"),
        "PodSpec": Utils.try_to_json(argv, "--PodSpec"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.EmrClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.ScaleOutInstanceRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.ScaleOutInstance(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doTerminateInstance(argv, arglist):
    g_param = parse_global_arg(argv)
    if "help" in argv:
        show_help("TerminateInstance", g_param[OptionsDefine.Version])
        return

    param = {
        "InstanceId": argv.get("--InstanceId"),
        "ResourceIds": Utils.try_to_json(argv, "--ResourceIds"),

    }
    cred = credential.Credential(g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey])
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile)
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.EmrClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.TerminateInstanceRequest()
    model.from_json_string(json.dumps(param))
    rsp = client.TerminateInstance(model)
    result = rsp.to_json_string()
    jsonobj = None
    try:
        jsonobj = json.loads(result)
    except TypeError as e:
        jsonobj = json.loads(result.decode('utf-8')) # python3.3
    FormatOutput.output("action", jsonobj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


CLIENT_MAP = {
    "v20190103": emr_client_v20190103,

}

MODELS_MAP = {
    "v20190103": models_v20190103,

}

ACTION_MAP = {
    "TerminateTasks": doTerminateTasks,
    "DescribeInstances": doDescribeInstances,
    "InquiryPriceUpdateInstance": doInquiryPriceUpdateInstance,
    "DescribeClusterNodes": doDescribeClusterNodes,
    "InquiryPriceRenewInstance": doInquiryPriceRenewInstance,
    "CreateInstance": doCreateInstance,
    "InquiryPriceCreateInstance": doInquiryPriceCreateInstance,
    "InquiryPriceScaleOutInstance": doInquiryPriceScaleOutInstance,
    "ScaleOutInstance": doScaleOutInstance,
    "TerminateInstance": doTerminateInstance,

}

AVAILABLE_VERSION_LIST = [
    v20190103.version,

]
AVAILABLE_VERSIONS = {
     'v' + v20190103.version.replace('-', ''): {"help": v20190103_help.INFO,"desc": v20190103_help.DESC},

}


def emr_action(argv, arglist):
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
        helpstr = HelpTemplate.SERVICE % {"name": "emr", "desc": desc, "actions": action_str}
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
    cmd = NiceCommand("emr", emr_action)
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
            version = config["emr"][OptionsDefine.Version]
            params[OptionsDefine.Version] = "v" + version.replace('-', '')

        if params[OptionsDefine.Endpoint] is None:
            params[OptionsDefine.Endpoint] = config["emr"][OptionsDefine.Endpoint]
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

    helpmsg = HelpTemplate.ACTION % {"name": action, "service": "emr", "desc": desc, "params": docstr}
    print(helpmsg)


def get_actions_info():
    config = Configure()
    new_version = max(AVAILABLE_VERSIONS.keys())
    version = new_version
    try:
        profile = config._load_json_msg(os.path.join(config.cli_path, "default.configure"))
        version = profile["emr"]["version"]
        version = "v" + version.replace('-', '')
    except Exception:
        pass
    if version not in AVAILABLE_VERSIONS.keys():
        version = new_version
    return AVAILABLE_VERSIONS[version]["help"]
