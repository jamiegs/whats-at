DEPLOY_S3_BUCKET="deploy-payloads"

build:
	sam build --use-container

test: build
	sam local invoke PageScraperFunction --event tests/test_events/renderer_event.json
	sam local invoke PageRendererFunction --event tests/test_events/renderer_event.json
	
test_scraper: build
	sam local invoke PageScraperFunction --event tests/test_events/renderer_event.json

test_renderer: build
	sam local invoke PageRendererFunction --event tests/test_events/renderer_event.json

package: build
	sam validate
	mkdir -p out/
	sam package --s3-bucket $(DEPLOY_S3_BUCKET) --s3-prefix whats-at-abes --output-template-file out/packaged-template.yaml

deploy: package
	sam deploy --template-file out/packaged-template.yaml --capabilities CAPABILITY_IAM --parameter-overrides param1=param1value --stack-name whats-at-abes-2