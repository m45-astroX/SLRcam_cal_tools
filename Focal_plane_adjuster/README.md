# Focal_plane_adjuster

2025.02.16 v1 by Yuam Aoki

一眼レフカメラのAF位置の補正量を算出するツール


## 使用例

- Bartinov maskを装着した一眼レフカメラを用いて、点光源を複数回撮影する

- 撮影したNEFファイルをコンポジット(加算平均)し、TIFFファイルとして保存する

    $ python3 composite.py indir(NEFファイルを格納しているディレクトリ) -o composite.tif

- コンポジットした画像ファイルに座標を付加する

    $ python3 coordinate.py composite.tif -o grid.png

- 座標を付加した画像ファイルを用いて、点光源の空間輝度分布を始点座標および終点座標を決定する

- 点光源の空間輝度分布を作成する

    $ python3 plot_profile.py composite.tif 1000 2000 1000 2500 -r 

- 空間輝度分布のフィットを行う

    $ python3 fit.py 
