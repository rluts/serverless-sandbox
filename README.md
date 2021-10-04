## Serverless framework
* `$ npm i`

Deploy all resources and services
```
$ $./deploy_all.sh
```

Removing stack
```
$ ./remove_all.sh
```
## CDK

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

Deployment:

```
$ cdk deploy
```

Removing stack:
```
$ cdk destroy
```
