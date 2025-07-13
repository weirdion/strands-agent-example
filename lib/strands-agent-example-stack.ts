import * as cdk from 'aws-cdk-lib';
import { Function, Runtime, Code, LayerVersion, Architecture } from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import { LambdaIntegration, LambdaRestApi } from 'aws-cdk-lib/aws-apigateway';
import { LogGroup, RetentionDays } from 'aws-cdk-lib/aws-logs';
import { RemovalPolicy } from 'aws-cdk-lib';

export interface StrandsAgentExampleStackProps extends cdk.StackProps {
}


export class StrandsAgentExampleStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: StrandsAgentExampleStackProps) {
    super(scope, id, props);

    // Lambda Layer for Python dependencies
    const pythonStrandsLayer = new LayerVersion(this, 'StrandsPythonLayer', {
      code: Code.fromAsset('lambda/layer'),
      compatibleRuntimes: [Runtime.PYTHON_3_12, Runtime.PYTHON_3_13],
      description: 'Python dependencies for Strands Agent Example',
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // lambda function
    const apiLambda = new Function(this, 'StrandsAgentExampleLambda', {
      runtime: Runtime.PYTHON_3_13,
      code: Code.fromAsset('app'),
      handler: 'main.handler',
      layers: [pythonStrandsLayer],
      environment: {
        MODEL_ACCOUNT_ID: cdk.Stack.of(this).account,
        MODEL_REGION: cdk.Stack.of(this).region,
      },
      logGroup: new LogGroup(this, 'StrandsAgentExampleLambdaLogGroup', {
        logGroupName: `/aws/lambda/${this.stackName}-StrandsAgentExampleLambda`,
        removalPolicy: RemovalPolicy.DESTROY,
        retention: RetentionDays.ONE_WEEK,
      }),
    });

    // api gateway
    const api = new LambdaRestApi(this, 'StrandsAgentExampleApi', {
      handler: apiLambda,
      proxy: false,
      deployOptions: {
        stageName: 'v1',
      },
      description: 'API for Strands Agent Example'
    });

    const items = api.root.addResource('invoke');
    items.addMethod('POST', new LambdaIntegration(apiLambda), {
      apiKeyRequired: false,  // ONLY for example - FIX THIS in PROD
    });
  }
}
