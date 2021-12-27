# データサイエンスチャレンジ2021 サンプル

## 概要
線形補間と Catmull–Rom Spline 補間のサンプル Python スクリプトです。

データサイエンスチャレンジ2021の出題意図としましては、訓練用データ(train.csv)から機械学習モデルを作成して、そのモデルに推論させてモーションデータ補間することではありますが、このサンプルスクリプトがデータファイルの読み書き方法等の最初の一歩になればと思います。

この simple_interp.py を実行して得られるデータの暫定スコアは線形補間で0.96、Catmull–Rom Spline 補間で0.8になります。

## 実行方法
1. input_data/test/ ディレクトリに test_easy.csv、test_normal.csv、test_hard.csv を配置します。
1. simple_interp.py を実行します。

## ライセンス
These codes are licensed under CC0.

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)