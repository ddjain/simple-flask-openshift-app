# Network Chaos for KubeVirt VMs

Injects network latency and packet loss to KubeVirt VM pods using krkn.

## Setup

1. Copy your kubeconfig to `config/kubeconfig`
2. Edit `config/scenarios/pod_egress_shaping.yml` to adjust latency/loss values

## Run

```bash
sh run.sh
```

## Configuration

| File | Description |
|------|-------------|
| `config/kubeconfig` | Kubernetes cluster credentials |
| `config/config.yaml` | Krkn main configuration |
| `config/scenarios/pod_egress_shaping.yml` | Network chaos parameters |
