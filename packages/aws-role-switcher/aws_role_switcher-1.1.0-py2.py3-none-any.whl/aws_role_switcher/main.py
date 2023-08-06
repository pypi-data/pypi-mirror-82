#!/usr/bin/env python3

import configparser
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from pathlib import Path

REGIONS = [
    "eu-north-1",
    "ap-south-1",
    "eu-west-3",
    "eu-west-2",
    "eu-west-1",
    "ap-northeast-2",
    "ap-northeast-1",
    "sa-east-1",
    "ca-central-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "eu-central-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]


class ARS():

    def init(self):
        self.config = configparser.ConfigParser()
        default_path = os.path.join(Path.home(), '.aws/credentials')
        extended_path = os.environ.get('AWS_PROFILE_SWITCHER_PATH')
        if extended_path:
            path = extended_path
        else:
            path = default_path
        self.config.read(path)

    def run(self, sys_args):
        profile_arg, region_arg = self.parse_arguments(sys_args)
        self.init()
        profile = self.prompt_for_profile_name(profile_arg)
        if profile:
            self.set_aws_environment_variables(profile)
        if not os.environ.get("AWS_DEFAULT_REGION"):
            self.set_aws_region(region_arg)

    def parse_arguments(self, sys_args):
        if len(sys_args) <= 1:
            return "", ""
        elif len(sys_args) == 2:
            return sys_args[1], ""
        else:
            return sys_args[1], sys_args[2]


    def set_aws_environment_variables(self, profile):
        variables = ["AWS_SECRET_ACCESS_KEY", "AWS_ACCESS_KEY_ID", "AWS_SESSION_TOKEN", "AWS_SECURITY_TOKEN"]
        for k, v in self.config[profile].items():
            if k.upper() in variables:
                print(f"export {k.upper()}={v}")


    def set_aws_region(self, arg):
        region = prompt('AWS_DEFAULT_REGION Not Set. Choose Region: ', default=arg, completer=FuzzyWordCompleter(REGIONS))
        if self.validate(region, REGIONS):
            print(f"export AWS_DEFAULT_REGION={region}")

    def validate(self, raw, expected):
        if raw in expected:
            return True
        else:
            raise Exception(f"{raw} is not valid, must be one of {expected}")

    def prompt_for_profile_name(self, arg):
        res = None
        profile = prompt('Enter Profile: ', default=arg, completer=FuzzyWordCompleter(self.config.sections()),
                         complete_while_typing=True)
        if self.validate(profile, self.config.sections()):
            res = profile
        return res



