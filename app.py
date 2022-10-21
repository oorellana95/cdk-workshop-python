#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack
from cdk_workshop.cdk_sns_stack import CdkSnsStack

app = cdk.App()
CdkWorkshopStack(app, "cdk-workshop")
CdkSnsStack(app, "cdk-sns")

app.synth()
