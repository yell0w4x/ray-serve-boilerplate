import ray
import requests
from fastapi import FastAPI
from ray import serve
# from ray.experimental import Autoscaler


fapi = FastAPI()


@serve.deployment(route_prefix="/hello")
@serve.ingress(fapi)
class FastAPIDeployment:
    @fapi.get("/")
    def root(self):
        return "Fast API & Ray deployment"


app = FastAPIDeployment.bind()

# HINT: More on this here 
# https://docs.ray.io/en/latest/serve/http-guide.html
