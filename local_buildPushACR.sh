az acr login --name jtf191
docker image build ./"$1" -t jtf191.azurecr.io/"$1":latest
docker push jtf191.azurecr.io/"$1":latest