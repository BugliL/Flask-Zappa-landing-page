# Flask-Zappa-landing-page
Project to create something for logging results from a landing page POST

Main notes for Zappa in [https://github.com/BugliL/prova_zappa](https://github.com/BugliL/prova_zappa)


## With aws configured
Config file containing aws profiles credentials ~/.aws/credentials
```ini
[zappa]
region=eu-west-1
aws_access_key_id = your_access_key_id_specific_to_zappa
aws_secret_access_key = your_secret_access_key_specific_to_zappa
```

```bash
$ export AWS_PROFILE=zappa
$ alias zappashell3='docker run -ti -e AWS_PROFILE=zappa -v $(pwd):/var/task -v ~/.aws/:/root/.aws  --rm lambci/lambda:build-python3.6 bash'
$ cd /your_zappa_project
$ zappashell3
bash-4.2#
```

```bash
bash-4.2# virtualenv ve
bash-4.2# source ve/bin/activate
(ve) bash-4.2# pip install -r requirements.txt
(ve) bash-4.2# pip install zappa
(ve) bash-4.2# zappa init
```

```bash
$ zappa deploy dev
$ zappa update dev
```
