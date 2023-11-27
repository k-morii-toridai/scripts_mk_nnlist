#!/bin/bash

# gfortranがインストールされているか確認
if ! command -v gfortran &> /dev/null
then
    echo "gfortranが見つかりません。最新版のインストールを開始します。"
    
    # インストール
    sudo apt-get update
    sudo apt-get install -y gfortran
else
    echo "gfortranは既にインストールされています。最新版にアップグレードします。"
    sudo apt-get update
    sudo apt-get upgrade -y gfortran
fi

# setup poscar2nnlist
unzip neib_code.zip
cd neib_code
gfortran m_ftox.f90 neib.f90 -o poscar2nnlist
