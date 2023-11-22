# FastAPI Kubernetes Service on Minikube

FastAPI web service that is deployed with Kubernetes (K8s) on the local Minikube cluster.

The FastAPI web service has three APIs that log information in a log file. This log file will be rotated later using a scheduled K8s Job. Alternatively, you can use Python logging handlers such as `RotatingFileHandler` that support the rotation of log files.

The deployment contains local persistent volume (PV) with `ReadWriteMany` access mode. The PV resides in the Minikube cluster under the `/persistent_volume/logs` path. The persistent volume claim (PVC) requests storage from the local PV. The deployment has one pod replica and pulls the docker image from the Minikube cluster. Hence the image pull policy is set to: `imagePullPolicy: Never`. It mounts the `/var/log/fastapi_app` logging folder to the PVC. Then, the pod is exposed as service, listening on the 8000 port.

A scheduled job (`CronJob`) performs log rotation on the logging folder, and it executes every minute. The job also mounts the logging directory and a log rotation config file (`ConfigMap`). The configuration file is put under the `/etc/logrotate.d` folder. The `copytruncate` option is important because it can be used when some program cannot be told to close its log file and thus might *continue writing* (appending) to the previous log file forever. If it is omitted, the web service can't write to the log file.

# Prerequisites

- Docker: Install the Docker engine: https://docs.docker.com/engine/install/
- Kubernetes: Download the Kubernetes command line tool: https://kubernetes.io/releases/download/
- Minikube: Install the local Minikube cluster: https://minikube.sigs.k8s.io/docs/start/

# Deploying with Uvicorn

Create a virtual environment:

```
python -m venv .venv
```

Activate the virtual environment:

```
source .venv/bin/activate # Linux
source .venv/Scripts/activate # Windows
```

Install the dependencies:

```
pip install -r app/requirements.txt
```

Serve the FastAPI web service using Uvicorn web server:

```
uvicorn app.main:app --reload
```

Go to the [generate log folders](http://127.0.0.1:8000/docs#/default/generate_log_folders_generate_log_folders__num_folders__get) API and create log folders. After the generation, archive the log folders:

```
python archiver/main.py
```

Verify the content of the compressed file:

```
tar -tzf <archived_[CURRENT_DATE].tar.gz>
```

# Deploying with Docker

Build the docker image:

```
docker build -t fastapi .
```

Create a container from the docker image:

```
docker run -p 8000:8000 fastapi
```

Visit the <http://localhost:8000/docs> SwaggerUI website. Generate logs via APIs.

# Deploying with Kubernetes

Initiate the Minikube cluster:

```
minikube start
```

Reuse the Minikube's Docker daemon:

```
eval $(minikube docker-env)
docker build -t fastapi-image .
```

Go inside the cluster:

```
minikube ssh
```

Create the persistent volume folder inside the Minikube cluster:

```
sudo mkdir -p /persistent_volume/logs
```

Create the K8s resource:

```
kubectl apply -f deployment.yml
```

Tunnel the service through Minikube to access it from the browser:

```
minikube service fastapi-service
```

Open the SwaggerUI and generate logs.

# Useful Commands

```
kubectl delete -f deployment.yml # delete the k8s workloads
kubectl get all # listing k8s workloads
kubectl rollout restart deployment fastapi-deployment # restart deployment
kubectl describe pod <pod_name> # describe pod info
kubectl logs <pod_name> -p # get logs from pod
kubectl exec -it <pod_name> -- sh # attach shell to pod
minikube image ls # list minikube images
minikube ssh # step into minikube
minikube stop # stop minikube
minikube delete # delete the VM, and associated files
rm -rf $HOME/.minikube # purge minikube
eval $(minikube docker-env -u) # deactivate docker daemon reuse
```
