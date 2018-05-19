### CIS 520 Final Project - Stock Market Prediction
Our CIS 520 final project is to predict the price movement of stocks in the tech sector, based on
recent news about the particular company

### Project Requirements
Python 3.6 (with OpenSSL 1.0)

### Build Instructions
pip install -r requirements.txt

### Data Format
labeled_data.json schema (example)
    [{article: text_of_article_here, stock: AAPL, label: 1, date: 2018-04-13, source: bloomberg}, {...}, ...]

grouped_data.json schema (example)
    {
        AAPL: [ list of article dictionaries ],
        NVDA: [ list of article dictionaries ], 
        ...
    }
    
### Implementation
The code for SVM, Logistic Regression and Naive Bayes classifiers can be found in linear_models/src folder.

The code for LSTM-RNN classifier using PyTorch and MATLAB R2018 can be found in the folders RNN-LSTM/run_py and RNN-LSTM/RNN_Matlab respectively. 
