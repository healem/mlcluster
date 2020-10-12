#!/usr/bin/env bash
#
# Taken from k8s install page: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/
#

# Ensure iptables can see bridged traffic
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system

