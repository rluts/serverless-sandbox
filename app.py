from aws_cdk import core as cdk

from cdk_app.cdk_app_stack import CdkAppStack


app = cdk.App()
CdkAppStack(app, "CdkStack")

app.synth()
