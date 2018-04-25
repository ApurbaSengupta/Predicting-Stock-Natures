%% MATLAB Script for running LSTM Recurrent Neural Network 
clear all
clc

% Loading Training Data
load('X_train.mat');
load('y_train.mat');

% Loading Test Data
load('X_test.mat');
load('y_test.mat');

y_train = (y_train' + 3) / 2;
y_test = (y_test' + 3) / 2;

X_train = cellfun(@transpose,X_train','UniformOutput',false);
X_test = cellfun(@transpose,X_test','UniformOutput',false);
y_train = categorical(y_train);
y_test = categorical(y_test);


net = LSTM_RNN(X_train, y_train);

%% Sort the test data by sequence length.

numObservationsTest = numel(X_test);
for i=1:numObservationsTest
    sequence = X_test{i};
    sequenceLengthsTest(i) = size(sequence,2);
end

[sequenceLengthsTest,idx] = sort(sequenceLengthsTest);
XTest = X_test(idx);
YTest = y_test(idx);

% Classify the test data. To reduce the amount of padding introduced by the classification process, set the mini-batch size to 27
for i=1:150
miniBatchSize = i;
YPred = classify(net,XTest, ...
    'MiniBatchSize',miniBatchSize, ...
    'SequenceLength','longest');

% Calculate the classification accuracy of the predictions.
acc(i) = sum(YPred == YTest)./numel(YTest)
end

[m,i]=max(acc)