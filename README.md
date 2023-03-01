# FastAPI for ML inference on Docker - demo app

Demo app for FastAPI for machine learning inference on Docker. Deployable to Kubernetes.

## Process for adding a new machine learning model

- Add a project to the root folder
- Write SQL in a `<project>/data.sql` file
- Download data using a `<project>/download_data.ipynb` script
- Train model using `<project>/train.ipynb` script
- Add `app/` folder with a `main.py` file serving FastAPI
- Add a `Dockerfile` per project to containerize the project/app
- Add to `kubernetes/` folder as a Service using ClusterIP
- Call API endpoint from within the Kubernetes cluster `http://demo-fastapi-ml-service-prod`, etc


## Docker

- Building the image locally, pass the `--build-arg PYTHON_ENV=development` to set the `ARG` and then `ENV` correctly for development.

```bash
DATE=$(date +%Y%m%d-%H%M%S)
DOCKER_BUILDKIT=1 docker build . -t briansigafoos/docker-fastapi-ml-inference:$DATE --build-arg PYTHON_ENV=development

# View FastAPI docs in browser at http://0.0.0.0:80/docs
docker run -p 80:80 briansigafoos/docker-fastapi-ml-inference:$DATE

# Run in bash
docker run --rm -i -t briansigafoos/docker-fastapi-ml-inference:$DATE bash
```

### First time setup

First push up for the new package repository

```shell
docker login ghcr.io --username <USERNAME>
# Then enter token

# Then build
DOCKER_BUILDKIT=1 docker build . -t ghcr.io/BrianSigafoos/docker-fastapi-ml-inference:first_push

# Then push
docker push ghcr.io/BrianSigafoos/docker-fastapi-ml-inference:first_push
```

## Development

Install [poetry](https://python-poetry.org/docs/#installation)

```shell
# Change config to create .venv folder in project root
poetry config virtualenvs.in-project true

# Set the Python version for poetry to use. If there's no .venv, it will create one.
poetry env use 3.11

# Example commands
poetry install
poetry update
poetry shell
poetry add black --group dev
```

### Git LFS

Initial setup to

```shell
brew install git-lfs
git lfs track "*.joblib"
git lfs track "*.pickle"
git add .gitattributes
```

### Linters

- Install [black](https://github.com/psf/black) `poetry add black --group dev` + `poetry add 'black[jupyter]' --group dev`
- Install [pre-commit] `poetry add pre-commit --group dev` and `pre-commit install; touch .pre-commit-config.yaml`

## Testing

Use `pytest`. Just run `pytest` in the root folder.

## Debugging

Similar to `binding.pry` in Ruby, jump into code with Python debugger: `pdb`

```shell
  import pdb; pdb.set_trace()
```

## Maintenance

- Update pre-commit hooks using `pre-commit autoupdate`

## Kubernetes

### K8s Deployment

```shell
# 1. Set env
K8S_ENV=prod #(!! update SHA in step 2!!)

# 2. Set SHA
# Update newTag SHA in kubernetes/overlays/$K8S_ENV/kustomization.yaml

# 3. Check diff
k diff -k kubernetes/overlays/$K8S_ENV

# 4. Apply and watch
k apply -k kubernetes/overlays/$K8S_ENV --validate; kgpwide -w

# 5. Validate up using url or health check
# TBD

# 6. Check pod distribution and utilization on nodes
k resource-capacity --pods --util

# 7. Debug a running pod. Get pods: kgp; POD=...
keti $POD -- /bin/bash

# 8. Rollout history and rollback
# kubectl rollout history deployment/...
krh deployment/demo-fastapi-ml-canary
# kubectl rollout undo deployment/...
kru deployment/demo-fastapi-ml-canary
```
### K8s Debugging

- <https://kubernetes.io/docs/tasks/debug-application-cluster/debug-application/>
- <https://kubernetes.io/docs/tasks/debug-application-cluster/debug-running-pod/>

```shell
# Get pod name
# kubectl get pod
kgp

# Set env vars
POD=
CONTAINER=demo-fastapi-ml-container

# Describe the pod to target. Shows Events on that pod
# kubectl describe pod $POD
kdp $POD

# View logs
# kubectl logs
# kl $POD $CONTAINER
kl $POD
# If failed
# kl $POD $CONTAINER --previous
kl $POD --previous

# Get interactive shell into the pod for debugging
# kubectl exec --stdin --tty $POD -- /bin/bash
keti $POD -- /bin/bash

# Create temporary debug pod copied from running pod
# k debug $POD -it --image=ubuntu --share-processes --copy-to=app-debug

# Debug a container that fails to start
# https://kubernetes.io/docs/tasks/debug-application-cluster/debug-running-pod/#copying-a-pod-while-changing-its-command
k debug $POD -it --copy-to=app-debug --container=$CONTAINER -- sh

k attach app-debug -c $CONTAINER -it

# Try running commands on container
# kubectl exec ${POD} -c ${CONTAINER} -- ${CMD} ${ARG1} ${ARG2} ... ${ARGN}
k exec $POD -c $CONTAINER --

# Clean up
k delete pod app-debug
```

### K8s monitoring

- Install [krew](https://github.com/kubernetes-sigs/krew)
  - Add to .zshrc (in instructions)
- Install [resource-capacity](https://github.com/robscott/kube-capacity) using `kubectl krew install resource-capacity and use it:

```shell
kubectl resource-capacity --util
kubectl resource-capacity --pods

kubectl resource-capacity --pods --util
```

### K8s secrets

Create secrets

```shell
# 1. Create file .env.production.local
# 2. Use a pw manager for contents
# 3. Create secret (after steps 1 and 2))
kubectl create secret generic demo-fastapi-ml-secrets --from-env-file='.env.production.local'
# 4. Verify secrets (see more commands below)
kubectl describe secret demo-fastapi-ml-secrets
# 5. Delete file .env.production.local
rm .env.production.local
```

Editing secrets

```shell
# Check secrets
kubectl get secret
# List all secrets
kubectl describe secret
# Show this secret
kubectl describe secret demo-fastapi-ml-secrets

# Delete secret
kubectl delete secrets demo-fastapi-ml-secrets

# Edit secrets to change/update
kubectl edit secrets demo-fastapi-ml-secrets
```

### ML Ops / Deployment research

#### Kubernetes

- FastAPI, uvicorn - <https://fastapi.tiangolo.com/deployment/server-workers/?h=kubernetes>
  - <https://fastapi.tiangolo.com/deployment/docker/>
- <https://towardsdatascience.com/machine-learning-with-docker-and-kubernetes-training-models-cbe33a08c999>
- <https://towardsdatascience.com/machine-learning-with-docker-and-kubernetes-batch-inference-4a25328f23c7>
- <https://mlinproduction.com/k8s-jobs/>

#### BentoML

- <https://docs.bentoml.org/en/latest/>
- [Comprehensive Guide to Deploying Any ML Model as APIs With Python And AWS Lambda](https://towardsdatascience.com/comprehensive-guide-to-deploying-any-ml-model-as-apis-with-python-and-aws-lambda-b441d257f1ec)
