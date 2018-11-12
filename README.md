# paperboy

Brief morning news.

## Quickstart

This project uses [Zappa](https://github.com/Miserlou/Zappa) to deploy a simple Python application to [AWS Lambda](https://aws.amazon.com/lambda/). If you haven't already, create a local [AWS credentials file](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks/).

Install requirements:

    $ make requirements

Package and deploy the service:

    $ make deploy

Finally, set environment variables the app needs to function.

If you make a change and want to deploy again:

    $ make ship

## Development

Run the script:

    $ make paperboy

Run the linter:

    $ make lint
