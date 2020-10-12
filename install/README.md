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
sudo kubeadm init
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

# Configure networking

Modify the calico.yaml file as needed, then apply it:

```
kubectl apply -f calico.yaml
kubectl apply -f calicoctl.yaml
```

To make execution of calicoctl easier, set up an alias in your .bashrc or .profile
