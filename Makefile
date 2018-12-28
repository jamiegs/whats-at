BRANCH=$(shell git rev-parse --abbrev-ref HEAD)
#dry-run is enabled for non-master branches
DRYRUN=$(shell git rev-parse --abbrev-ref HEAD | grep "master" >> /dev/null && echo "false" || echo "true")
DEPLOY_S3_BUCKET="hudl-web-updates"

IS_PROD=$(shell git rev-parse --abbrev-ref HEAD | grep "master" >> /dev/null && echo "true" || echo "false")
ENV_PREFIX=$(shell git rev-parse --abbrev-ref HEAD | grep "master" >> /dev/null && echo "p" || echo "t")

STACK_NAME=$(ENV_PREFIX)-whatsat-$(BRANCH)

package:
	sam validate
	mkdir -p out/
	sam package --template-file template.yaml --s3-bucket $(DEPLOY_S3_BUCKET) --s3-prefix whatsat --output-template-file out/packaged-template.yaml

deploy-abes: package
	sam deploy --template-file out/packaged-template.yaml --capabilities CAPABILITY_IAM --parameter-overrides Branch=$(BRANCH) DryRunEnabled=$(DRYRUN) EnvironmentPrefix=$(ENV_PREFIX) RootDomainName=whatsatabes.com --stack-name $(ENV_PREFIX)-whatsatabes-$(BRANCH)

start-local-dynamodb:
	docker run -p 8000:8000 amazon/dynamodb-local