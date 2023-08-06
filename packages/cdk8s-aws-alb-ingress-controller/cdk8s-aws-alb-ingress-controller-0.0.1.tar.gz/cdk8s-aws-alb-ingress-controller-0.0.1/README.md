# cdk8s-aws-alb-ingress-controller

> [aws alb ingress controller](https://github.com/kubernetes-sigs/aws-alb-ingress-controller) constructs for cdk8s

Basic implementation of a [aws alb ingress controller](https://github.com/kubernetes-sigs/aws-alb-ingress-controller) construct for cdk8s. Contributions are welcome!

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk8s import App, Chart
from constructs import Construct
from cdk8s_aws_alb_ingress_controller import AlbIngressController

class MyChart(Chart):
    def __init__(self, scope, name):
        super().__init__(scope, name)
        AlbIngressController(self, "albingresscntroller",
            cluster_name="EKScluster"
        )
app = App()
MyChart(app, "testcdk8s")
app.synth()
```

## License

Distributed under the [Apache 2.0](./LICENSE) license.
