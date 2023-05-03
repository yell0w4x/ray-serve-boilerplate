from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from ray.serve.drivers import DAGDriver
from ray.serve.deployment_graph import InputNode
from ray.serve.http_adapters import json_request


@serve.deployment(ray_actor_options={"num_cpus": 0.1, "num_gpus": 0})
class Adder:
    def __call__(self, input: int) -> int:
        return input + 2


@serve.deployment(ray_actor_options={"num_cpus": 0.1, "num_gpus": 0})
class Multiplier:
    def __call__(self, input: int) -> int:
        return input * 2


@serve.deployment(ray_actor_options={"num_cpus": 0.1, "num_gpus": 0})
class Router:
    def __init__(
        self,
        adder: RayServeDeploymentHandle,
        multiplier: RayServeDeploymentHandle,
    ):
        self.adder = adder
        self.multiplier = multiplier

    async def route(self, op: str, input: int) -> int:
        if op == "ADD":
            return await (await self.adder.remote(input))
        elif op == "MUL":
            return await (await self.multiplier.remote(input))


with InputNode() as inp:
    operation, amount_input = inp[0], inp[1]

    multiplier = Multiplier.bind()
    adder = Adder.bind()
    router = Router.bind(adder, multiplier)
    amount = router.route.bind(operation, amount_input)

app = DAGDriver.options(route_prefix="/calculator", ray_actor_options={"num_cpus": 0.1, "num_gpus": 0}).bind(
    amount, http_adapter=json_request
)
