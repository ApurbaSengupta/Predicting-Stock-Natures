This folder contains the code for RNN implemented in PyTorch using Google Colaboratory on Google Drive. Hence, the code is to use Google Colaboratory which can be added as an additional app to your Google Drive. Please see https://www.kdnuggets.com/2018/02/google-colab-free-gpu-tutorial-tensorflow-keras-pytorch.html for more details.

The notebook LSTM_RNN_Classifier_50d_GloVe.ipynb is the script that implements LSTM-RNN for the used data for 50d GloVe representations of words. The notebook LSTM_RNN_Classifier_100d_GloVe.ipynb is the script that implements LSTM-RNN for the used data for 50d GloVe representations of words. 

The raw data are available as labeled_data_bin.json which is a copy of oracle/data/labeled_data.json. The 50d GloVe word-embeddings are present in the file glove.6B.50d.txt and the 100d GloVe word-embeddings are present in the file glove.6B.100d.txt.

The .mat files created in the BATCH50d and BATCH100d folders are used in the MATLAB R2018 implementation of LSTM-RNN and are same as in oracle/RNN-LSTM/RNN_Matlab.
