import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { StrandsAgentExampleStack } from '../lib/strands-agent-example-stack';

describe('StrandsAgentExampleStack', () => {
  let app: cdk.App;
  let stack: StrandsAgentExampleStack;
  let template: Template;

  beforeAll(() => {
    app = new cdk.App();
    stack = new StrandsAgentExampleStack(app, 'TestStack');
    template = Template.fromStack(stack);
  });

  it('creates a Lambda Layer for Python dependencies', () => {
    template.hasResourceProperties('AWS::Lambda::LayerVersion', {
      Description: 'Python dependencies for Strands Agent Example',
    });
  });

  it('creates a Lambda function with the correct handler and layer', () => {
    template.hasResourceProperties('AWS::Lambda::Function', {
      Handler: 'main.handler',
      Runtime: 'python3.13',
    });
  });

  it('grants the Lambda function permission to use Bedrock models', () => {
    template.hasResourceProperties('AWS::IAM::Policy', {
      PolicyDocument: {
        Statement: [
          {
            Action: 'bedrock:InvokeModelWithResponseStream',
            Effect: 'Allow',
            Resource: [
              {
                'Fn::Join': [
                  '',
                  [
                    'arn:aws:bedrock:',
                    { Ref: 'AWS::Region' },
                    ':',
                    { Ref: 'AWS::AccountId' },
                    ':inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0'
                  ]
                ]
              },
              'arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-3-7-sonnet-20250219-v1:0'
            ],
          },
        ],
        Version: '2012-10-17',
      },
    });
  });

  it('creates an API Gateway with /invoke POST method', () => {
    template.hasResourceProperties('AWS::ApiGateway::RestApi', {
      Description: 'API for Strands Agent Example',
    });
    template.hasResourceProperties('AWS::ApiGateway::Method', {
      HttpMethod: 'POST',
      AuthorizationType: 'NONE',
    });
    template.hasResourceProperties('AWS::ApiGateway::Resource', {
      PathPart: 'invoke',
    });
  });
});
