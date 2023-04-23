# github-mirror
This tool mirrors all your repos by cloning/pulling them periodically.

# Required config
Put the following according to `secrets.yaml.example` into a `secrets.yaml` file.
- PERSONAL_ACCESS_TOKEN [fine grained token](https://github.com/settings/tokens?type=beta) or [classic token](https://github.com/settings/tokens)
- USERNAME (github username)

# Optional config
- BACKUP_DELAY_IN_SECONDS (you can change this in the `docker-compose.yml` file)

# Getting started
```
mkdir ./data
chmod o+rw data/
docker-compose up --build
```