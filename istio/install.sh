# Download Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

# Install Istio with demo profile
istioctl install --set profile=demo -y

# Enable automatic sidecar injection
kubectl label namespace user istio-injection=enabled
kubectl label namespace order istio-injection=enabled
kubectl label namespace payment istio-injection=enabled
