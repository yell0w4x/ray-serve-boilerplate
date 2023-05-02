import requests
from starlette.requests import Request
from typing import Dict

from ray import serve


# 1: Define a Ray Serve deployment.
# @serve.deployment(route_prefix="/", num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
@serve.deployment
class AsdfDeployment:
    def __init__(self, msg: str):
        # Initialize model state: could be very large neural net weights.
        self._msg = msg
        print('AsdfDeployment __init__')        

    async def __call__(self, request: Request) -> Dict:
        return {"result": self._msg}


app = AsdfDeployment.bind(msg="Consider using serverless")

# # 2: Deploy the model.
# serve.run(Deployment.bind(msg="Hello world!"))

# # 3: Query the deployment and print the result.
# print(requests.get("http://localhost:8000/").json())
# # {'result': 'Hello world!'}