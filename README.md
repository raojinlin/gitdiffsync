# git diff sync tool

将本地修改应用到服务器的git副本

## 场景
假设有个功能需要在某个测试服务器上排查问题，但是服务器上又不好查代码，这个时候可以在本地修改，然后提交修改到git，服务器拉下代码。但是这样可能会产生很多无意义的提交。
这个时候就可以使用```git diff```和```git apply```两个命令来操作，```git diff```将本地修改输出然后在到服务器上```git apply```一下就好了。

## 使用
### 本地
```bash
$ git diff | gitdiffapply --host <server address> --port <server port> --chdir <chdir>
```

### 服务器
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
$ python3 ./src/diffsyncserver.py
```

