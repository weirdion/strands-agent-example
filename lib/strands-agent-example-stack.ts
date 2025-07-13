import * as cdk from 'aws-cdk-lib';
import { Function, Runtime, Code, LayerVersion } from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import { LambdaIntegration, LambdaRestApi } from 'aws-cdk-lib/aws-apigateway';

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
      apiKeyRequired: false,
    });
  }
}
