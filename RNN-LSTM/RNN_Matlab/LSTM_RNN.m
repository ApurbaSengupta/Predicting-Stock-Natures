function [net] = LSTM_RNN(XTrain, YTrain)

  % Get the sequence lengths for each observation.
    numObservations = numel(XTrain);
    for i=1:numObservations
        sequence = XTrain{i};
        sequenceLengths(i) = size(sequence,2);
    end

  % Sort the data by sequence length.
    [~,idx] = sort(sequenceLengths);
    XTrain = XTrain(idx);
    YTrain = YTrain(idx);

  % Define LSTM Network Architecture
    inputSize = 100;
    numHiddenUnits = 120; %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    numClasses = 2;

    layers = [ ...
        sequenceInputLayer(inputSize)
        bilstmLayer(numHiddenUnits,'OutputMode','last')
        fullyConnectedLayer(numClasses)
        softmaxLayer
        classificationLayer];

  % Now specify the training options
    maxEpochs = 60;
    miniBatchSize = 25; 

    options = trainingOptions('adam', ...
        'ExecutionEnvironment','auto', ...
        'MaxEpochs',maxEpochs, ...
        'MiniBatchSize',miniBatchSize, ...
        'SequenceLength','longest', ...
        'Shuffle','never', ...
        'Verbose',0, ...
        'Plots','training-progress');

  % Train the LSTM network with the specified training options by using trainNetwork.
    net = trainNetwork(XTrain,YTrain,layers,options);

end