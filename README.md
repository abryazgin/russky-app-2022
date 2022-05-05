# russky-app-2022

Some application to demonstrate DevOps work

* Run tests
    ```bash
    make test
    ```
* Run linters & prettify
    ```bash
    make plint
    ```
* Run server
    ```bash
    make run
    ```

## Cheatsheets

### Docker

#### Login

[Instruction](https://cloud.yandex.ru/docs/container-registry/operations/authentication) (get token
by [link](https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb)):

```bash
docker login --username oauth --password <token> cr.yandex
```

#### Build

```bash
docker build -t cr.yandex/<registry id>/russky-app-2022 .
docker push cr.yandex/<registry id>/russky-app-2022
```

#### Run on VM

* Go to VM vis ssh
  ```bash
  ssh <vm>
  ```
* Install docker
  ```bash
  sudo apt install docker.io
  ```
* Configure docker to work without `sudo` ([instruction](https://docs.docker.com/engine/install/linux-postinstall/))
  ```bash
  sudo usermod -aG docker $USER
  ```
* Login into docker on VM
  ```bash
  docker login --username oauth --password <token> cr.yandex
  ```
* Run docker image with auto-restart
  ```bash
  # simple run
  docker run -it -p 8080:8080 --pull always cr.yandex/crphntksaqh2dho7ale3/russky-app-2022
  # daemonized run with auto-restart
  docker run -it -p 8080:8080 --pull always -d --restart unless-stopped cr.yandex/crphntksaqh2dho7ale3/russky-app-2022
  ```

### Start ELK

```bash
sudo sysctl -w vms.tf.max_map_count=262144
```
or https://stackoverflow.com/questions/42889241/how-to-increase-vm-max-map-count

### Prepare CI/CD

By [deploy instruction](https://cloud.yandex.ru/docs/cos/tutorials/vm-update) (login instruction - [link](https://cloud.yandex.ru/docs/cli/quickstart))

1. List service accounts
  ```bash
  yc iam service-account --folder-id <folder_id> list
  ```
2. Generate service-account key
  ```bash
  yc iam key create --folder-id  <folder_id> --service-account-name <sa name> --output key.json
  ```
3. Put secrets in GitHub:

   * `CONTAINER_REGISTRY_ID` == <registry_id>
   * `CONTAINER_REGISTRY_TOKEN` = <получить по [ссылке](https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb) >
   * `YC_SA_KEY_JSON` with content of key.json
   * `YC_INSTANCE_GROUP_ID` = <instance_group_id>

## TODO

* ELK alerts