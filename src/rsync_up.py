import ray
from ray.autoscaler._private.commands import rsync
import os


def main():
    ray.init(address='ray://localhost:10001', runtime_env=dict(working_dir=os.getcwd()))

    local_path = "requirements.txt"
    remote_path = "/home/ray"
    rsync('cluster.yaml', source=local_path, target=remote_path, 
          override_cluster_name='default', down=False)
    

if __name__ == '__main__':
    main()
