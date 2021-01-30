# Installation

First, run the following on all kubernetes nodes:

1. docker.sh
2. system_setup.sh
3. kubeadm.sh

Disable swap permanently:

```
sudo swapoff -a

# Comment out any lines that configure swap:
sudo vi /etc/fstab
```

Logout and log back in.

Now run the following on the control node:

```
kubeadm config images pull

# Take note of the join command that is output by init, you'll need it later
sudo kubeadm init

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

# Configure networking

Update each host's /etc/hosts file with the name and IP of the other servers.

Modify the calico.yaml file as needed, then apply it:

```
kubectl apply -f calico.yaml
kubectl apply -f calicoctl.yaml
```

To make execution of calicoctl easier, set up an alias in your .bashrc or .profile

Now is the time to execute the node join command on each of the worker nodes.  Once complete, label the worker nodes:
`kubectl label node dell01 node-role.kubernetes.io/worker=worker`

# Install helm

```
helm.sh
```

# Option 1: use bitnami

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install spark1 -f spark_helm_values.yaml bitnami/spark
kubectl port-forward --namespace default svc/spark1-master-svc 80:80
```

# Option 2: Build spark

Install R: `spark.sh`

Clone the spark source repo:
`git clone https://github.com/apache/spark.git`

Then run the build: 
`./dev/make-distribution.sh --name custom-spark --pip --r --tgz -Psparkr -Phive -Phive-thriftserver -Pmesos -Pyarn -Pkubernetes`

Then run the python container build:
`./bin/docker-image-tool.sh -t pyspark -p ./kubernetes/dockerfiles/spark/bindings/python/Dockerfile build`


# Install glusterfs

This must be run on each node in the cluster.

```
sudo apt install software-properties-common
sudo add-apt-repository ppa:gluster/glusterfs-7
sudo apt update
sudo apt install glusterfs-server glusterfs-client
sudo systemctl start glusterd.service
sudo systemctl enable glusterd.service
```

## Now configure the glusterfs storage

Run this on each node in the cluster:
```
sudo mkdir /var/finance-data
sudo mkdir /var/data
```

Run this on only one node:
```
sudo gluster peer probe dell02
sudo gluster peer probe dell01
sudo gluster volume create finance-data hp01:/var/finance-data dell01:/var/finance-data dell02:/var/finance-data
sudo gluster volume start finance-data
sudo gluster volume create data hp01:/var/data dell01:/var/data dell02:/var/data
sudo gluster volume start data

kubectl create -f gluster-endpoint.yaml
kubectl create -f gluster-service.yaml
```

# Configure prometheus and grafana

Or just install via Lens settings for the cluster.
```
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo update
helm install prometheus-stak --set prometheusOperator.createCustomResource=false prometheus-community/kube-prometheus-stack
```

# Mount the glusterfs volume on host

This is needed if you want to run things directly on the host to access the gluster volume.

```
sudo modprobe fuse

# Add the following to /etc/fstab
# glusterfs finance-data volume mount
hp01:/finance-data /finance-data glusterfs defaults,_netdev 0 0

sudo mount -a
```



# Useful commands

```
# To list pods
kubectl get pods

# To get into a pod:
kubectl exec -it spark1-master-0 -- /bin/bash

# Search for prometheus helm charts
helm search repo prometheus-community
```

