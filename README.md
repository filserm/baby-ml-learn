# baby-ml-learn

## Installation guide

### Docker base image -> for starting the learning POD
```
docker build -f Dockerfile.base -t baby-learn:v1 .
```

```
docker image tag baby-learn:v1 filsermichael/baby-learn:latest
```

```
docker image push filsermichael/baby-learn:latest

```

### Docker code image -> for running the mic and applying the model
```
docker build -f Dockerfile.code -t baby-monitor:v1 .
```

### run the app
docker run -it --device=/dev/snd:/dev/snd --user appuser baby-monitor:v1 /bin/bash