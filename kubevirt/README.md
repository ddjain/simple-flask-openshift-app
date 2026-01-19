# KubeVirt on OpenShift - Setup Guide

Quick setup guide for running virtual machines on OpenShift using KubeVirt.

## Prerequisites

- OpenShift cluster (4.x)
- `kubectl` or `oc` CLI configured
- `virtctl` CLI installed

### Install virtctl

```bash
VERSION=$(curl -s https://storage.googleapis.com/kubevirt-prow/release/kubevirt/kubevirt/stable.txt)
curl -L -o virtctl https://github.com/kubevirt/kubevirt/releases/download/${VERSION}/virtctl-${VERSION}-darwin-amd64
chmod +x virtctl
sudo mv virtctl /usr/local/bin/
```

## Installation

### Step 1: Install KubeVirt Operator

```bash
export VERSION=$(curl -s https://storage.googleapis.com/kubevirt-prow/release/kubevirt/kubevirt/stable.txt)
echo $VERSION

kubectl create -f "https://github.com/kubevirt/kubevirt/releases/download/${VERSION}/kubevirt-operator.yaml"
```

### Step 2: Deploy KubeVirt CR

```bash
kubectl apply -f kubevirt-cr.yaml
```

Or from upstream:
```bash
kubectl create -f "https://github.com/kubevirt/kubevirt/releases/download/${VERSION}/kubevirt-cr.yaml"
```

### Step 3: Wait for Deployment

```bash
kubectl get kubevirt -n kubevirt -w
```

Wait until `PHASE` shows `Deployed`.

### Step 4: Verify Components

```bash
kubectl get pods -n kubevirt
```

All pods should be `Running`:
- virt-operator
- virt-api
- virt-controller
- virt-handler (on each worker node)

## Create a VM

### Simple VM (CirrOS)

```bash
kubectl apply -f vm2.yaml
```

### Fedora VM with Nginx

```bash
kubectl apply -f vm-fedora.yaml
```

## VM Operations

```bash
# List VMs
kubectl get vms

# Start VM
virtctl start <vm-name>

# Stop VM
virtctl stop <vm-name>

# Console access
virtctl console <vm-name>

# Delete VM
kubectl delete vm <vm-name>
```

## Expose VM Service

```bash
virtctl expose vm <vm-name> --port=80 --name=<service-name> --type=ClusterIP
```

## Troubleshooting

### ErrorUnschedulable - No KVM Support

If VMs fail with `ErrorUnschedulable` and message about `Insufficient devices.kubevirt.io/kvm`:

```bash
kubectl patch kubevirt kubevirt -n kubevirt --type=merge \
  -p '{"spec":{"configuration":{"developerConfiguration":{"useEmulation":true}}}}'
```

Then restart the VM:
```bash
virtctl stop <vm-name>
virtctl start <vm-name>
```

### Check VM Status

```bash
kubectl describe vmi <vm-name>
```

## Files

| File | Description |
|------|-------------|
| `kubevirt-cr.yaml` | KubeVirt CR with emulation enabled |
| `vm.yaml` | Sample testvm (CirrOS) |
| `vm2.yaml` | myvm (CirrOS, auto-start) |
| `vm-fedora.yaml` | Fedora VM with nginx |

## VM Credentials

| VM | User | Password |
|----|------|----------|
| CirrOS (testvm, myvm) | cirros | gocubsgo |
| Fedora | fedora | fedora |
