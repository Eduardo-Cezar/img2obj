#!/bin/bash

pip3 install ailia

git clone --depth 1 https://github.com/axinc-ai/ailia-models

pip3 install -r ailia-models/neural_rendering/tripo_sr/requirements.txt

pip3 install onnxruntime