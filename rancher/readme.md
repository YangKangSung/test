v1.33.0+k3s1

curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.33.0+k3s1 K3S_TOKEN=CelestialBeing sh -s - server --cluster-init

192.168.0.8:6443
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.33.0+k3s1 K3S_TOKEN=CelestialBeing sh -s - server --server https://192.168.0.8:6443
