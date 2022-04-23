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
docker-compose build app
docker-compose push app
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
  docker run -p 80:80 --pull always cr.yandex/crphntksaqh2dho7ale3/russky-app-2022
  # daemonized run with auto-restart
  docker run -p 80:80 --pull always -d --restart unless-stopped cr.yandex/crphntksaqh2dho7ale3/russky-app-2022
  ```

### Start ELK

```bash
sudo sysctl -w vms.tf.max_map_count=262144
```

## TODO

* ELK alerts