# Strands Agent Example

An example app for building personal agentic AI backends using AWS Lambda, API Gateway, and [Strands Agents](https://strandsagents.com/).  
This project demonstrates a hybrid TypeScript (AWS CDK) and Python (with AWS Powertools) workflow, with poetry dependency management and Lambda Layer separation.

## 🛠️ Project Structure

```
.
├── app/                # Python Lambda source (Powertools, Strands Agent logic)
│   ├── agent.py
│   └── main.py
├── lambda/layer/       # Lambda Layer for Python dependencies (built via Poetry/Makefile)
├── lib/                # CDK TypeScript stack (API Gateway, Lambda, Layer)
├── bin/                # CDK entrypoint
├── test/               # CDK/infra tests
├── pyproject.toml      # Poetry project config for lambda dependencies
├── package.json        # Node/TypeScript project config for CDK
├── Makefile            # Build, lint, and layer automation
└── ...
```

## 🚀 Quickstart

### 1. Initialize the Project (Recommended for new users)

```sh
make
```

- Installs Node/TypeScript and Python dependencies (via Poetry)
- Installs the pre-commit hook for lint and test

### 2. Build the Lambda Layer

```sh
make layer
```

- Exports Python dependencies from Poetry and installs them into `lambda/layer/python` for Lambda Layer packaging.

### 3. Deploy to AWS

```sh
npx cdk deploy
```

- Deploys the stack: Lambda Layer, Lambda function, and API Gateway.

## 🧹 Pre-commit Hook (via Husky)

This repo uses [Husky](https://typicode.github.io/husky/) to run `make lint-check` and `npm test` before every commit. The hook is installed automatically with `make` or `make setup`.

To (re)install the hook manually:

```sh
make setup
```

To customize the hook, edit `.husky/pre-commit`.

## 🔁 API Usage

After deployment, your API Gateway endpoint will look like:

```
POST https://<api-id>.execute-api.<region>.amazonaws.com/v1/invoke
```

**Example request:**

```sh
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, agent!"}' \
  https://<api-id>.execute-api.<region>.amazonaws.com/v1/invoke
```

**Expected response:**

```json
{"message": "<agent response>"}
```


## 💸 Cost Estimate

Running this stack is very affordable for most personal and prototype use cases, but here are the main cost factors:

- **AWS Lambda:**
  - Free tier: 1M requests and 400,000 GB-seconds compute per month ([Lambda pricing](https://aws.amazon.com/lambda/pricing/)).
  - After free tier: ~$0.20 per 1M requests, plus compute time (depends on memory and duration).

- **API Gateway:**
  - Free tier: 1M HTTP API calls per month ([API Gateway pricing](https://aws.amazon.com/api-gateway/pricing/)).
  - After free tier: ~$1.00 per 1M requests.

- **Lambda Layer storage:**
  - No extra charge for using Lambda Layers, but you pay for total Lambda storage if you have many versions ([Lambda storage pricing](https://aws.amazon.com/lambda/pricing/)).

- **Amazon Bedrock Model Inference:**
  - Each API call invokes an Amazon Bedrock model (by default currently in strands, Sonnet 3.7).
  - Pricing depends on the model and tokens processed ([Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)).
  - As of July 2025, Sonnet 3.7 is ~$0.0030 per 1,000 input tokens and ~$0.0150 per 1,000 output tokens (check the link for current rates).

**Example:**

If you run 100,000 invocations per month, each <1s and <512MB, and each prompt/response averages 1,000 tokens in and 1,000 tokens out:

- Lambda and API Gateway: Likely free (within free tier) for most new AWS accounts; after free tier, well under $1/month for typical usage.
- Bedrock Sonnet 3.7: ~$0.0030 + $0.0150 = $0.018 per invocation → $1.80 per 100,000 invocations (token usage will vary).

> For up-to-date details, always check the official AWS pricing pages linked above.


## 🪪 License

MIT
