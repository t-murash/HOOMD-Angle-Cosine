# HOOMD-blue v6.0.0 RTX 5090対応パッチ

このディレクトリには、NVIDIA GeForce RTX 5090でHOOMD-blue v6.0.0を動作させるために修正したファイルが含まれています。

## 修正したファイル

### 1. ExecutionConfiguration.cc
**元のファイルパス**: `hoomd-blue/hoomd/ExecutionConfiguration.cc`

**修正内容**:
- **Lines 388-410**: 管理メモリチェックをコメントアウト（RTX 5090は`cudaDevAttrConcurrentManagedAccess`非対応）
- **Lines 267-269**: `cudaSetValidDevices()`呼び出しをコメントアウト（特定GPU IDの場合）
- **Lines 277-279**: `cudaSetValidDevices()`呼び出しをコメントアウト（自動検出の場合）

### 2. ExecutionConfiguration.h
**元のファイルパス**: `hoomd-blue/hoomd/ExecutionConfiguration.h`

**修正内容**:
- **Lines 132-140**: `setDevice()`メソッドの検証ロジックを`if (m_gpu_id >= 0)`から`if (exec_mode == GPU)`に変更

### 3. Autotuner.h
**元のファイルパス**: `hoomd-blue/hoomd/Autotuner.h`

**修正内容**:
- **Lines 495-497**: CUDA event作成前に`hipGetLastError()`を呼び出して保留中のエラーをクリア

## 適用方法

### 方法1: ファイルの直接置き換え

```bash
# HOOMD-blueソースディレクトリに移動
cd /path/to/hoomd-blue

# 修正ファイルをバックアップ
cp hoomd/ExecutionConfiguration.cc hoomd/ExecutionConfiguration.cc.orig
cp hoomd/ExecutionConfiguration.h hoomd/ExecutionConfiguration.h.orig
cp hoomd/Autotuner.h hoomd/Autotuner.h.orig

# 修正ファイルをコピー
cp /path/to/hoomd-v6.0.0-mod/hoomd/ExecutionConfiguration.cc hoomd/
cp /path/to/hoomd-v6.0.0-mod/hoomd/ExecutionConfiguration.h hoomd/
cp /path/to/hoomd-v6.0.0-mod/hoomd/Autotuner.h hoomd/

# 再ビルド
cd build
ninja
ninja install
```

### 方法2: パッチの手動適用

各ファイルの指定された行を手動で編集してください。詳細は`../CLAUDE.md`の「2025-12-18: RTX 5090 GPU実行の問題解決」セクションを参照。

## 修正の詳細

### 問題の背景

NVIDIA GeForce RTX 5090（Compute Capability 12.0）は以下の理由でHOOMD-blue v6.0.0がそのままでは動作しません:

1. RTX 5090は`cudaDevAttrConcurrentManagedAccess`属性をサポートしていない
2. `cudaSetValidDevices()`がRTX 5090で予期しないエラーを引き起こす
3. GPU初期化中に"invalid device ordinal"エラーが保留される

### 修正の効果

- ✅ RTX 5090でのGPU認識が成功
- ✅ GPU計算の実行が可能
- ✅ ベンチマーク結果: 3,832.39 TPS (1000粒子LJ流体)

## 動作確認環境

- **GPU**: NVIDIA GeForce RTX 5090
- **CUDA**: 12.6.85
- **HOOMD-blue**: v6.0.0
- **Python**: 3.13.9
- **OS**: Linux (WSL2)
- **Compiler**: GCC 13.3.0

## 注意事項

1. これらの修正はRTX 5090での動作を優先したワークアラウンドです
2. 他のGPUでの動作には影響しないはずですが、十分にテストされていません
3. 将来のHOOMD-blueバージョンでは公式に対応される可能性があります
4. 管理メモリ（Managed Memory）を使用する機能には影響がある可能性があります

## ライセンス

修正ファイルはオリジナルのHOOMD-blueと同じBSD 3-Clause Licenseに従います。

## 参考資料

- HOOMD-blue公式: https://hoomd-blue.readthedocs.io/
- 修正の詳細: `../CLAUDE.md`
