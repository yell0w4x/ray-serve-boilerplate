# Minimal Ray cluster web application boilerplate for AWS

> **&#9432;** Make sure that you have active AWS credentials here `~/.aws/credentials`.
> For successful deploy use python version same to `rayproject/ray` docker image. At the moment it's python 3.7.
> I use conda for python install.

    git clone https://github.com/yell0w4x/ray-serve-boilerplate.git
    cd ray-serve-boilerplate
    pip install -r requirements.txt

Create cluster and run multiple deployment by issuing line as is follows

    ./deploy

Or issue these

    # Create cluster
    ray up -y cluster.yaml
    
    # Push code to cluster 
    # It should be ray rsync-up cluster.yaml src/serve_native_deployment/asdf_deployment.py /home/ray, but somehow it doesn't work
    ray submit cluster.yaml src/serve_native_deployment/asdf_deployment.py

    # ~/.ssh/ray-autoscaler_us-west-2.pem key file created on first step
    # Run following line in separate console.
    ssh -L 52365:localhost:52365 -nNT -i ~/.ssh/ray-autoscaler_us-west-2.pem -v ubuntu@<head-node-ip>
    serve deploy src/serve_native_deployment/asdf_deployment.yaml

To shutdown the app

    serve shutdown -y

To run the app and get an output

    ssh -L 10001:localhost:10001 -nNT -i ~/.ssh/ray-autoscaler_us-west-2.pem -v ubuntu@<head-node-ip>
    RAY_ADDRESS=ray://localhost:10001 serve run serve_native_deployment/asdf_deployment:app

For dashboard access

    ray dashboard cluster.yaml

Dashboard access http://localhost:8265. To attach to head node terminal issue this one.

    ray attach cluster.yaml

## Destroy cluster

    ray down -y cluster.yaml

## Fastapi based

    ray submit cluster.yaml src/fastapi_deployment/fastapi_deployment.py
    serve deploy src/fastapi_deployment/fastapi_deployment.yaml

## Multiple deployment

> **&#9432;** Make sure you have at least 2Gb ram for default ray config (refer to docs). 
> Instead OOM may occur.

    ray submit cluster.yaml src/multiple_deployment/calculator.py
    ray submit cluster.yaml src/multiple_deployment/geet.py
    serve deploy src/multiple_deployment/multiple_deployment.yaml

# Ray docs

https://docs.ray.io/
